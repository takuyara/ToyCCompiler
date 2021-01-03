from llvmlite import ir


class SymbolTable:
    
    def __init__(self):
        #table[i]是一个字典
        self.Table = [{}]
        self.CurrentLevel = 0  

    #从符号表中获取元素
    #input：元素的key
    #return：成功返回元素，失败返回None
    def get(self, item):
        level = self.CurrentLevel
        while level >= 0:
            ItemList = self.Table[level]
            if item in ItemList:
                return ItemList[item]
            level -= 1
        return None

    #向符号表中添加元素
    #input：添加的key，value
    #return：成功True,失败False
    def add(self, key, value):
        '''
        if key == "left":
            print(value)
            raise CompileError(None, "fuck")
        '''
        if key in self.Table[self.CurrentLevel]:
            return False
        self.Table[self.CurrentLevel][key] = value
        return True

    #判断元素是否在符号表里
    #input：元素的key
    #return：存在True，否则False
    def ifExist(self, item):
        i = self.CurrentLevel
        while i >= 0:
            if item in self.Table[i]:
                return True
            i -= 1
        return False

    #增加一个level
    def addLevel(self):
        self.CurrentLevel += 1
        self.Table.append({})

    #减少一个level
    def declineLevel(self):
        if self.CurrentLevel == 0:
            return
        self.Table.pop(-1)
        self.CurrentLevel -= 1
    
    #判断当前变量是否全局
    #return: 是True,不是False
    def isGlobal(self):
        if len(self.Table) == 1:
            return True
        else:
            return False
