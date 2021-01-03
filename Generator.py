from antlr4 import *

from ToyCLexer import ToyCLexer
from ToyCParser import ToyCParser
from ToyCVisitor import ToyCVisitor
from ToyCSymbolTable import SymbolTable
from ToyCErrorListener import syntaxErrorListener, SemanticError

# Pionniers du TJ, benissiez-moi par votre Esprits Saints!
from llvmlite import ir
from llvmlite import binding as llvm

llvm.initialize()
llvm.initialize_native_target()
llvm.initialize_native_asmprinter()

ir_double = ir.DoubleType()
ir_bool = ir.IntType(1)
ir_int = ir.IntType(32)
ir_pointer = ir.IntType(8)
ir_void = ir.VoidType()

class ToyCGenerator(ToyCVisitor):
    def __init__(self):
        super(ToyCVisitor, self).__init__()
        self.module = ir.Module()
        self.module.triple = llvm.Target.from_default_triple()
        backing_mod = llvm.parse_assembly("")
        target_machine = self.module.triple.create_target_machine()
        self.module.data_layout = llvm.create_mcjit_compiler(backing_mod, target_machine)

        self.blocks = []
        self.builders = []
        self.funcs = {}
        self.current_func = []
        self.n_string = 0
        self.need_load = True
        self.end_if = None

        self.symbol_table = SymbolTable()
    
    
    #运算和表达式求值，类型转换相关函数
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

    def exprConvert(self, index1, index2):
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
    
    def visitID(self, ctx:ToyCParser.IDContext):
        return self.visit(ctx.getChild(0))
    
    def visitMULDIV(self, ctx:ToyCParser.MULDIVContext):
        builder = self.builders[-1]
        index1, index2 = self.exprConvert(self.visit(ctx.getChild(0)), self.visit(ctx.getChild(2)))
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
        index1, index2 = self.exprConvert(self.visit(ctx.getChild(0)), self.visit(ctx.getChild(2)))
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

    def visitArrayItem(self, ctx:ToyCParser.ArrayItemContext):
        return self.visit(ctx.getChild(0))

    def visitArgument(self, ctx:ToyCParser.ArgumentContext):
        return self.visit(ctx.getChild(0))

    def visitItemID(self, ctx:ToyCParser.ItemIDContext):
        item_name = ctx.getText()
        JudgeReg = False
        if not self.symbol_table.ifExist(item_name):
           return {'type': ir_int, 'const': JudgeReg, 'name': ir.Constant(ir_int, None)}
        builder = self.builders[-1]
        item = self.symbol_table.get(item_name)
        if item is not None:
            if self.need_load:
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
        index = ProcessIndex[1:-1]
        index += '\0'
        length = len(bytearray(ProcessIndex, 'utf-8'))
        return_value = ir.GlobalVariable(self.module, ir.ArrayType(ir_pointer, length), ".str_id_%d" % self.n_string)
        return_value.global_constant = True
        return_value.initializer = ir.Constant(ir.ArrayType(ir_pointer, Len), bytearray(ProcessIndex, 'utf-8'))
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
    print(generator.module)
    generator.save_to_file(output_filename)
