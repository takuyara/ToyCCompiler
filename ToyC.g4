grammar ToyC;

//------语法
prog :(include)* (initBlock|initArrBlock|itemFunction)*;
include : '#include' '<' itemLIB '>';

//函数
itemFunction : (itemType|itemVoid) itemID '(' parameters ')' '{' funcBody '}';

//函数体
funcBody : body returnBlock;

//参数
parameters : parameter (','parameter)* |;
parameter : itemType itemID;

//语句块
body : (block | func';')*;

//语句块
block : initBlock | initArrBlock | ifBlocks | forBlock | whileBlock | assignBlock | returnBlock;

//初始化
initBlock : (itemType) itemID ('=' expr)? (',' itemID ('=' expr)?)* ';';
initArrBlock : itemType itemID '[' itemINT ']'';'; 

//if
ifBlocks : ifBlock (elifBlock)* (elseBlock)?;
ifBlock : 'if' '('condition')' '{' body '}';
elifBlock : 'else' 'if' '(' condition ')' '{' body '}';
elseBlock : 'else' '{' body '}';
condition :  expr;

//while
whileBlock : 'while' '(' condition ')' '{' body '}';

//赋值
assignBlock : ((arrayItem|itemID) '=')+  expr ';';

//for
forBlock : 'for' '(' forExpr  ';' condition ';' forExpr ')' ('{' body '}'|';');
forExpr :  itemID '=' expr (',' forExpr)?|;

//return
returnBlock : 'return' (itemINT|itemID)? ';';

//表达式
expr : '(' expr ')'              								#EXP
    | op='!' expr      											#NEG
    | expr '&&' expr       										#AND
    | expr '||' expr											#OR
	| (op='-')? itemINT                                   		#INT
    | (op='-')? itemDOUBLE										#DOUBLE   
	| expr op=('+' | '-') expr									#ADDSUB
    | expr op=('*' | '/' | '%') expr							#MULDIV
    | expr op=('==' | '!=' | '<' | '<=' | '>' | '>=') expr      #EQUA                 
    | itemCHAR                									#CHAR
    | itemSTRING                   								#STRING
    | itemID 													#ID 
    | arrayItem  												#ARRAY
    | func                                                     	#FUNCTION
    ;

itemType : 'int'| 'double'| 'char'| 'string';
itemArray : itemID '[' itemINT ']'; 
itemVoid : 'void';
arrayItem : itemID '[' expr ']';

//函数
func : (strlenFun | atoiFun | printfFun | scanfFun | getsFun | otherFun);
strlenFun : 'strlen' '(' itemID ')';
atoiFun : 'atoi' '(' itemID ')' ;
printfFun : 'printf' '(' (itemSTRING | itemID) (','expr)* ')';
scanfFun : 'scanf' '(' itemSTRING (','('&')?(itemID|arrayItem))* ')';
getsFun : 'gets' '(' itemID ')';
otherFun : itemID '('((argument|itemID)(','(argument|itemID))*)? ')';

argument : itemINT | itemDOUBLE | itemCHAR | itemSTRING;

itemID : ID;
itemINT : INT;
itemDOUBLE : DOUBLE;
itemCHAR : CHAR;
itemSTRING : STRING;

//------词法

ID : [a-zA-Z_][0-9A-Za-z_]*;
INT : [0-9]+;
DOUBLE : [0-9]+'.'[0-9]+;
CHAR : '\''.'\'';
STRING : '"'.*?'"';
LIB : [a-zA-Z]+'.h'?;
Conjunction : '&&' | '||';
Operator : '!' | '+' | '-' | '*' | '/' | '==' | '!=' | '<' | '<=' | '>' | '>=';
UnaryOperator :  '&' | '*' | '+' | '-' | '~' | '!';
LineComment: '//'.*?'\r'?'\n'   -> skip;
BlockComment:  '/*'.*?'*/'  -> skip;
WS : [ \t\r\n]+ -> skip ; // skip spaces, tabs, newlines

