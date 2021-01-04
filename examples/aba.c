#include <stdio.h>
char a[1000];
int len;
int check(){
	int i;
	for (i = 0; i < len; i = i + 1){
		if (a[i] != a[len - i - 1]){
			return 0;
		}
	}
	return 1;
}
int main(){
	int i;
	char tmpchar;
	printf("Input length: ");
	scanf("%d%", &len);
	printf("Input string: ");
	scanf("%c", &tmpchar);
	for (i = 0; i < len; i = i + 1){
		scanf("%c", &a[i]);
	}
	if (check() == 0){
		printf("Not palindrome\n");
	} else {
		printf("Palindrome\n");
	}
	return 0;
}

