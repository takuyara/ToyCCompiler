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
    def ifGlobal(self):
        if len(self.Table) == 1:
            return True
        else:
            return False

#不写结构体时，以下是否需要？
'''
class Structure:
    def __init__(self):
        self.List = {}
    
    def AddItem(self, Name, MemberList, TypeList):
        
        描述：添加一个元素
        参数：名称，成员列表，类型列表
        返回：成功{"result":"success"}，失败{"result":"fail","reason":具体原因码}
        
        #todo:处理这个错误
        if Name in self.List:
            return False
        NewStruct = {}
        NewStruct["Members"] = MemberList
        NewStruct["Type"] = ir.LiteralStructType(TypeList)
        self.List[Name] = NewStruct
        return True

    def GetMemberType(self, Name, Member):
        
        描述：获取成员类型
        参数：结构体名称，结构体成员名
        返回：类型,不存在返回None
        
        if Name not in self.List:
            return None
        StructItem = self.List[Name]
        TheIndex = StructItem["Members"].index(Member)
        TheType = StructItem["Type"].elements[TheIndex]
        return TheType

    def GetMemberIndex(self, Name, Member):
        
        描述：获取成员编号
        参数：结构体名称，结构体成员名
        返回：类型,不存在返回None
        
        if Name not in self.List:
            return None
        StructItem = self.List[Name]["Members"]
        TheIndex = StructItem.index(Member)
        return TheIndex
'''