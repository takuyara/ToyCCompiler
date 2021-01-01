# Generated from ToyC.g4 by ANTLR 4.9
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .ToyCParser import ToyCParser
else:
    from ToyCParser import ToyCParser

# This class defines a complete listener for a parse tree produced by ToyCParser.
class ToyCListener(ParseTreeListener):

    # Enter a parse tree produced by ToyCParser#prog.
    def enterProg(self, ctx:ToyCParser.ProgContext):
        pass

    # Exit a parse tree produced by ToyCParser#prog.
    def exitProg(self, ctx:ToyCParser.ProgContext):
        pass


    # Enter a parse tree produced by ToyCParser#include.
    def enterInclude(self, ctx:ToyCParser.IncludeContext):
        pass

    # Exit a parse tree produced by ToyCParser#include.
    def exitInclude(self, ctx:ToyCParser.IncludeContext):
        pass


    # Enter a parse tree produced by ToyCParser#itemFunction.
    def enterItemFunction(self, ctx:ToyCParser.ItemFunctionContext):
        pass

    # Exit a parse tree produced by ToyCParser#itemFunction.
    def exitItemFunction(self, ctx:ToyCParser.ItemFunctionContext):
        pass


    # Enter a parse tree produced by ToyCParser#funcBody.
    def enterFuncBody(self, ctx:ToyCParser.FuncBodyContext):
        pass

    # Exit a parse tree produced by ToyCParser#funcBody.
    def exitFuncBody(self, ctx:ToyCParser.FuncBodyContext):
        pass


    # Enter a parse tree produced by ToyCParser#parameters.
    def enterParameters(self, ctx:ToyCParser.ParametersContext):
        pass

    # Exit a parse tree produced by ToyCParser#parameters.
    def exitParameters(self, ctx:ToyCParser.ParametersContext):
        pass


    # Enter a parse tree produced by ToyCParser#parameter.
    def enterParameter(self, ctx:ToyCParser.ParameterContext):
        pass

    # Exit a parse tree produced by ToyCParser#parameter.
    def exitParameter(self, ctx:ToyCParser.ParameterContext):
        pass


    # Enter a parse tree produced by ToyCParser#body.
    def enterBody(self, ctx:ToyCParser.BodyContext):
        pass

    # Exit a parse tree produced by ToyCParser#body.
    def exitBody(self, ctx:ToyCParser.BodyContext):
        pass


    # Enter a parse tree produced by ToyCParser#block.
    def enterBlock(self, ctx:ToyCParser.BlockContext):
        pass

    # Exit a parse tree produced by ToyCParser#block.
    def exitBlock(self, ctx:ToyCParser.BlockContext):
        pass


    # Enter a parse tree produced by ToyCParser#initBlock.
    def enterInitBlock(self, ctx:ToyCParser.InitBlockContext):
        pass

    # Exit a parse tree produced by ToyCParser#initBlock.
    def exitInitBlock(self, ctx:ToyCParser.InitBlockContext):
        pass


    # Enter a parse tree produced by ToyCParser#initArrBlock.
    def enterInitArrBlock(self, ctx:ToyCParser.InitArrBlockContext):
        pass

    # Exit a parse tree produced by ToyCParser#initArrBlock.
    def exitInitArrBlock(self, ctx:ToyCParser.InitArrBlockContext):
        pass


    # Enter a parse tree produced by ToyCParser#ifBlocks.
    def enterIfBlocks(self, ctx:ToyCParser.IfBlocksContext):
        pass

    # Exit a parse tree produced by ToyCParser#ifBlocks.
    def exitIfBlocks(self, ctx:ToyCParser.IfBlocksContext):
        pass


    # Enter a parse tree produced by ToyCParser#ifBlock.
    def enterIfBlock(self, ctx:ToyCParser.IfBlockContext):
        pass

    # Exit a parse tree produced by ToyCParser#ifBlock.
    def exitIfBlock(self, ctx:ToyCParser.IfBlockContext):
        pass


    # Enter a parse tree produced by ToyCParser#elifBlock.
    def enterElifBlock(self, ctx:ToyCParser.ElifBlockContext):
        pass

    # Exit a parse tree produced by ToyCParser#elifBlock.
    def exitElifBlock(self, ctx:ToyCParser.ElifBlockContext):
        pass


    # Enter a parse tree produced by ToyCParser#elseBlock.
    def enterElseBlock(self, ctx:ToyCParser.ElseBlockContext):
        pass

    # Exit a parse tree produced by ToyCParser#elseBlock.
    def exitElseBlock(self, ctx:ToyCParser.ElseBlockContext):
        pass


    # Enter a parse tree produced by ToyCParser#condition.
    def enterCondition(self, ctx:ToyCParser.ConditionContext):
        pass

    # Exit a parse tree produced by ToyCParser#condition.
    def exitCondition(self, ctx:ToyCParser.ConditionContext):
        pass


    # Enter a parse tree produced by ToyCParser#whileBlock.
    def enterWhileBlock(self, ctx:ToyCParser.WhileBlockContext):
        pass

    # Exit a parse tree produced by ToyCParser#whileBlock.
    def exitWhileBlock(self, ctx:ToyCParser.WhileBlockContext):
        pass


    # Enter a parse tree produced by ToyCParser#assignBlock.
    def enterAssignBlock(self, ctx:ToyCParser.AssignBlockContext):
        pass

    # Exit a parse tree produced by ToyCParser#assignBlock.
    def exitAssignBlock(self, ctx:ToyCParser.AssignBlockContext):
        pass


    # Enter a parse tree produced by ToyCParser#forBlock.
    def enterForBlock(self, ctx:ToyCParser.ForBlockContext):
        pass

    # Exit a parse tree produced by ToyCParser#forBlock.
    def exitForBlock(self, ctx:ToyCParser.ForBlockContext):
        pass


    # Enter a parse tree produced by ToyCParser#forExpr.
    def enterForExpr(self, ctx:ToyCParser.ForExprContext):
        pass

    # Exit a parse tree produced by ToyCParser#forExpr.
    def exitForExpr(self, ctx:ToyCParser.ForExprContext):
        pass


    # Enter a parse tree produced by ToyCParser#returnBlock.
    def enterReturnBlock(self, ctx:ToyCParser.ReturnBlockContext):
        pass

    # Exit a parse tree produced by ToyCParser#returnBlock.
    def exitReturnBlock(self, ctx:ToyCParser.ReturnBlockContext):
        pass


    # Enter a parse tree produced by ToyCParser#expr.
    def enterExpr(self, ctx:ToyCParser.ExprContext):
        pass

    # Exit a parse tree produced by ToyCParser#expr.
    def exitExpr(self, ctx:ToyCParser.ExprContext):
        pass


    # Enter a parse tree produced by ToyCParser#itemType.
    def enterItemType(self, ctx:ToyCParser.ItemTypeContext):
        pass

    # Exit a parse tree produced by ToyCParser#itemType.
    def exitItemType(self, ctx:ToyCParser.ItemTypeContext):
        pass


    # Enter a parse tree produced by ToyCParser#itemArray.
    def enterItemArray(self, ctx:ToyCParser.ItemArrayContext):
        pass

    # Exit a parse tree produced by ToyCParser#itemArray.
    def exitItemArray(self, ctx:ToyCParser.ItemArrayContext):
        pass


    # Enter a parse tree produced by ToyCParser#itemVoid.
    def enterItemVoid(self, ctx:ToyCParser.ItemVoidContext):
        pass

    # Exit a parse tree produced by ToyCParser#itemVoid.
    def exitItemVoid(self, ctx:ToyCParser.ItemVoidContext):
        pass


    # Enter a parse tree produced by ToyCParser#arrayItem.
    def enterArrayItem(self, ctx:ToyCParser.ArrayItemContext):
        pass

    # Exit a parse tree produced by ToyCParser#arrayItem.
    def exitArrayItem(self, ctx:ToyCParser.ArrayItemContext):
        pass


    # Enter a parse tree produced by ToyCParser#func.
    def enterFunc(self, ctx:ToyCParser.FuncContext):
        pass

    # Exit a parse tree produced by ToyCParser#func.
    def exitFunc(self, ctx:ToyCParser.FuncContext):
        pass


    # Enter a parse tree produced by ToyCParser#strlenFun.
    def enterStrlenFun(self, ctx:ToyCParser.StrlenFunContext):
        pass

    # Exit a parse tree produced by ToyCParser#strlenFun.
    def exitStrlenFun(self, ctx:ToyCParser.StrlenFunContext):
        pass


    # Enter a parse tree produced by ToyCParser#atoiFun.
    def enterAtoiFun(self, ctx:ToyCParser.AtoiFunContext):
        pass

    # Exit a parse tree produced by ToyCParser#atoiFun.
    def exitAtoiFun(self, ctx:ToyCParser.AtoiFunContext):
        pass


    # Enter a parse tree produced by ToyCParser#printfFun.
    def enterPrintfFun(self, ctx:ToyCParser.PrintfFunContext):
        pass

    # Exit a parse tree produced by ToyCParser#printfFun.
    def exitPrintfFun(self, ctx:ToyCParser.PrintfFunContext):
        pass


    # Enter a parse tree produced by ToyCParser#scanfFun.
    def enterScanfFun(self, ctx:ToyCParser.ScanfFunContext):
        pass

    # Exit a parse tree produced by ToyCParser#scanfFun.
    def exitScanfFun(self, ctx:ToyCParser.ScanfFunContext):
        pass


    # Enter a parse tree produced by ToyCParser#getsFun.
    def enterGetsFun(self, ctx:ToyCParser.GetsFunContext):
        pass

    # Exit a parse tree produced by ToyCParser#getsFun.
    def exitGetsFun(self, ctx:ToyCParser.GetsFunContext):
        pass


    # Enter a parse tree produced by ToyCParser#otherFun.
    def enterOtherFun(self, ctx:ToyCParser.OtherFunContext):
        pass

    # Exit a parse tree produced by ToyCParser#otherFun.
    def exitOtherFun(self, ctx:ToyCParser.OtherFunContext):
        pass


    # Enter a parse tree produced by ToyCParser#argument.
    def enterArgument(self, ctx:ToyCParser.ArgumentContext):
        pass

    # Exit a parse tree produced by ToyCParser#argument.
    def exitArgument(self, ctx:ToyCParser.ArgumentContext):
        pass


    # Enter a parse tree produced by ToyCParser#itemID.
    def enterItemID(self, ctx:ToyCParser.ItemIDContext):
        pass

    # Exit a parse tree produced by ToyCParser#itemID.
    def exitItemID(self, ctx:ToyCParser.ItemIDContext):
        pass


    # Enter a parse tree produced by ToyCParser#itemINT.
    def enterItemINT(self, ctx:ToyCParser.ItemINTContext):
        pass

    # Exit a parse tree produced by ToyCParser#itemINT.
    def exitItemINT(self, ctx:ToyCParser.ItemINTContext):
        pass


    # Enter a parse tree produced by ToyCParser#itemDOUBLE.
    def enterItemDOUBLE(self, ctx:ToyCParser.ItemDOUBLEContext):
        pass

    # Exit a parse tree produced by ToyCParser#itemDOUBLE.
    def exitItemDOUBLE(self, ctx:ToyCParser.ItemDOUBLEContext):
        pass


    # Enter a parse tree produced by ToyCParser#itemCHAR.
    def enterItemCHAR(self, ctx:ToyCParser.ItemCHARContext):
        pass

    # Exit a parse tree produced by ToyCParser#itemCHAR.
    def exitItemCHAR(self, ctx:ToyCParser.ItemCHARContext):
        pass


    # Enter a parse tree produced by ToyCParser#itemSTRING.
    def enterItemSTRING(self, ctx:ToyCParser.ItemSTRINGContext):
        pass

    # Exit a parse tree produced by ToyCParser#itemSTRING.
    def exitItemSTRING(self, ctx:ToyCParser.ItemSTRINGContext):
        pass


    # Enter a parse tree produced by ToyCParser#itemLIB.
    def enterItemLIB(self, ctx:ToyCParser.ItemLIBContext):
        pass

    # Exit a parse tree produced by ToyCParser#itemLIB.
    def exitItemLIB(self, ctx:ToyCParser.ItemLIBContext):
        pass



del ToyCParser