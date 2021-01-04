//Pionniers du TJ, benissiez-moi par votre Esprits Saints!
#include <stdio.h>
int a[10000];
int n, i, sum;
int main(){
	scanf("%d", &n);
	/*
	i = 1;
	while (i <= n){
		scanf("%d", &a[i]);
		i = i + 1;
	}
	i = 1;
	sum = 0;
	while (i <= n){
		sum = sum + a[i];
		i = i + 1;
	}
	*/
	for (i = 1; i <= n; i = i + 1){ scanf("%d", &a[i]); }
	for (i = 1; i <= n; i = i + 1){ sum = sum + a[i]; }
	printf("sum=%d\n", sum);
	return 0;
}

