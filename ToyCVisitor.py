# Generated from ToyC.g4 by ANTLR 4.9
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .ToyCParser import ToyCParser
else:
    from ToyCParser import ToyCParser

# This class defines a complete generic visitor for a parse tree produced by ToyCParser.

class ToyCVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by ToyCParser#prog.
    def visitProg(self, ctx:ToyCParser.ProgContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyCParser#include.
    def visitInclude(self, ctx:ToyCParser.IncludeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyCParser#itemFunction.
    def visitItemFunction(self, ctx:ToyCParser.ItemFunctionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyCParser#funcBody.
    def visitFuncBody(self, ctx:ToyCParser.FuncBodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyCParser#parameters.
    def visitParameters(self, ctx:ToyCParser.ParametersContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyCParser#parameter.
    def visitParameter(self, ctx:ToyCParser.ParameterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyCParser#body.
    def visitBody(self, ctx:ToyCParser.BodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyCParser#block.
    def visitBlock(self, ctx:ToyCParser.BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyCParser#initBlock.
    def visitInitBlock(self, ctx:ToyCParser.InitBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyCParser#initArrBlock.
    def visitInitArrBlock(self, ctx:ToyCParser.InitArrBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyCParser#ifBlocks.
    def visitIfBlocks(self, ctx:ToyCParser.IfBlocksContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyCParser#ifBlock.
    def visitIfBlock(self, ctx:ToyCParser.IfBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyCParser#elifBlock.
    def visitElifBlock(self, ctx:ToyCParser.ElifBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyCParser#elseBlock.
    def visitElseBlock(self, ctx:ToyCParser.ElseBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyCParser#condition.
    def visitCondition(self, ctx:ToyCParser.ConditionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyCParser#whileBlock.
    def visitWhileBlock(self, ctx:ToyCParser.WhileBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyCParser#assignBlock.
    def visitAssignBlock(self, ctx:ToyCParser.AssignBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyCParser#forBlock.
    def visitForBlock(self, ctx:ToyCParser.ForBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyCParser#forExpr.
    def visitForExpr(self, ctx:ToyCParser.ForExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyCParser#returnBlock.
    def visitReturnBlock(self, ctx:ToyCParser.ReturnBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyCParser#expr.
    def visitExpr(self, ctx:ToyCParser.ExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyCParser#itemType.
    def visitItemType(self, ctx:ToyCParser.ItemTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyCParser#itemArray.
    def visitItemArray(self, ctx:ToyCParser.ItemArrayContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyCParser#itemVoid.
    def visitItemVoid(self, ctx:ToyCParser.ItemVoidContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyCParser#arrayItem.
    def visitArrayItem(self, ctx:ToyCParser.ArrayItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyCParser#func.
    def visitFunc(self, ctx:ToyCParser.FuncContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyCParser#strlenFun.
    def visitStrlenFun(self, ctx:ToyCParser.StrlenFunContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyCParser#atoiFun.
    def visitAtoiFun(self, ctx:ToyCParser.AtoiFunContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyCParser#printfFun.
    def visitPrintfFun(self, ctx:ToyCParser.PrintfFunContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyCParser#scanfFun.
    def visitScanfFun(self, ctx:ToyCParser.ScanfFunContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyCParser#getsFun.
    def visitGetsFun(self, ctx:ToyCParser.GetsFunContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyCParser#otherFun.
    def visitOtherFun(self, ctx:ToyCParser.OtherFunContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyCParser#argument.
    def visitArgument(self, ctx:ToyCParser.ArgumentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyCParser#itemID.
    def visitItemID(self, ctx:ToyCParser.ItemIDContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyCParser#itemINT.
    def visitItemINT(self, ctx:ToyCParser.ItemINTContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyCParser#itemDOUBLE.
    def visitItemDOUBLE(self, ctx:ToyCParser.ItemDOUBLEContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyCParser#itemCHAR.
    def visitItemCHAR(self, ctx:ToyCParser.ItemCHARContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyCParser#itemSTRING.
    def visitItemSTRING(self, ctx:ToyCParser.ItemSTRINGContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyCParser#itemLIB.
    def visitItemLIB(self, ctx:ToyCParser.ItemLIBContext):
        return self.visitChildren(ctx)



del ToyCParser