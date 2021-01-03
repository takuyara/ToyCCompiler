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
    def convert(self, CalcIndex, DType):
        if (CalcIndex['type'] == DType):
            return CalcIndex
        if self.isInteger(CalcIndex['type']) and self.isInteger(DType):
            if (CalcIndex['type'] == ir_bool):
                CalcIndex = self.convertIIZ(CalcIndex, DType)
            else:
                CalcIndex = self.convertIIS(CalcIndex, DType)
        elif self.isInteger(CalcIndex['type']) and DType == ir_double:
            CalcIndex = self.convertIDS(CalcIndex)
        elif self.isInteger(DType) and CalcIndex['type'] == ir_double:
            CalcIndex = self.convertDIS(CalcIndex)
        return CalcIndex
    
    def convertIIZ(self, CalcIndex, DType):
        Builder = self.builders[-1]
        ConfirmedVal = Builder.zext(CalcIndex['name'], DType)
        JudgeReg = False
        return {
                'type': DType,
                'const': JudgeReg,
                'name': ConfirmedVal
        }

    def convertIIS(self, CalcIndex, DType):
        Builder = self.builders[-1]
        ConfirmedVal = Builder.sext(CalcIndex['name'], DType)
        JudgeReg = False
        return {
                'type': DType,
                'const': JudgeReg,
                'name': ConfirmedVal
        }

    def convertDIS(self, CalcIndex, DType):
        Builder = self.builders[-1]
        ConfirmedVal = Builder.fptosi(CalcIndex['name'], DType)
        JudgeReg = False
        return {
                'type': DType,
                'const': JudgeReg,
                'name': ConfirmedVal
        }

    def convertDIU(self, CalcIndex, DType):
        Builder = self.builders[-1]
        ConfirmedVal = Builder.fptoui(CalcIndex['name'], DType)
        JudgeReg = False
        return {
                'type': DType,
                'const': JudgeReg,
                'name': ConfirmedVal
        }

    def convertIDS(self, CalcIndex):
        Builder = self.builders[-1]
        ConfirmedVal = Builder.sitofp(CalcIndex['name'], ir_double)
        JudgeReg = False
        return {
                'type': ir_double,
                'const': JudgeReg,
                'name': ConfirmedVal
        }

    def convertIDU(self, CalcIndex):
        Builder = self.builders[-1]
        JudgeReg = False
        ConfirmedVal = Builder.uitofp(CalcIndex['name'], ir_double)
        return {
                'type': ir_double,
                'const': JudgeReg,
                'name': ConfirmedVal
        }
    
    def isInteger(self, object):
        return hasattr(object, "width")

    def exprConvert(self, Index1, Index2):
        if Index1['type'] == Index2['type']:
            return Index1, Index2
        if self.isInteger(Index1['type']) and self.isInteger(Index2['type']):
            if Index1['type'].width < Index2['type'].width:
                if Index1['type'].width == 1:
                    Index1 = self.convertIIZ(Index1, Index2['type'])
                else:
                    Index1 = self.convertIIS(Index1, Index2['type'])
            else:
                if Index2['type'].width == 1:
                    Index2 = self.convertIIZ(Index2, Index1['type'])
                else:
                    Index2 = self.convertIIS(Index2, Index1['type'])
        elif self.isInteger(Index1['type']) and Index2['type'] == double:
            Index1 = convertIDS(Index1, Index2['type'])
        elif self.isInteger(Index2['type']) and Index1['type'] == double:
            Index2 = convertIDS(Index2, Index1['type'])
        else:
            raise SemanticError(ctx=ctx,msg="类型不匹配")
        return Index1, Index2

    def visitFunc(self, ctx:ToyCParser.FuncContext):
        return self.visit(ctx.getChild(0))

    def visitGetsFun(self, ctx:ToyCParser.GetsFunContext):
        if 'gets' in self.funcs:
            gets = self.funcs['gets']
        else:
            getsType = ir.FunctionType(ir_int, [], var_arg = True)
            gets = ir.Function(self.module, getsType, name = "gets")
            self.funcs['gets'] = gets

        TheBuilder = self.builders[-1]
        zero = ir.Constant(ir_int, 0)

        PreviousNeedLoad = self.WhetherNeedLoad
        self.WhetherNeedLoad = False
        ParameterInfo = self.visit(ctx.getChild(2))
        self.WhetherNeedLoad = PreviousNeedLoad

        Arguments = [TheBuilder.gep(ParameterInfo['name'], [zero, zero], inbounds = True)]
        ReturnVariableName = TheBuilder.call(gets, Arguments)
        Result = {'type': int32, 'name': ReturnVariableName}
        return Result
    
    def visitARRAY(self, ctx:ToyCParser.ARRAYContext):
        return self.visit(ctx.getChild(0))
    
    def visitSTRING(self, ctx:ToyCParser.STRINGContext):
        return self.visit(ctx.getChild(0))
    
    def visitDOUBLE(self, ctx:ToyCParser.DOUBLEContext):
        if ctx.getChild(0).getText() == '-':
            IndexMid = self.visit(ctx.getChild(1))
            Builder = self.builders[-1]
            RealReturnValue = Builder.neg(IndexMid['name'])
            return {
                    'type': IndexMid['type'],
                    'name': RealReturnValue
            }
        return self.visit(ctx.getChild(0))
    
    def visitID(self, ctx:ToyCParser.IDContext):
        return self.visit(ctx.getChild(0))
    
    def visitMULDIV(self, ctx:ToyCParser.MULDIVContext):
        Builder = self.builders[-1]
        Index1 = self.visit(ctx.getChild(0))
        Index2 = self.visit(ctx.getChild(2))
        Index1, Index2 = self.exprConvert(Index1, Index2)
        JudgeReg = False
        if ctx.getChild(1).getText() == '*':
            RealReturnValue = Builder.mul(Index1['name'], Index2['name'])
        elif ctx.getChild(1).getText() == '/':
            RealReturnValue = Builder.sdiv(Index1['name'], Index2['name'])
        elif ctx.getChild(1).getText() == '%':
            RealReturnValue = Builder.srem(Index1['name'], Index2['name'])
        return {
                'type': Index1['type'],
                'const': JudgeReg,
                'name': RealReturnValue
        }
    
    def visitADDSUB(self, ctx:ToyCParser.ADDSUBContext):
        Builder = self.builders[-1]
        Index1 = self.visit(ctx.getChild(0))
        Index2 = self.visit(ctx.getChild(2))
        Index1, Index2 = self.exprConvert(Index1, Index2)
        JudgeReg = False
        if ctx.getChild(1).getText() == '+':
            RealReturnValue = Builder.add(Index1['name'], Index2['name'])
        elif ctx.getChild(1).getText() == '-':
            RealReturnValue = Builder.sub(Index1['name'], Index2['name'])
        return {
                'type': Index1['type'],
                'const': JudgeReg,
                'name': RealReturnValue
        }
    
    def visitNEG(self, ctx:ToyCParser.NEGContext):
        RealReturnValue = self.visit(ctx.getChild(1))
        RealReturnValue = self.toBoolean(RealReturnValue, notFlag = True)
        # res 未返回
        return self.visitChildren(ctx)
    
    def visitINT(self, ctx:ToyCParser.INTContext):
        if ctx.getChild(0).getText() == '-':
            IndexMid = self.visit(ctx.getChild(1))
            Builder = self.builders[-1]
            RealReturnValue = Builder.neg(IndexMid['name'])
            return {
                    'type': IndexMid['type'],
                    'name': RealReturnValue
            }
        return self.visit(ctx.getChild(0))

    def visitFUNCTION(self, ctx:ToyCParser.FUNCTIONContext):
        return self.visit(ctx.getChild(0))

    def visitOR(self, ctx:ToyCParser.ORContext):
        Index1 = self.visit(ctx.getChild(0))
        Index1 = self.toBoolean(Index1, notFlag=False)
        Index2 = self.visit(ctx.getChild(2))
        Index2 = self.toBoolean(Index2, notFlag=False)
        Builder = self.builders[-1]
        RealReturnValue = Builder.or_(Index1['name'], Index2['name'])
        return {
                'type': Index1['type'],
                'const': False,
                'name': RealReturnValue
        }
    
    def visitCHAR(self, ctx:ToyCParser.CHARContext):
        return self.visit(ctx.getChild(0))
    
    

    def visitCondition(self, ctx:ToyCParser.ConditionContext):
        result = self.visit(ctx.getChild(0))
        return self.toBoolean(result, notFlag=False)

    def visitItemArray(self, ctx:ToyCParser.ItemArrayContext):
        return {
            'IDname': ctx.getChild(0).getText(),
            'length': int(ctx.getChild(2).getText())
        }

    def visitItemVoid(self, ctx:ToyCParser.ItemVoidContext):
        return ir_void

    def visitArrayItem(self, ctx:ToyCParser.ArrayItemContext):
        return self.visit(ctx.getChild(0))



    def visitOtherFun(self, ctx:ToyCParser.OtherFunContext):
        #获取返回值类型
        ReturnType = self.visit(ctx.getChild(0)) # mtype
        
        #获取函数名 todo
        FunctionName = ctx.getChild(1).getText() # func name
        
        #获取参数列表
        ParameterList = self.visit(ctx.getChild(3)) # func params

        #根据返回值，函数名称和参数生成llvm函数
        ParameterTypeList = []
        for i in range(len(ParameterList)):
            ParameterTypeList.append(ParameterList[i]['type'])
        LLVMFunctionType = ir.FunctionType(ReturnType, ParameterTypeList)
        LLVMFunction = ir.Function(self.module, LLVMFunctionType, name = FunctionName)

        #存储函数的变量        
        for i in range(len(ParameterList)):
            LLVMFunction.args[i].name = ParameterList[i]['IDname']

        #存储函数的block
        TheBlock = LLVMFunction.append_basic_block(name = FunctionName + '.entry')

        #判断重定义，存储函数
        if FunctionName in self.Functions:
            raise SemanticError(ctx=ctx,msg="函数重定义错误！")
        else:
            self.Functions[FunctionName] = LLVMFunction

        TheBuilder = ir.IRBuilder(TheBlock)
        self.blocks.append(TheBlock)
        self.builders.append(TheBuilder)

        #进一层
        self.current_func = FunctionName
        self.symbol_table.addLevel()

        #存储函数的变量
        VariableList = {}
        for i in range(len(ParameterList)):
            NewVariable = TheBuilder.alloca(ParameterList[i]['type'])
            TheBuilder.store(LLVMFunction.args[i], NewVariable)
            TheVariable = {}
            TheVariable["Type"] = ParameterList[i]['type']
            TheVariable["Name"] = NewVariable
            TheResult = self.SymbolTable.AddItem(ParameterList[i]['IDname'], TheVariable)
            if TheResult["result"] != "success":
                raise SemanticError(ctx=ctx,msg=TheResult["reason"])

        #处理函数body
        self.visit(ctx.getChild(6)) # func body

        #处理完毕，退一层
        self.CurrentFunction = ''
        self.blocks.pop()
        self.builders.pop()
        self.symbol_table.declineLevel()
        return

    def visitArgument(self, ctx:ToyCParser.ArgumentContext):
        return self.visit(ctx.getChild(0))

    def visitItemID(self, ctx:ToyCParser.ItemIDContext):
        IDname = ctx.getText()
        JudgeReg = False
        if self.symbol_table.ifExist(IDname) != True:
           return {
                'type': ir_int,
                'const': JudgeReg,
                'name': ir.Constant(ir_int, None)
            }
        Builder = self.builders[-1]
        TheItem = self.symbol_table.get(IDname)
        if TheItem != None:
            if self.WhetherNeedLoad:
                ReturnValue = Builder.load(TheItem["Name"])
                return {
                    "type" : TheItem["Type"],
                    "const" : JudgeReg,
                    "name" : ReturnValue,
                    "struct_name" : TheItem["StructName"] if "StructName" in TheItem else None
                }
            else:
                return {
                    "type" : TheItem["Type"],
                    "const" : JudgeReg,
                    "name" : TheItem["Name"],
                    "struct_name" : TheItem["StructName"] if "StructName" in TheItem else None
                }
        else:
            return {
                'type': ir_void,
                'const': JudgeReg,
                'name': ir.Constant(ir_void, None)
            }


    def visitItemINT(self, ctx:ToyCParser.ItemINTContext):
        JudgeReg = True
        return {
                'type': ir_int,
                'const': JudgeReg,
                'name': ir.Constant(ir_int, int(ctx.getText()))
        }

    def visitItemDOUBLE(self, ctx:ToyCParser.ItemDOUBLEContext):
        JudgeReg = True
        return {
                'type': ir_double,
                'const': JudgeReg,
                'name': ir.Constant(ir_double, float(ctx.getText()))
        }


    def visitItemCHAR(self, ctx:ToyCParser.ItemCHARContext):
        JudgeReg = True
        return {
                'type': ir_pointer,
                'const': JudgeReg,
                'name': ir.Constant(ir_pointer, ord(ctx.getText()[1]))
        }

    def visitItemSTRING(self, ctx:ToyCParser.ItemSTRINGContext):
        MarkIndex = self.n_string
        self.n_string += 1
        ProcessIndex = ctx.getText().replace('\\n', '\n')
        ProcessIndex = ProcessIndex[1:-1]
        ProcessIndex += '\0'
        Len = len(bytearray(ProcessIndex, 'utf-8'))
        JudgeReg = False
        RealReturnValue = ir.GlobalVariable(self.module, ir.ArrayType(ir_pointer, Len), ".str%d"%MarkIndex)
        RealReturnValue.global_constant = True
        RealReturnValue.initializer = ir.Constant(ir.ArrayType(ir_pointer, Len), bytearray(ProcessIndex, 'utf-8'))
        return {
                'type': ir.ArrayType(ir_pointer, Len),
                'const': JudgeReg,
                'name': RealReturnValue
        }
    
    #TODO: 
    def visitItemLIB(self, ctx:ToyCParser.ItemLIBContext):
        pass

    def toBoolean(self, ManipulateIndex, notFlag = True):
        Builder = self.builders[-1]
        if notFlag:
            OperationChar = '=='
        else:
            OperationChar = '!='
        if ManipulateIndex['type'] == ir_pointer or ManipulateIndex['type'] == ir_int:
            RealReturnValue = Builder.icmp_signed(OperationChar, ManipulateIndex['name'], ir.Constant(ManipulateIndex['type'], 0))
            return {
                    'tpye': ir_bool,
                    'const': False,
                    'name': RealReturnValue
            }
        elif ManipulateIndex['type'] == ir_double:
            RealReturnValue = Builder.fcmp_ordered(OperationChar, ManipulateIndex['name'], ir.Constant(ir_double, 0))
            return {
                    'tpye': ir_bool,
                    'const': False,
                    'name': RealReturnValue
            }
        return ManipulateIndex
    

    def save_to_file(self, filename):
        with open(filename, "w") as f:
            f.write(repr(self.module))

def generate(input_filename, output_filename):
    """
    将C代码文件转成IR代码文件
    :param input_filename: C代码文件
    :param output_filename: IR代码文件
    :return: 生成是否成功
    """
    lexer = ToyCLexer(FileStream(input_filename))
    stream = CommonTokenStream(lexer)
    
    parser = ToyCParser(stream)
    parser.removeErrorListeners()
    errorListener = syntaxErrorListener()
    parser.addErrorListener(errorListener)

    tree = parser.prog()
    generator = ToyCGenerator()
    generator.visit(tree)
    print(generator.module)
    generator.save_to_file(output_filename)