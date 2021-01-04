#include <stdio.h>
int a[1000];
int n, i;
void sort(int l, int r){
	int i = l, j = r, x = a[l], t;
	while (i <= j){
		while (a[i] < x){ i = i + 1; }
		while (a[j] > x){ j = j - 1; }
		if (i <= j){
			t = a[i];
			a[i] = a[j];
			a[j] = t;
			i = i + 1;
			j = j - 1;
		}
	}
	if (l < j){ sort(l, j); }
	if (i < r){ sort(i, r); }
	return ;
}
int main(){
	printf("Input length: ");
	scanf("%d", &n);
	printf("Input array: ");
	for (i = 1; i <= n; i = i + 1){ scanf("%d", &a[i]); }
	sort(1, n);
	for (i = 1; i <= n; i = i + 1){ printf("%d ", a[i]); }
	printf("\n");
	return 0;
}

