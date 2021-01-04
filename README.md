# ToyCCompiler



## 一、项目简述

Python语言实现的一款简易的C-to-LLVM的编译器。使用antlr自动生成lexer和parser，再使用visitor模式编写具体文法到LLVM IR的映射关系。



## 二、使用说明

### 1. 环境要求

+ Python >= 3.7.0

+ pipenv虚拟环境

+ llvm虚拟机

  PS：建议使用Linux系统进行安装，如Ubuntu/Centos，分别使用`apt`和`yum`即可直接安装。Mac系统可以使用：

  ```bash
  # Ubuntu
  apt-get install llvm
  
  # Centos
  yum install llvm
  
  # Mac
  brew install llvm
  ```

  并确认`lli`加入到了环境变量中。

### 2. 使用方式

```bash
# 进入python虚拟环境
pipenv shell

# 安装依赖包，目前仅antlr4-python3-runtime和llvmlite
pipenv install

# 编译c代码
python main.py examples/add.c

# 使用lli进行测试
lli examples/add.ll
```

### 3. 目录结构

```bash
├── LICENSE                   					# 证书           
├── Pipfile															# 虚拟环境配置
├── Pipfile.lock												# 虚拟环境lock文件
├── README.md														# 文档
├── ToyCError.py												# 错误类
├── ToyC.g4													    # ToyC的antlr语法
├── ToyC.interp													# antlr生成
├── ToyC.tokens													# antlr生成
├── ToyCLexer.interp										# antlr生成
├── ToyCLexer.tokens										# antlr生成
├── ToyCLexer.py												# antlr生成的Lexer
├── ToyCParser.py												# antlr生成的Parser
├── ToyCListener.py											# Listener模式
├── ToyCVisitor.py											# Visitor模式
├── ToyCSymbolTable.py									# 实现符号表
├── all_generator.py										# 语义分析具体实现，C到LLVM IR的转换，继承ToyCVisitor
├── examples														# 测试用C代码
│   ├── aba.c
│   ├── add.c
│   ├── array.c
│   ├── calc.c
│   ├── func.c
│   └── sort.c
└── main.py															# 主函数，会编译第一个参数的文件，并在其位置生成IR代码
```



## 三、实现方法与重难点简述







## 四、团队分工

|        |                                    |
| ------ | ---------------------------------- |
|        |                                    |
| 郑吉源 | all_generator部分实现，汇报PPT制作 |




