from scipy.fft import fft, fftfreq
import matplotlib.pyplot as plt
from scipy.signal import decimate
from scipy.io import wavfile
import numpy as np

# Чтение файла со звуком
fs_voice, y_voice = wavfile.read('C:/Users/user/Downloads/ExpRecord.wav')

def quantize_signal(signal, num_bits):

    # Преобразование сигнала к float64 для избежания переполнения
    signal = signal.astype(np.float64)
    # Максимальное значение уровня квантования
    levels = 2 ** num_bits - 1
    # Нормализация и квантование
    signal_normalized = (signal - signal.min()) / (signal.max() - signal.min()) * levels
    signal_quantized = np.round(signal_normalized)
    # Возвращаем сигнал обратно к исходной шкале
    return signal_quantized / levels * (signal.max() - signal.min()) + signal.min()

# Функция для вычисления ошибки квантования
def quantization_error(original, quantized):
    return np.mean(np.abs(original - quantized))

# Квантование сигнала для 3, 4, 5 и 6 бит
bit_depths = [3, 4, 5, 6]
quantized_signals = [quantize_signal(y_voice, bits) for bits in bit_depths]

# Рассчитаем ошибки квантования
quantization_errors = [quantization_error(y_voice, q_signal) for q_signal in quantized_signals]

quantization_errors = [quantization_error(y_voice, q_signal) for q_signal in quantized_signals]

# Вывод результатов квантования и ошибок
for bits, error in zip(bit_depths, quantization_errors):
    print(f"Разрядность АЦП: {bits} бита, Средняя ошибка квантования: {error}")
