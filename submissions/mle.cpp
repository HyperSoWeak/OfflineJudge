#include <bits/stdc++.h>
using namespace std;
const int MN = 100000000;

long long x[MN];

int main() {
    for(int i = 0; i < MN; i++) {
        x[i] = i;
    }
    long long a, b;
    cin >> a >> b;
    cout << a + b << '\n';
}