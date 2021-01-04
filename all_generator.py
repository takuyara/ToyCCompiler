 # Pionniers du TJ, benissiez-moi par votre Esprits Saints!
from antlr4 import *
from llvmlite import ir
from llvmlite import binding as llvm
from ToyCLexer import ToyCLexer
from ToyCParser import ToyCParser
from ToyCVisitor import ToyCVisitor
from ToyCSymbolTable import SymbolTable
from ToyCError import CompileError
from ToyCSymbolTable import SymbolTable

llvm.initialize()
llvm.initialize_native_target()
llvm.initialize_native_asmprinter()

ir_double = ir.DoubleType()
ir_bool = ir.IntType(1)
ir_int = ir.IntType(32)
ir_pointer = ir.IntType(8)
ir_void = ir.VoidType()
ir_char = ir.IntType(8)

class ToyCGenerator(ToyCVisitor):
    def __init__(self):
        super(ToyCVisitor, self).__init__()
        self.module = ir.Module()
        '''
        self.module.triple = llvm.Target.from_default_triple()
        backing_mod = llvm.parse_assembly("")
        target_machine = self.module.triple.create_target_machine()
        self.module.data_layout = llvm.create_mcjit_compiler(backing_mod, target_machine)
        '''
        self.module.triple = "x86_64-pc-linux-gnu"
        self.module.data_layout = "e-m:e-i64:64-f80:128-n8:16:32:64-S128"

        self.blocks = []
        self.builders = []
        self.funcs = {}
        self.current_func = []
        self.n_string = 0
        self.need_load = True
        self.endif_block = None

        # TODO: symbol table
        self.symbol_table = SymbolTable()

    def visitProg(self, ctx: ToyCParser.ProgContext):
        # prog :(include)* (initBlock|initArrBlock|mFunction)*;
        for i in range(ctx.getChildCount()):
            self.visit(ctx.getChild(i))

    def visitParameter(self, ctx: ToyCParser.ParameterContext):
        # parameter : itemType itemID;
        return {"type": self.visit(ctx.getChild(0)), "name": ctx.getChild(1).getText()}
    
    def visitParameters(self, ctx: ToyCParser.ParametersContext):
        # parameters : parameter (','parameter)* |;
        if ctx.getChildCount() == 0:
            return []
        params = []
        for i in range(0, ctx.getChildCount(), 2):
            params.append(self.visit(ctx.getChild(i)))
        return params

    def visitBody(self, ctx: ToyCParser.BodyContext):
        # body : (block | func';')*;
        for i in range(ctx.getChildCount()):
            self.visit(ctx.getChild(i))
            if self.blocks[-1].is_terminated:
                break

    def visitReturnBlock(self, ctx: ToyCParser.ReturnBlockContext):
        # returnBlock : 'return' (itemINT|itemID)? ';';
        if ctx.getChildCount() == 2:
            return_value = self.builders[-1].ret_void()
            return {"type": ir_void, "const": True, "name": return_value}
        index = self.visit(ctx.getChild(1))
        return_value = self.builders[-1].ret(index["name"])
        return {"type": ir_void, "const": True, "name": return_value}

    def visitFuncBody(self, ctx: ToyCParser.FuncBodyContext):
        # funcBody : body returnBlock;
        self.symbol_table.addLevel()
        for i in range(ctx.getChildCount()):
            self.visit(ctx.getChild(i))
        self.symbol_table.declineLevel()

    def visitItemFunction(self, ctx: ToyCParser.ItemFunctionContext):
        # itemFunction : (itemType|itemVoid) itemID '(' parameters ')' '{' funcBody '}';
        return_value_type = self.visit(ctx.getChild(0))
        func_name = ctx.getChild(1).getText()
        params = self.visit(ctx.getChild(3))
        param_types = []
        for i in params:
            param_types.append(i["type"])
        ir_func_type = ir.FunctionType(return_value_type, param_types)
        ir_func = ir.Function(self.module, ir_func_type, name = func_name)
        for i in range(len(params)):
            ir_func.args[i].name = params[i]["name"]
        if func_name in self.funcs:
            raise CompileError(context = ctx, message = "Duplicate function name.")
        self.funcs[func_name] = ir_func
        block = ir_func.append_basic_block(name = func_name + ".block")
        self.blocks.append(block)
        builder = ir.IRBuilder(block)
        self.builders.append(builder)
        self.current_func = func_name
        # TODO: Check
        self.symbol_table.addLevel()
        variables = {}
        for i in range(len(params)):
            current_param = params[i]
            variable_name = builder.alloca(current_param["type"])
            builder.store(ir_func.args[i], variable_name)
            current_variable = {
                "type": current_param["type"],
                "name": variable_name,
            }
            if not self.symbol_table.add(current_param["name"], current_variable):
                raise CompileError(context = ctx, message = "Duplicate variable name.")
        self.visit(ctx.getChild(6))
        self.current_func = ""
        self.blocks.pop()
        self.builders.pop()
        self.symbol_table.declineLevel()

    def visitPrintfFun(self, ctx: ToyCParser.PrintfFunContext):
        # printfFun : 'printf' '(' (itemSTRING | itemID) (','expr)* ')';
        if "printf" in self.funcs:
            ir_func = self.funcs["printf"]
        else:
            param_types = ir.FunctionType(ir_int, [ir.PointerType(ir_pointer)], var_arg = True)
            ir_func = ir.Function(self.module, param_types, name = "printf")
            self.funcs["printf"] = ir_func
        builder = self.builders[-1]
        zero = ir.Constant(ir_int, 0)
        params = self.visit(ctx.getChild(2))
        args = [builder.gep(params["name"], [zero, zero], inbounds = True)]
        if ctx.getChildCount() == 4:
            return_value_name = builder.call(ir_func, args)
        else:
            for i in range(4, ctx.getChildCount() - 1, 2):
                param = self.visit(ctx.getChild(i))
                args.append(param["name"])
            return_value_name = builder.call(ir_func, args)
        return {"type": ir_int, "name": return_value_name}

    def visitScanfFun(self, ctx: ToyCParser.ScanfFunContext):
        # scanfFun : 'scanf' '(' itemSTRING (','('&')?(itemID|arrayItem))* ')';
        if "scanf" in self.funcs:
            ir_func = self.funcs["scanf"]
        else:
            param_types = ir.FunctionType(ir_int, [ir.PointerType(ir_pointer)], var_arg = True)
            ir_func = ir.Function(self.module, param_types, name = "scanf")
            self.funcs["scanf"] = ir_func
        builder = self.builders[-1]
        zero = ir.Constant(ir_int, 0)
        params = self.visit(ctx.getChild(2))
        # print("Text: ", ctx.getChild(0).getText())
        args = [builder.gep(params["name"], [zero, zero], inbounds = True)]
        i = 4
        while i < ctx.getChildCount() - 1:
            offset = 1 if ctx.getChild(i).getText() == "&" else 0
            tmp = self.need_load
            self.need_load = offset == 0
            param = self.visit(ctx.getChild(i + offset))
            self.need_load = tmp
            args.append(param["name"])
            i += offset + 2
        return_value_name = builder.call(ir_func, args)
        return {"type": ir_int, "name": return_value_name}

    def visitStrlenFun(self, ctx: ToyCParser.StrlenFunContext):
        if "strlen" in self.funcs:
            ir_func = self.funcs["strlen"]
        else:
            param_types = ir.FunctionType(ir_int, [ir.PointerType(ir_char)], var_arg = False)
            ir_func = ir.Function(self.module, param_types, name = "strlen")
            self.funcs["strlen"] = ir_func
        builder = self.builders[-1]
        zero = ir.Constant(ir_int, 0)
        tmp = self.need_load
        self.need_load = False
        params = self.visit(ctx.getChild(2))
        self.need_load = tmp
        args = [builder.gep(params["name"], [zero, zero], inbounds = True)]
        return {"type": ir_int, "name": builder.call(ir_func, args)}

    def visitGetsFun(self, ctx: ToyCParser.GetsFunContext):
        if "gets" in self.funcs:
            ir_func = self.funcs["gets"]
        else:
            param_types = ir.FunctionType(ir_int, [], var_arg = True)
            ir_func = ir.Function(self.module, param_types, name = "gets")
            self.funcs["gets"] = ir_func
        builder = self.builders[-1]
        zero = ir.Constant(ir_int, 0)
        tmp = self.need_load
        self.need_load = False
        params = self.visit(ctx.getChild(2))
        self.need_load = tmp
        args = [builder.gep(params["name"], [zero, zero], inbounds = True)]
        return {"type": ir_int, "name": builder.call(ir_func, args)}

    def visitOtherFun(self, ctx: ToyCParser.OtherFunContext):
        # otherFun : itemID '('((argument|itemID)(','(argument|itemID))*)? ')';
        builder = self.builders[-1]
        func_name = ctx.getChild(0).getText()
        if func_name not in self.funcs:
            raise CompileError(context = ctx, message = "Undefined function")
        ir_func = self.funcs[func_name]
        params = []
        for i in range(2, ctx.getChildCount() - 1, 2):
            param = self.visit(ctx.getChild(i))
            # TODO: Check convert func
            param = self.convert(param, ir_func.args[(i >> 1) - 1].type)
            params.append(param["name"])
        return_value_name = builder.call(ir_func, params)
        return {"type": ir_func.function_type.return_type, "name": return_value_name}

    def visitBlock(self, ctx: ToyCParser.BlockContext):
        # block : initBlock | initArrBlock | ifBlocks | forBlock | whileBlock | assignBlock | returnBlock;
        for i in range(ctx.getChildCount()):
            self.visit(ctx.getChild(i))

    def visitInitBlock(self, ctx: ToyCParser.InitBlockContext):
        # initBlock : (itemType) itemID ('=' expr)? (',' itemID ('=' expr)?)* ';';
        item_type = self.visit(ctx.getChild(0))
        i = 1
        while i < ctx.getChildCount():
            item_name = ctx.getChild(i).getText()
            if self.symbol_table.isGlobal():
                ir_variable = ir.GlobalVariable(self.module, item_type, name = item_name);
                ir_variable.linkage = "internal"
            else:
                ir_variable = self.builders[-1].alloca(item_type, name = item_name)
            variable = {"type": item_type, "name": ir_variable}
            if not self.symbol_table.add(item_name, variable):
                raise CompileError(context = ctx, message = "Duplicate variable name")
            if ctx.getChild(i + 1).getText() != "=":
                i += 2
            else:
                init_value = self.visit(ctx.getChild(i + 2))
                if self.symbol_table.isGlobal():
                    ir_variable.initializer = ir.Constant(init_value["type"], init_value["name"].constant)
                else:
                    init_value = self.convert(init_value, item_type)
                    self.builders[-1].store(init_value["name"], ir_variable)
                i += 4

    def visitInitArrBlock(self, ctx: ToyCParser.InitArrBlockContext):
        # initArrBlock : itemType itemID '[' itemINT ']'';';
        item_type = self.visit(ctx.getChild(0))
        item_name = ctx.getChild(1).getText()
        item_length = int(ctx.getChild(3).getText())
        if self.symbol_table.isGlobal():
            ir_variable = ir.GlobalVariable(self.module, ir.ArrayType(item_type, item_length), name = item_name)
            ir_variable.linkage = "internal"
        else:
            ir_variable = self.builders[-1].alloca(ir.ArrayType(item_type, item_length), name = item_name)
        variable = {"type": ir.ArrayType(item_type, item_length), "name": ir_variable}
        if not self.symbol_table.add(item_name, variable):
            raise CompileError(context = ctx, message = "Duplicate array name")

    def visitAssignBlock(self, ctx: ToyCParser.AssignBlockContext):
        # assignBlock : ((arrayItem|itemID) '=')+  expr ';';
        builder = self.builders[-1]
        item_id = ctx.getChild(0).getText()
        if '[' not in item_id and not self.symbol_table.ifExist(item_id):
            raise CompileError(context = ctx, message = "Undefined variable")
        print("Value: ", ctx.getChild(ctx.getChildCount() - 2).getText())
        right_value = self.visit(ctx.getChild(ctx.getChildCount() - 2))
        right_value = {"type": right_value["type"], "name": right_value["name"]}
        # print("Name: ", right_value["name"])
        for i in range(0, ctx.getChildCount() - 2, 2):
            tmp = self.need_load
            self.need_load = False
            left_value = self.visit(ctx.getChild(i))
            self.need_load = tmp
            # TODO: Check if this is right
            # print("Left name: ", left_value["name"])
            value_for_this = self.convert(right_value, left_value["type"])
            # print("ASSIGN: ", left_value["name"], "   FFFF     ", value_for_this["name"])
            builder.store(value_for_this["name"], left_value["name"])
            # TODO: Chekc if this is right
        return {"type": left_value["type"], "name": builder.load(left_value["name"])}

    def visitCondition(self, ctx: ToyCParser.ConditionContext):
        # condition :  expr;
        return self.toBoolean(self.visit(ctx.getChild(0)), False)

    def __update_2b(self, block):
        a, b = self.blocks.pop(), self.builders.pop()
        self.blocks.append(block)
        self.builders.append(ir.IRBuilder(block))
        return a, b

    def visitIfBlocks(self, ctx: ToyCParser.IfBlocksContext):
        # ifBlocks : ifBlock (elifBlock)* (elseBlock)?;
        builder = self.builders[-1]
        if_block = builder.append_basic_block()
        endif_block = builder.append_basic_block()
        builder.branch(if_block)
        self.__update_2b(if_block)
        tmp = self.endif_block
        self.endif_block = endif_block
        for i in range(ctx.getChildCount()):
            self.visit(ctx.getChild(i))
        self.endif_block = tmp
        # TODO: Check order correct
        tmp_block, tmp_builder = self.__update_2b(endif_block)
        if not tmp_block.is_terminated:
            tmp_builder.branch(endif_block)
        
    def visitIfBlock(self, ctx: ToyCParser.IfBlockContext):
        # ifBlock : 'if' '('condition')' '{' body '}';
        self.symbol_table.addLevel()
        builder = self.builders[-1]
        true_block = builder.append_basic_block()
        false_block = builder.append_basic_block()
        condition = self.visit(ctx.getChild(2))
        builder.cbranch(condition["name"], true_block, false_block)
        self.blocks.pop()
        self.builders.pop()
        self.blocks.append(true_block)
        self.builders.append(ir.IRBuilder(true_block))
        self.visit(ctx.getChild(5))
        if not self.blocks[-1].is_terminated:
            self.builders[-1].branch(self.endif_block)
        self.blocks.pop()
        self.builders.pop()
        self.blocks.append(false_block)
        self.builders.append(ir.IRBuilder(false_block))
        # TODO: Check asymmetrical
        self.symbol_table.declineLevel()

    def visitElifBlock(self, ctx: ToyCParser.ElifBlockContext):
        # elifBlock : 'else' 'if' '(' condition ')' '{' body '}';
        self.symbol_table.addLevel()
        builder = self.builders[-1]
        true_block = builder.append_basic_block()
        false_block = builder.append_basic_block()
        condition = self.visit(ctx.getChild(3))
        builder.cbranch(condition["name"], true_block, false_block)
        self.__update_2b(true_block)
        self.visit(ctx.getChild(6))
        if not self.builders[-1].is_terminated:
            self.builders[-1].branch(self.endif_block)
        self.__update_2b(false_block)
        # TODO: Check asymmetrical
        self.symbol_table.declineLevel()

    def visitElseBlock(self, ctx: ToyCParser.ElseBlockContext):
        # elseBlock : 'else' '{' body '}';
        self.symbol_table.addLevel()
        self.visit(ctx.getChild(2))
        self.symbol_table.declineLevel()

    def visitWhileBlock(self, ctx: ToyCParser.WhileBlockContext):
        self.symbol_table.addLevel()
        builder = self.builders[-1]
        condition_block = builder.append_basic_block()
        print("Condition: ", condition_block)
        body = builder.append_basic_block()
        print("Body: ", body)
        end_while = builder.append_basic_block()
        builder.branch(condition_block)
        # self.__update_2b(condition_block)
        self.blocks.pop()
        self.builders.pop()
        self.blocks.append(condition_block)
        self.builders.append(ir.IRBuilder(condition_block))

        condition = self.visit(ctx.getChild(2))
        self.builders[-1].cbranch(condition["name"], body, end_while)

        #self.__update_2b(body)
        self.blocks.pop()
        self.builders.pop()
        self.blocks.append(body)
        self.builders.append(ir.IRBuilder(body))
        self.visit(ctx.getChild(5))

        self.builders[-1].branch(condition_block)

        # self.__update_2b(end_while)
        self.blocks.pop()
        self.builders.pop()
        self.blocks.append(end_while)
        self.builders.append(ir.IRBuilder(end_while))
        
        self.symbol_table.declineLevel()

    def visitForBlock(self, ctx: ToyCParser.ForBlockContext):
        # forBlock : 'for' '(' forExpr  ';' condition ';' forExpr ')' ('{' body '}'|';');
        self.symbol_table.addLevel()
        self.visit(ctx.getChild(2))
        builder = self.builders[-1]
        condition_block = builder.append_basic_block()
        body = builder.append_basic_block()
        end_for = builder.append_basic_block()
        builder.branch(condition_block)
        self.__update_2b(condition_block)
        condition = self.visit(ctx.getChild(4))
        self.builders[-1].cbranch(condition["name"], body, end_for)
        self.__update_2b(body)
        if ctx.getChildCount() == 11:
            self.visit(ctx.getChild(9))
        self.visit(ctx.getChild(6))
        self.builders[-1].branch(condition_block)
        self.__update_2b(end_for)
        self.symbol_table.declineLevel()

    def visitForExpr(self, ctx: ToyCParser.ForExprContext):
        # forExpr :  itemID '=' expr (',' forExpr)?|;
        if ctx.getChildCount() == 0:
            return
        tmp = self.need_load
        self.need_load = False
        item_id = self.visit(ctx.getChild(0))
        self.need_load = tmp
        expr_id = self.convert(self.visit(ctx.getChild(2)), item_id["type"])
        # print("left: %s, right: %s" % (item_id["name"], expr_id["name"]))
        self.builders[-1].store(expr_id["name"], item_id["name"])
        if ctx.getChildCount() > 3:
            self.visit(ctx.getChild(4))

    def convert(self, index, data_type):
        if (index['type'] == data_type):
            return index
        if self.isInteger(index['type']) and self.isInteger(data_type):
            if (index['type'] == ir_bool):
                index = self.convertIIZ(index, data_type)
            else:
                index = self.convertIIS(index, data_type)
        elif self.isInteger(index['type']) and data_type == ir_double:
            index = self.convertIDS(index)
        elif self.isInteger(data_type) and index['type'] == ir_double:
            index = self.convertDIS(index)
        return index
    
    def convertIIZ(self, index, data_type):
        return {'type': data_type, 'const': False, 'name': self.builders[-1].zext(index['name'], data_type)}

    def convertIIS(self, index, data_type):
        return {'type': data_type, 'const': False, 'name': self.builders[-1].sext(index['name'], data_type)}

    def convertDIS(self, index, data_type):
        return {'type': data_type, 'const': False, 'name': self.builders[-1].fptosi(index['name'], data_type)}

    def convertDIU(self, index, data_type):
        return { 'type': data_type, 'const': False, 'name': self.builders[-1].fptoui(index['name'], data_type)}

    def convertIDS(self, index):
        return {'type': ir_double, 'const': False, 'name': self.builders[-1].sitofp(index['name'], ir_double)}

    def convertIDU(self, index):
        return {'type': ir_double, 'const': False, 'name': self.builders[-1].uitofp(index['name'], ir_double)}
    
    def isInteger(self, object):
        return hasattr(object, "width")

    def expr_convert(self, index1, index2):
        if index1['type'] == index2['type']:
            return index1, index2
        if self.isInteger(index1['type']) and self.isInteger(index2['type']):
            if index1['type'].width < index2['type'].width:
                if index1['type'].width == 1:
                    index1 = self.convertIIZ(index1, index2['type'])
                else:
                    index1 = self.convertIIS(index1, index2['type'])
            else:
                if index2['type'].width == 1:
                    index2 = self.convertIIZ(index2, index1['type'])
                else:
                    index2 = self.convertIIS(index2, index1['type'])
        elif self.isInteger(index1['type']) and index2['type'] == double:
            index1 = convertIDS(index1, index2['type'])
        elif self.isInteger(index2['type']) and index1['type'] == double:
            index2 = convertIDS(index2, index1['type'])
        else:
            raise CompileError(context=ctx,message="Type mismatch.")
        return index1, index2

    def visitFunc(self, ctx:ToyCParser.FuncContext):
        return self.visit(ctx.getChild(0))
  
    def visitARRAY(self, ctx:ToyCParser.ARRAYContext):
        return self.visit(ctx.getChild(0))
    
    def visitSTRING(self, ctx:ToyCParser.STRINGContext):
        return self.visit(ctx.getChild(0))
    
    def visitDOUBLE(self, ctx:ToyCParser.DOUBLEContext):
        if ctx.getChild(0).getText() == '-':
            index = self.visit(ctx.getChild(1))
            return {'type': index['type'], 'name': self.builders[-1].neg(index['name'])}
        return self.visit(ctx.getChild(0))
    
    def visitEQUA(self, ctx: ToyCParser.EQUAContext):
        # expr op=('==' | '!=' | '<' | '<=' | '>' | '>=') expr
        builder = self.builders[-1]
        op1, op2 = self.expr_convert(self.visit(ctx.getChild(0)), self.visit(ctx.getChild(2)))
        operator = ctx.getChild(1).getText()
        if op1["type"] == ir_double:
            return_value = builder.fcmp_ordered(operator, op1["name"], op2["name"])
        elif self.isInteger(op1["type"]):
            return_value = builder.icmp_signed(operator, op1["name"], op2["name"])
        else:
            raise CompileError(ctx, "Type mismatch: not able to compare.")
        return {"type": ir_bool, "const": False, "name": return_value}

    def visitID(self, ctx:ToyCParser.IDContext):
        return self.visit(ctx.getChild(0))
    
    def visitMULDIV(self, ctx:ToyCParser.MULDIVContext):
        builder = self.builders[-1]
        index1, index2 = self.expr_convert(self.visit(ctx.getChild(0)), self.visit(ctx.getChild(2)))
        JudgeReg = False
        if ctx.getChild(1).getText() == '*':
            return_value = builder.mul(index1['name'], index2['name'])
        elif ctx.getChild(1).getText() == '/':
            return_value = builder.sdiv(index1['name'], index2['name'])
        elif ctx.getChild(1).getText() == '%':
            return_value = builder.srem(index1['name'], index2['name'])
        return {'type': index1['type'], 'const': False, 'name': return_value}
    
    def visitADDSUB(self, ctx:ToyCParser.ADDSUBContext):
        builder = self.builders[-1]
        index1, index2 = self.expr_convert(self.visit(ctx.getChild(0)), self.visit(ctx.getChild(2)))
        if ctx.getChild(1).getText() == '+':
            return_value = builder.add(index1['name'], index2['name'])
        elif ctx.getChild(1).getText() == '-':
            return_value = builder.sub(index1['name'], index2['name'])
        return {'type': index1['type'], 'const': False, 'name': return_value}
    
    def visitNEG(self, ctx:ToyCParser.NEGContext):
        index1 = self.visit(ctx.getChild(0))
        return {"type": index1["type"], "const": False, "name": self.toBoolean(self.visit(ctx.getChild(1)), notFlag = True)}
        
    def visitINT(self, ctx:ToyCParser.INTContext):
        if ctx.getChild(0).getText() == '-':
            index = self.visit(ctx.getChild(1))
            return {'type': index['type'], 'name': self.builders[-1].neg(index["name"])}
        return self.visit(ctx.getChild(0))

    def visitFUNCTION(self, ctx:ToyCParser.FUNCTIONContext):
        return self.visit(ctx.getChild(0))

    def visitOR(self, ctx:ToyCParser.ORContext):
        index1 = self.toBoolean(self.visit(ctx.getChild(0)), notFlag=False)
        index2 = self.toBoolean(self.visit(ctx.getChild(2)), notFlag=False)
        return_value = self.builders[-1].or_(index1['name'], index2['name'])
        return {'type': index1['type'], 'const': False, 'name': return_value}
    
    def visitCHAR(self, ctx:ToyCParser.CHARContext):
        return self.visit(ctx.getChild(0))
    
    def visitItemArray(self, ctx:ToyCParser.ItemArrayContext):
        return {'name': ctx.getChild(0).getText(), 'length': int(ctx.getChild(2).getText())}

    def visitItemVoid(self, ctx:ToyCParser.ItemVoidContext):
        return ir_void

    def visitItemType(self, ctx: ToyCParser.ItemTypeContext):
        if ctx.getText() == "int":
            return ir_int
        if ctx.getText() == "char":
            return ir_char
        if ctx.getText() == "double":
            return ir_double
        return ir_void

    def visitArrayItem(self, ctx:ToyCParser.ArrayItemContext):
        # print(ctx.getText())
        tmp = self.need_load
        self.need_load = False
        res = self.visit(ctx.getChild(0))
        self.need_load = tmp
        if not isinstance(res["type"], ir.types.ArrayType):
            raise CompileError(context = ctx, message = "Type mismatch. Not an array.")
        builder = self.builders[-1]
        tmp = self.need_load
        self.need_load = True
        index = self.visit(ctx.getChild(2))
        self.need_load = tmp
        zero = ir.Constant(ir_int, 0)
        # print("Resname: ", res["name"], "   Indexname: ", index["name"])
        return_value = builder.gep(res["name"], [zero, index["name"]], inbounds = True)
        # print(return_value)
        if self.need_load:
            # print("Load")
            return_value = builder.load(return_value)
        return {"type": res["type"].element, "const": False, "name": return_value}

    def visitArgument(self, ctx:ToyCParser.ArgumentContext):
        return self.visit(ctx.getChild(0))

    def visitItemID(self, ctx:ToyCParser.ItemIDContext):
        item_name = ctx.getText()
        # print(item_name)
        JudgeReg = False
        if not self.symbol_table.ifExist(item_name):
           return {'type': ir_int, 'const': JudgeReg, 'name': ir.Constant(ir_int, None)}
        builder = self.builders[-1]
        item = self.symbol_table.get(item_name)
        if item is not None:
            if self.need_load:
                # print(item)
                return {"type" : item["type"], "const" : False, "name" : builder.load(item["name"])}
            else:
                return {"type" : item["type"], "const" : False, "name" : item["name"]}
        else:
            return {'type': ir_void, 'const': False, 'name': ir.Constant(ir_void, None)}

    def visitItemINT(self, ctx:ToyCParser.ItemINTContext):
        return {'type': ir_int, 'const': True, 'name': ir.Constant(ir_int, int(ctx.getText()))}

    def visitItemDOUBLE(self, ctx:ToyCParser.ItemDOUBLEContext):
        return {'type': ir_double, 'const': True, 'name': ir.Constant(ir_double, float(ctx.getText()))}

    def visitItemCHAR(self, ctx:ToyCParser.ItemCHARContext):
        return {'type': ir_char, 'const': True, 'name': ir.Constant(ir_char, ord(ctx.getText()[1]))}

    def visitItemSTRING(self, ctx:ToyCParser.ItemSTRINGContext):
        self.n_string += 1
        index = ctx.getText().replace('\\n', '\n')
        index = index[1:-1]
        index += '\0'
        length = len(bytearray(index, 'utf-8'))
        return_value = ir.GlobalVariable(self.module, ir.ArrayType(ir_pointer, length), ".str_id_%d" % self.n_string)
        return_value.global_constant = True
        return_value.initializer = ir.Constant(ir.ArrayType(ir_pointer, length), bytearray(index, 'utf-8'))
        return {'type': ir.ArrayType(ir_pointer, length), 'const': False, 'name': return_value}

    def toBoolean(self, index, notFlag = True):
        builder = self.builders[-1]
        if notFlag:
            operator = '=='
        else:
            operator = '!='
        if index['type'] == ir_pointer or index['type'] == ir_int:
            return {'type': ir_bool, 'const': False, 'name': builder.icmp_signed(operator, index['name'], ir.Constant(index['type'], 0))}
        elif index['type'] == ir_double:
            return {'type': ir_bool, 'const': False, 'name': builder.fcmp_ordered(operator, index['name'], ir.Constant(ir_double, 0))}
        return index
    
    def save_to_file(self, filename):
        with open(filename, "w") as f:
            f.write(repr(self.module))

def generate(input_filename, output_filename):
    lexer = ToyCLexer(FileStream(input_filename))
    stream = CommonTokenStream(lexer)    
    parser = ToyCParser(stream)
    tree = parser.prog()
    generator = ToyCGenerator()
    generator.visit(tree)
    # print(generator.module)
    generator.save_to_file(output_filename)
