#include <iostream>
#include <cmath>
using namespace std;

// Функция для вычисления корреляции
double correlation(int a[], int b[], int N) {
    double result = 0;
    for (int i = 0; i < N; i++) {
        result += a[i] * b[i];
    }
    return result;
}

// Нормализованная корреляция
double normalized_correlation(int a[], int b[], int N) {
    double sum_a = 0, sum_b = 0, sum_ab = 0;
    
    for (int i = 0; i < N; i++) {
        sum_ab += a[i] * b[i];
        sum_a += a[i] * a[i];
        sum_b += b[i] * b[i];
    }
    
    return sum_ab / (sqrt(sum_a) * sqrt(sum_b));
}

int main() {
    const int N = 8;
    int a[N] = {8, 3, 7, 2, -2, -4, 1, 4};
    int b[N] = {4, 2, 5, -1, -3, -7, 2, 1};
    int c[N] = {-2, -1, 3, -6, 5, -1, 4, -1};
    
    cout << "Корреляция между a и b: " << correlation(a, b, N) << endl;
    cout << "Нормализованная корреляция между a и b: " << normalized_correlation(a, b, N) << endl;
    
    cout << "Корреляция между a и c: " << correlation(a, c, N) << endl;
    cout << "Нормализованная корреляция между a и c: " << normalized_correlation(a, c, N) << endl;
    
    return 0;
}
