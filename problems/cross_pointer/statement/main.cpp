#include<iostream>
using namespace std;
const int MAXN = 1000;
const int MAXP = 1000;

int count_cross(int *ptrs[]) {
	// Implement your solution here
}

int main() {
	int arr[MAXN];
	int *ptrs[MAXP];
	int n, index;
	cin >> n;
	for(int i=0; i<n; i++) {
		cin >> index;
		ptrs[i] = &arr[index];
	}
	ptrs[n] = NULL;
	cout << count_cross(ptrs) << '\n';
}
