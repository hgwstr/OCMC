#include <iostream>
#include <cmath>
#include <iomanip>
#include <vector>


using namespace std;


const int REGISTER_SIZE = 5;


// Функция для сдвига регистра x
void shiftX(int x[REGISTER_SIZE]) {
   int8_t shiftedElement = (x[3] + x[4]) % 2;
   for (int i = REGISTER_SIZE - 1; i > 0; i--) {
       x[i] = x[i - 1];
   }
   x[0] = shiftedElement;
}


// Функция для сдвига регистра y
void shiftY(int y[REGISTER_SIZE]) {
   int8_t shiftedElement = (y[1] + y[4]) % 2;
   for (int i = REGISTER_SIZE - 1; i > 0; i--) {
       y[i] = y[i - 1];
   }
   y[0] = shiftedElement;
}


// Функция для генерации последовательности Голда
void goldSequence(int x[REGISTER_SIZE], int y[REGISTER_SIZE], int result[], int length) {
   for (int i = 0; i < length; i++) {
       result[i] = (x[4] + y[4]) % 2;
       shiftX(x);
       shiftY(y);
   }
}


// Циклический сдвиг элементов массива
void shiftElements(int a[], int length) {
   int8_t shiftedElement = a[length - 1];
   for (int i = length - 1; i > 0; i--) {
       a[i] = a[i - 1];
   }
   a[0] = shiftedElement;
}


// Функция для расчёта автокорреляции
void autocorrelation(int sequence[], int length, double result[]) {
   for (int i = 0; i <= length; i++) {
       int shiftedSequence[length];
       for (int j = 0; j < length; j++) {
           shiftedSequence[j] = sequence[j];
       }
       for (int k = 0; k < i; k++) {
           shiftElements(shiftedSequence, length);
       }
       double correlation = 0;
       for (int j = 0; j < length; j++) {
           correlation += sequence[j] * shiftedSequence[j];
       }
       double sumSqA = 0, sumSqB = 0;
       for (int j = 0; j < length; j++) {
           sumSqA += sequence[j] * sequence[j];
           sumSqB += shiftedSequence[j] * shiftedSequence[j];
       }
       result[i] = correlation / sqrt(sumSqA * sumSqB);
   }
}


// Функция для расчёта взаимной корреляции
int correlation(int x[], int y[], int length) {
   int sum = 0;
   for (int i = 0; i < length; i++) {
       sum += x[i] * y[i];
   }
   return sum;
}


// Функция для вывода таблицы автокорреляции
void printAutocorrelationTable(int sequence[], int length, double autocorr[]) {
  
   cout << endl;


   cout << "│Сдвиг│";
   for (int i = 1; i <= length; i++) {
       cout << setw(2) << i << "│";
   }
   cout << "      Автокорр.   │" << endl;


   int shifted_sequence[length];


   for (int shift = 0; shift <= length; shift++) {
       cout << "│" << setw(5) << shift << "│";


       for (int i = 0; i < length; i++) {
           shifted_sequence[i] = sequence[(i + shift) % length];
           cout << setw(2) << shifted_sequence[i] << "│";
       }


       cout << setw(17) << fixed << setprecision(3) << autocorr[shift] << " │" << endl;


   }


}


int main() {
   int registerX[REGISTER_SIZE] = {0, 1, 0, 0, 0}; // x = 8
   int registerY[REGISTER_SIZE] = {0, 1, 1, 1, 1}; // y = 15


   int registerX1[REGISTER_SIZE] = {0, 1, 0, 0, 1}; // x = 9
   int registerY1[REGISTER_SIZE] = {0, 1, 0, 1, 0}; // y = 10


   int length = pow(2, REGISTER_SIZE) - 1;
   int goldSeq1[length];
   int goldSeq2[length];
   goldSequence(registerX, registerY, goldSeq1, length);
   goldSequence(registerX1, registerY1, goldSeq2, length);


   cout << "\nПосл-сть Голда (0, 1, 0, 0, 0 и 0, 1, 1, 1, 1): ";
   for (int i = 0; i < length; i++) {
       cout << goldSeq1[i] << " ";
   }
   cout << endl;


   double autocorr1[length + 1];
   autocorrelation(goldSeq1, length, autocorr1);
   printAutocorrelationTable(goldSeq1, length, autocorr1);


   cout << "\nПосл-сть Голда (0, 1, 0, 0, 1 и 0, 1, 0, 1, 0): ";
   for (int i = 0; i < length; i++) {
       cout << goldSeq2[i] << " ";
   }
   cout << endl;


   double autocorr2[length + 1];
   autocorrelation(goldSeq2, length, autocorr2);
   printAutocorrelationTable(goldSeq2, length, autocorr2);


   cout << "\nКорреляция между первой и второй последовательностей: " << correlation(goldSeq1, goldSeq2, length) << endl;


   return 0;
}


