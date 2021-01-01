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

//表达式情形
expr : '(' expr ')'              
    | op='!' expr      
    | expr '&&' expr       
    | expr '||' expr	
	| (op='-')? itemINT                                   
    | (op='-')? itemDOUBLE   
	| expr op=('+' | '-') expr
    | expr op=('*' | '/' | '%') expr
    | expr op=('==' | '!=' | '<' | '<=' | '>' | '>=') expr                              
    | itemCHAR                
    | itemSTRING                   
    | itemID  
    | arrayItem  	
    | func                                                     
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
itemLIB : LIB;

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

