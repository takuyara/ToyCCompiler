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
		return {"type": self.visit(ctx.getChild(0)), "name": ctx.getChild(1).getText()}
	
	def visitParameters(self, ctx: ToyCParser.ParametersContext):
		if ctx.getChildCount() == 0:
			return []
		params = []
		for i in range(0, ctx.getChildCount(), 2):
			params.append(self.visit(ctx.getChild(i)))
		return params

	def visitReturnBlock(self, ctx: ToyCParser.ReturnBlockContext):
		# returnBlock : 'return' (mINT|mID)? ';';
		if ctx.getChildCount() == 2:
			return_value = self.builders[-1].ret_void()
			return {"type": ir_void, "const": True, "name": return_value}
		index = self.visit(ctx.getChild(1))
		return_value = self.builder[-1].ret(index["name"])
		return {"type": ir_void, "const": True, "name": return_value}

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



	