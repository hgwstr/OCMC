#include <iostream>
#include <vector>


using namespace std;


// Функция для вычисления CRC
vector<int> calculateCRC(const vector<int>& data, const vector<int>& generator) {
   vector<int> augmentedData = data;


   // Добавляем нули для расчета CRC
   for (int i = 0; i < generator.size() - 1; ++i) {
       augmentedData.push_back(0);
   }


   vector<int> remainder = augmentedData;
   for (int i = 0; i <= augmentedData.size() - generator.size(); ++i) {
       if (remainder[i] == 1) {
           for (int j = 0; j < generator.size(); ++j) {
               remainder[i + j] ^= generator[j];
           }
       }
   }


   // Возвращаем последние биты (остаток) как CRC
   return vector<int>(remainder.end() - (generator.size() - 1), remainder.end());
}


// Функция для проверки ошибки на приемной стороне
bool checkData(const vector<int>& dataWithCRC, const vector<int>& generator) {
   vector<int> remainder = dataWithCRC;
   for (int i = 0; i <= dataWithCRC.size() - generator.size(); ++i) {
       if (remainder[i] == 1) {
           for (int j = 0; j < generator.size(); ++j) {
               remainder[i + j] ^= generator[j];
           }
       }
   }


   // Если остаток содержит только нули, ошибок нет
   for (int i = dataWithCRC.size() - generator.size() + 1; i < dataWithCRC.size(); ++i) {
       if (remainder[i] != 0) return false;
   }
   return true;
}


void sendDataAndCheck(const vector<int>& data, const vector<int>& generator) {
   // Вычисляем CRC для данных
   vector<int> crc = calculateCRC(data, generator);


   // Формируем пакет данных + CRC
   vector<int> dataWithCRC = data;
   dataWithCRC.insert(dataWithCRC.end(), crc.begin(), crc.end());


   // Проверка на приемной стороне
   cout << "Data sent (with CRC): ";
   for (int bit : dataWithCRC) cout << bit;
   cout << endl;


   bool isErrorFree = checkData(dataWithCRC, generator);
   cout << "Error detection result: " << (isErrorFree ? "No errors detected" : "Errors detected") << endl;
}


vector<int> generateRandomData(int size) {
   vector<int> data(size);
   for (int i = 0; i < size; ++i) {
       data[i] = rand() % 2; // Заполнение случайными 0 и 1
   }
   return data;
}


void runExtendedTest(const vector<int>& generator) {
   srand(time(0));
   vector<int> data = generateRandomData(250);


   // Выполняем отправку и проверку данных длиной 250 бит
   sendDataAndCheck(data, generator);
}


void testErrorDetectionExtended(const vector<int>& data, const vector<int>& generator) {
   vector<int> crc = calculateCRC(data, generator);
   vector<int> dataWithCRC = generateRandomData(250);
   dataWithCRC.insert(dataWithCRC.end(), crc.begin(), crc.end()); // Пакет данных + CRC


   int detectedErrors = 0;
   int undetectedErrors = 0;


   for (int i = 0; i < dataWithCRC.size(); ++i) { // Проходим по всем 250 + CRC длины битам
       // Искажаем один бит
       dataWithCRC[i] ^= 1;


       // Проверка на приемной стороне
       if (checkData(dataWithCRC, generator)) {
           undetectedErrors++;
       } else {
           detectedErrors++;
       }


       // Восстанавливаем бит для следующей итерации
       dataWithCRC[i] ^= 1;
   }


   cout << "Detected errors: " << detectedErrors << endl;
   cout << "Undetected errors: " << undetectedErrors << endl;
}


int main() {
   // Исходные данные (пример для 28 бит)
   vector<int> data = {1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0};


   // Порождающий полином для варианта №8 (x^6 + x^5 + x^4 + x^3 + x^2 + x + 1)
   vector<int> generator = {0, 1, 1, 1, 1, 1, 1, 1};


   cout << "Testing 28-bit data:" << endl;
   sendDataAndCheck(data, generator);


   cout << "\nTesting 250-bit random data:" << endl;
   runExtendedTest(generator);


   cout << "\nError detection with bit alterations:" << endl;
   testErrorDetectionExtended(data, generator);


   return 0;
}
