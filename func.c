#include <stdio.h>
int x;
int sqr(int x){
	int res = x * x;
	return res;
}
int main(){
	x = 10;
	printf("%d\n", sqr(x));
	return 0;
}
