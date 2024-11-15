#include <iostream>
#include <vector>
#include <ctime>
#include <cstdlib>

#define DATA_SIZE 250

// Генерация случайных данных
void generate_random_data(std::vector<uint32_t> &data, size_t size) {
    data.clear();
    for (size_t i = 0; i < size; i++) {
        data.push_back(rand() % 2);
    }
}

// Имитация вычисления CRC (пример программного CRC-32, без аппаратного модуля)
uint32_t calculate_crc(const std::vector<uint32_t> &data) {
    uint32_t crc = 0xFFFFFFFF;  // Инициализация CRC
    for (size_t i = 0; i < data.size(); i++) {
        crc ^= data[i];
        for (int j = 0; j < 8; j++) {
            if (crc & 1)
                crc = (crc >> 1) ^ 0xEDB88320;  // Полином для CRC-32
            else
                crc >>= 1;
        }
    }
    return ~crc;  // Инверсия результата
}

// Проверка данных с помощью CRC
bool check_data(const std::vector<uint32_t> &data, uint32_t expected_crc) {
    uint32_t crc_value = calculate_crc(data);
    return crc_value == expected_crc;
}

// Тестирование переменной длины полинома с выводом на график
void test_variable_polynomial_lengths() {
    std::vector<uint32_t> data;
    generate_random_data(data, DATA_SIZE);

    std::vector<double> times;   // Время выполнения
    std::vector<int> lengths;    // Длина полинома

    std::cout << "Testing variable polynomial lengths:\n";

    for (size_t length = 4; length <= 1000; length += 2) {
        // В этом варианте полином меняется программно, но не аппаратно, так как мы на ПК

        clock_t start = clock();

        uint32_t crc_value = calculate_crc(data);
        bool is_valid = check_data(data, crc_value);

        clock_t end = clock();
        double elapsed_time = ((double)(end - start) / CLOCKS_PER_SEC) * 1e6;  // Время в микросекундах

        lengths.push_back(length);
        times.push_back(elapsed_time);

        std::cout << "Polynomial length: " << length
                  << ", Time: " << elapsed_time << " microseconds, CRC Valid: "
                  << (is_valid ? "Yes" : "No") << std::endl;
    }

}

int main() {
    srand(time(nullptr));  // Инициализация генератора случайных чисел
    test_variable_polynomial_lengths();
    return 0;
}
