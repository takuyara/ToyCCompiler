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
		self.end_if = none

		# TODO: symbol table
		self.symbol_table = SymbolTable()

	def visitProg(self, ctx: ToyCParser.ProgContext):
		# prog :(include)* (initBlock|initArrBlock|mFunction)*;
		for i in range(ctx.getChildCount()):
			self.visit(ctx.getChild(i))

	def visitParam(self, ctx: ToyCParser.ParamContext):
		# param : mType mID;
		return {"type": self.visit(ctx.getChild(0)), "name": ctx.getChild(1).getText()}
	
	def visitParameters(self, ctx: ToyCParser.ParametersContext):
		# parameters : param (','param)* |;
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
		# returnBlock : 'return' (mINT|mID)? ';';
		if ctx.getChildCount() == 2:
			return_value = self.builders[-1].ret_void()
			return {"type": ir_void, "const": True, "name": return_value}
		index = self.visit(ctx.getChild(1))
		return_value = self.builder[-1].ret(index["name"])
		return {"type": ir_void, "const": True, "name": return_value}

	def visitFuncBody(self, ctx: ToyCParser.FuncBodyContext):
		# funcBody : body returnBlock;
		self.symbol_table.enter_scope()
		for i in range(ctx.getChildCount()):
			self.visit(ctx.getChild(i))
		self.symbol_table.quit_scope()

	def visitMFunction(self, ctx: ToyCParser.MFunctionContext):
		# mFunction : (mType|mVoid) mID '(' parameters ')' '{' funcBody '}';
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
		self.symbol_table.enter_scope()
		variables = {}
		for i in range(len(params)):
			current_param = params[i]
			variable_name = builder.alloca(current_param["type"])
			builder.store(ir_func.args[i], variable_name)
			current_variable = {
				"type": current_param["type"],
				"name": variable_name,
			}
			# TODO: Check
			res = self.symbol_table.add_item(current_param["name"], variable_name)
			if res["result"] != "success":
				raise CompileError(context = ctx, message = res["reason"])
		self.visit(ctx.getChild(6))
		self.current_func = ""
		self.blocks.pop()
		self.builders.pop()
		self.symbol_table.quit_scope()

	def visitPrintfFunc(self, ctx: ToyCParser.PrintfFuncContext):
		# printfFunc : 'printf' '(' (mSTRING | mID) (','expr)* ')';
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

	def visitScanfFunc(self, ctx: ToyCParser.ScanfFuncContext):
		# scanfFunc : 'scanf' '(' mSTRING (','('&')?(mID|arrayItem))* ')';
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
		for i in range(4, ctx.getChildCount() - 1, 2):
			offset = 1 if ctx.getChild(i).getText() == "&" else 0
			tmp = self.need_load
			self.need_load = offset == 0
			param = self.visit(ctx.getChild(i + offset))
			self.need_load = tmp
			args.append(param["name"])
			i += offset
		return_value_name = builder.call(ir_func, args)
		return {"type": ir_int, "name": return_value_name}

	def visitSelfDefinedFunc(self, ctx: ToyCParser.SelfDefinedFuncContext):
		# selfDefinedFunc : mID '('((argument|mID)(','(argument|mID))*)? ')';
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
