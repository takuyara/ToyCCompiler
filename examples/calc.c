#include <stdio.h>
#include <string.h>

int main()
{
    char expression[2048];
    char operation[2048];
    int numStack[2048];
    int nowNum = -1, nowOp = -1, decimal = 1, length;
    int num = 0, i;
    printf("Please input expression: ");
    gets(expression);
    length = strlen(expression);
    for(i = length - 1; i >= 0; i = i - 1) 
    {
        expression[i + 1] = expression[i];
    }
    i = length + 1;
    expression[0] = '(';
    expression[length + 1] = ')';
    length = length + 2;
    while(i >= 0){
        if(expression[i] == '+')
        {
            while(nowOp >= 0 && ((operation[nowOp] == '*') || (operation[nowOp] == '/'))){
                if(operation[nowOp] == '*') {
                    numStack[nowNum - 1] = numStack[nowNum] * numStack[nowNum - 1];
                }
                else {
                    numStack[nowNum - 1] = numStack[nowNum] / numStack[nowNum - 1];
                }
                nowOp = nowOp - 1;
                nowNum = nowNum - 1;
            }
            nowOp = nowOp + 1;
            operation[nowOp] = '+';
            i = i - 1;
        }
        else if(expression[i] == '-')
        {
            while(nowOp >= 0 && ((operation[nowOp] == '*') || (operation[nowOp] == '/'))){
                if(operation[nowOp] == '*'){
                    numStack[nowNum - 1] = numStack[nowNum] * numStack[nowNum - 1];
                }
                else{
                    numStack[nowNum - 1] = numStack[nowNum] / numStack[nowNum - 1];
                }
                nowNum = nowNum - 1;
                nowOp = nowOp - 1;
            }
            nowOp = nowOp + 1;
            operation[nowOp] = '-';
            i = i - 1;
        }
        else if(expression[i] == '*')
        {
            nowOp = nowOp + 1;
            operation[nowOp] = '*';
            i = i - 1;
        }
        else if(expression[i] == '/')
        {
            nowOp = nowOp + 1;
            operation[nowOp] = '/';
            i = i - 1;
        }
        else if(expression[i] == ')'){
            nowOp = nowOp + 1;
            operation[nowOp] = ')';
            i = i - 1;
        }
        else if(expression[i] == '(')
        {
            while(operation[nowOp] != ')')
            {
                char OperatorGet = operation[nowOp];
                nowOp = nowOp - 1;
				if(OperatorGet == '+'){
                    numStack[nowNum - 1] = numStack[nowNum] + numStack[nowNum - 1];
                }
                else if(OperatorGet == '-'){
                    numStack[nowNum - 1] = numStack[nowNum] - numStack[nowNum - 1];
                }
                else if(OperatorGet == '/'){
                    numStack[nowNum - 1] = numStack[nowNum] / numStack[nowNum - 1];
                }
                else if(OperatorGet == '*'){
                    numStack[nowNum - 1] = numStack[nowNum] * numStack[nowNum - 1];
                }
                nowNum = nowNum - 1;
            }
            nowOp = nowOp - 1;
            i = i - 1;
        }
        else
        {
            num = 0;
            decimal = 1;
            while(i >= 0 && expression[i] <= '9' && expression[i] >= '0')
            {
                num = num + (expression[i] - '0') * decimal;
                decimal = decimal * 10;
                i = i - 1;
            }
            numStack[nowNum + 1] = num;
            nowNum = nowNum + 1;
        }
    }
    printf("Result=%d\n", numStack[0]);
    return 0;
}
