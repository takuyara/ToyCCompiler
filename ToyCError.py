# Pionniers du TJ, benissiez-moi par votre Esprits Saints!
class CompileError(Exception):
	def __init__(self, message, context):
		super().__init__()
		if context is not None:
			self.line = context.start.line
			self.column = context.start.column
		else:
			self.line = self.column = 0
		self.message = message
	def __str__(self):
		return "Compile error (%d, %d): " % (self.line, self.column) + self.message
