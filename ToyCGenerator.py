# Pionniers du TJ, benissiez-moi par votre Esprits Saints!
from llvmlite import ir
from llvmlite import binding as llvm

from ToyCSymbolTable import SymbolTable

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
		self.end_if = none

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
		return_value = self.builder[-1].ret(index["name"])
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
			param_types.append(params["type"])
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
			if not self.symbol_table.add(current_param["name"], variable_name):
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
			param_types = ir.FunctionType(int32, [ir.PointerType(ir_pointer)], var_arg = True)
			ir_func = ir.Function(self.module, param_types, name = "scanf")
			self.funcs["scanf"] = ir_func
		builder = self.builders[-1]
		zero = ir.Constant(ir_int, 0)
		params = self.visit(ctx.getChild(0))
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

	def visitOtherFun(self, ctx: ToyCParser.SelfDefinedFuncContext):
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
		for i in range(ctx.getChildCount())
			self.visit(ctx.getChild(i))

	def visitInitBlock(self, ctx: ToyCParser.InitBlockContext):
		# initBlock : (itemType) itemID ('=' expr)? (',' itemID ('=' expr)?)* ';';
		item_type = self.visit(ctx.getChild(0))
		i = 1
		while i < ctx.getChildCount:
			item_name = ctx.getChild().getText()
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
		if self.isGlobal():
			ir_variable = ir.GlobalVariable(self.module, ir.ArrayType(item_type, item_length), name = item_name)
			ir_variable.linkage = "internal"
		else:
			ir_variable = self.builder[-1].alloca(ir.ArrayType(item_type, item_length), name = item_name)
		variable = {"type": ir.ArrayType(item_type, item_length), "name": ir_variable}
		if not self.symbol_table.add(item_name, variable):
			raise CompileError(context = ctx, message = "Duplicate array name")

	def visitAssignBlock(self, ctx: ToyCParser.AssignBlockContext):
		# assignBlock : ((arrayItem|itemID) '=')+  expr ';';
		builder = self.builders[-1]
		item_id = ctx.getChild(0).getText()
		if '[' not in and not self.symbol_table.ifExist(item_id):
			raise CompileError("Undefined variable")
		right_value = self.visit(ctx.getChild(ctx.getChildCount() - 2))
		right_value = {"type": right_value["type"], "name": right_value["name"]}
		for i in range(0, ctx.getChildCount() - 2, 2):
			tmp = self.need_load
			self.need_load = False
			left_value = self.visit(ctx.getChild(i))
			self.need_load = tmp
			# TODO: Check if this is right
			value_for_this = self.convert(right_value, left_value["type"])
			builder.store(left_value["name"], value_for_this["name"])
			# TODO: Chekc if this is right
		return {"type": left_value["type"], "name": builder.load(left_value["name"])}

	def visitCondition(self, ctx: ToyCParser.ConditionBlockContext):
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
		if self.endif_block is not None:
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
		if not self.builders[-1].is_terminated:
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

	def visitElseBlock(self, ctx: ElseBlockContext):
		# elseBlock : 'else' '{' body '}';
		self.symbol_table.addLevel()
		self.visit(ctx.getChild(2))
		self.symbol_table.declineLevel()

	def visitWhileBlock(self, ctx: WhileBlockContext):
		self.symbol_table.addLevel()
		builder = self.builders[-1]
		condition_block = builder.append_basic_block()
		body = builder.append_basic_block()
		end_while = builder.append_basic_block()
		builder.branch(condition_block)
		self.__update_2b(condition_block)
		condition = self.visit(ctx.getChild(2))
		self.builders[-1].cbranch(condition["name"], body, end_while)
		self.__update_2b(body)
		self.visit(ctx.getChild(5))
		self.Builders[-1].branch(condition_block)
		self.__update_2b(end_while)
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
		self.builders[-1].store(expr_id["name"], item_id["name"])
		if ctx.getChildCount() > 3:
			self.visit(ctx.getChild(4))
