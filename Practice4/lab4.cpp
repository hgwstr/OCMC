#include <iostream>
#include <vector>
#include <iomanip>
#include <cmath>

// Функция для генерации последовательности Голда
std::vector<int> generateGoldSequence(std::vector<int> x, std::vector<int> y, int length) {
    std::vector<int> gold_sequence;
    for (int i = 0; i < length; ++i) {
        int new_bit_x = x[4] ^ x[2]; // XOR элементов 5 и 3
        int new_bit_y = y[4] ^ y[2]; // XOR элементов 5 и 3
        gold_sequence.push_back(x[4] ^ y[4]); // Голд последовательность как XOR выходов двух регистров

        // Обновляем регистры
        for (int j = 4; j > 0; --j) {
            x[j] = x[j - 1];
            y[j] = y[j - 1];
        }
        x[0] = new_bit_x;
        y[0] = new_bit_y;
    }
    return gold_sequence;
}

// Функция для циклического сдвига вектора на одну позицию вправо
std::vector<int> cyclicShift(const std::vector<int>& sequence) {
    std::vector<int> shifted_sequence = sequence;
    int last_bit = shifted_sequence.back();
    shifted_sequence.pop_back();
    shifted_sequence.insert(shifted_sequence.begin(), last_bit);
    return shifted_sequence;
}

// Функция для расчёта корреляции между двумя последовательностями
int calculateCorrelation(const std::vector<int>& seq1, const std::vector<int>& seq2) {
    int correlation = 0;
    for (size_t i = 0; i < seq1.size(); ++i) {
        correlation += (seq1[i] == seq2[i]) ? 1 : -1;
    }
    return correlation;
}

// Сбалансированность
bool checkBalance(const std::vector<int>& sequence) {
    int count_ones = 0;
    for (int bit : sequence) {
        if (bit == 1) count_ones++;
    }
    int count_zeros = sequence.size() - count_ones;
    return std::abs(count_ones - count_zeros) <= 1;
}

// Проверка на m-последовательность
bool isMSequence(const std::vector<int>& sequence) {
    if (sequence.size() != 31) return false; // Проверка длины последовательности 2^n - 1
    return checkBalance(sequence); // Дополнительные критерии для m-последовательности
}

// Вычисление автокорреляции с проверкой на m-последовательность
void calculateAutocorrelationAndCheckMSequence(const std::vector<int>& sequence, int sequence_length) {
    std::vector<int> shifted_sequence = sequence;
    std::cout << "Сдвиг|                                                               |Корреляция| m-последовательность\n";
    for (int shift = 0; shift < sequence_length; ++shift) {
        int corr = calculateCorrelation(sequence, shifted_sequence);
        
        std::cout << std::setw(4) << shift << " | ";
        for (int bit : shifted_sequence) {
            std::cout << bit << " ";
        }
        std::cout << "| " << corr << "/" << sequence_length;
        
        // Проверка на m-последовательность
        bool is_m_sequence = isMSequence(shifted_sequence);
        std::cout << "    | " << (is_m_sequence ? "Да" : "Нет") << "\n";
        
        shifted_sequence = cyclicShift(shifted_sequence);
    }
}

// Функция для взаимной корреляции
int correlation(const std::vector<int>& seq1, const std::vector<int>& seq2, int length) {
    int sum = 0;
    for (int i = 0; i < length; i++) {
        sum += seq1[i] * seq2[i];
    }
    return sum;
}

int main() {
    int sequence_length = 31;

    // Первая последовательность Голда (x = 8, y = 15)
    std::vector<int> x1 = {0, 1, 0, 0, 0}; // 01000
    std::vector<int> y1 = {0, 1, 1, 1, 1}; // 01111
    std::vector<int> gold_sequence1 = generateGoldSequence(x1, y1, sequence_length);

    // Вторая последовательность Голда (x = 9, y = 10)
    std::vector<int> x2 = {0, 1, 0, 0, 1}; // 01001
    std::vector<int> y2 = {0, 1, 0, 1, 0}; // 01010
    std::vector<int> gold_sequence2 = generateGoldSequence(x2, y2, sequence_length);

    // Вывод первой последовательности
    std::cout << "Первая последовательность Голда (x=8, y=15):\n";
    for (int bit : gold_sequence1) {
        std::cout << bit << " ";
    }
    std::cout << "\n\n";

    // Вывод второй последовательности
    std::cout << "Вторая последовательность Голда (x=9, y=10):\n";
    for (int bit : gold_sequence2) {
        std::cout << bit << " ";
    }
    std::cout << "\n\n";

    // Сбалансированность
    std::cout << "Сбалансированность: ";
    if (checkBalance(gold_sequence1)) {
        std::cout << "выполнено\n";
    } else {
        std::cout << "не выполнено\n";
    }

    // Автокорреляция и проверка на m-последовательность
    std::cout << "\nАвтокорреляция первой последовательности с проверкой на m-последовательность:\n";
    calculateAutocorrelationAndCheckMSequence(gold_sequence1, sequence_length);

    // Взаимная корреляция между первой и второй последовательностями
    int cross_correlation = correlation(gold_sequence1, gold_sequence2, sequence_length);
    std::cout << "\nВзаимная корреляция между первой и второй последовательностями: ";
    std::cout << cross_correlation << "/" << sequence_length << std::endl;

    return 0;
}
