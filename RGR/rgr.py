import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq
from scipy.signal import butter, lfilter

fs = 1000

# 1. Ввод имени и фамилии
name = input("Введите имя латиницей: ")
surname = input("Введите фамилию латиницей: ")
full_name = name + " " + surname
print(f"Вы ввели: {full_name}")

# 2. Генерация битовой последовательности из ASCII-кодов
def text_to_bits(text):
    return [int(bit) for char in text for bit in f"{ord(char):08b}"]

bit_sequence = text_to_bits(full_name)
print(f"Битовая последовательность: {bit_sequence}")

plt.figure(figsize=(10, 2))
plt.plot(bit_sequence, drawstyle='steps-mid')
plt.title("Битовая последовательность")
plt.xlabel("Индекс бита")
plt.ylabel("Значение")
plt.grid()
plt.show()

# 3. Вычисление CRC
def crc_generate(data, poly, m):
    poly_bits = [int(bit) for bit in f"{poly:0{m+1}b}"]  # m+1 бит
    data = data + [0] * m
    for i in range(len(data) - m):
        if data[i] == 1:
            for j in range(m + 1):
                data[i + j] ^= poly_bits[j]
    return data[-m:]

poly = 0x7
m = 3
crc = crc_generate(bit_sequence, poly, m)
print(f"Сгенерированный CRC: {crc}")
bit_sequence_with_crc = bit_sequence + crc

# 4. Добавление стоп-слова
stop_word = [1, 1, 1, 1, 1, 1, 1, 1]  # Стоп-слово из пяти единиц
final_sequence = bit_sequence_with_crc + stop_word
print(f"Последовательность с CRC и стоп-словом: {final_sequence}")

plt.figure(figsize=(12, 2))
plt.plot(final_sequence, drawstyle='steps-mid')
plt.title("Последовательность с CRC и стоп-словом")
plt.xlabel("Индекс бита")
plt.ylabel("Значение")
plt.grid()
plt.show()

# 5. Преобразование в временные отсчёты
def bits_to_samples(bits, n):
    return [bit for bit in bits for _ in range(n)]

n = 10
time_samples = bits_to_samples(final_sequence, n)

plt.figure(figsize=(12, 2))
plt.plot(time_samples, drawstyle='steps-mid')
plt.title("Временные отсчёты сигнала")
plt.xlabel("Индекс отсчёта")
plt.ylabel("Значение")
plt.grid()
plt.show()

# 6. Создание нулевого массива и вставка сигнала
signal_length = 2 * len(time_samples)
signal = [0] * signal_length
insert_position = int(input(f"Введите позицию для вставки (0 - {signal_length - len(time_samples)}): "))
signal[insert_position:insert_position + len(time_samples)] = time_samples

plt.figure(figsize=(12, 2))
plt.plot(signal, drawstyle='steps-mid')
plt.title("Сигнал с вставленными данными")
plt.xlabel("Индекс отсчёта")
plt.ylabel("Значение")
plt.grid()
plt.show()

# 7. Добавление шума
sigma = float(input("Введите значение стандартного отклонения шума (\u03c3): "))
noise = np.random.normal(0, sigma, signal_length)
noisy_signal = [signal[i] + noise[i] for i in range(signal_length)]

plt.figure(figsize=(12, 4))
plt.plot(noisy_signal, label="Зашумленный сигнал")
plt.title("Зашумленный сигнал")
plt.xlabel("Индекс отсчёта")
plt.ylabel("Амплитуда")
plt.grid()
plt.legend()
plt.show()

# 8. Корреляционный приёмник
# 8.1 Фильтрация 
def butter_lowpass_filter(data, cutoff, fs, order=5):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    y = lfilter(b, a, data)
    return y

cutoff_freq = 0.3 * fs
filtered_signal = butter_lowpass_filter(noisy_signal, cutoff_freq, fs)

plt.figure(figsize=(12, 4))
plt.plot(filtered_signal, label="Отфильтрованный сигнал")
plt.title("Отфильтрованный сигнал")
plt.xlabel("Индекс отсчёта")
plt.ylabel("Амплитуда")
plt.grid()
plt.legend()
plt.show()

# 8.2 Синхронизация и поиск стоп-слова
def find_stop_word(signal, stop_word, n):
    stop_samples = bits_to_samples(stop_word, n)
    corr = np.correlate(signal, stop_samples, mode="valid")
    stop_start = np.argmax(corr)
    return stop_start

sync_start = find_stop_word(filtered_signal, stop_word, n)
print(f"Синхронизация начинается с индекса: {sync_start}")
trimmed_signal = filtered_signal[:sync_start]

plt.figure(figsize=(12, 4))
plt.plot(filtered_signal, label="Отфильтрованный сигнал")
plt.axvline(sync_start, color='red', linestyle='--', label="Стоп-слово")
plt.title("Синхронизация и обнаружение стоп-слова")
plt.xlabel("Индекс")
plt.ylabel("Амплитуда")
plt.grid()
plt.legend()
plt.show()

# 9. Разбор символов на основе N отсчётов
def decode_bits(signal, n, threshold):
    decoded_bits = []
    for i in range(0, len(signal), n):
        chunk = signal[i:i + n]
        avg = sum(chunk) / n
        decoded_bits.append(1 if avg > threshold else 0)
    return decoded_bits

threshold = 0.5
decoded_bits = decode_bits(trimmed_signal, n, threshold)
print(f"Декодированные биты: {decoded_bits}")

# 10. Удаление стоп-слова
if stop_word in decoded_bits:
    stop_index = decoded_bits.index(stop_word[0])
    decoded_bits = decoded_bits[:stop_index]

# 11. Проверка CRC
received_crc = decoded_bits[-m:]
data_without_crc = decoded_bits[:-m]

if len(data_without_crc[0:len(bit_sequence)]) % 8 != 0:
    print("Ошибка: длина данных без CRC не кратна 8!")

calculated_crc = crc_generate(data_without_crc, poly, m)

if received_crc == calculated_crc:
    print("Ошибок нет, CRC совпадает.")
else:
    print("Обнаружена ошибка в данных!")

# 12. Восстановление данных из ASCII
if received_crc == calculated_crc:
    def bits_to_text(bits):
        chars = [bits[i:i + 8] for i in range(0, len(bits), 8)]
        return ''.join([chr(int(''.join(map(str, char)), 2)) for char in chars])

    recovered_text = bits_to_text(data_without_crc[0:len(bit_sequence)])
    print(f"Восстановленный текст: {recovered_text}")
