from scipy.fft import fft, fftfreq
import matplotlib.pyplot as plt
from scipy.signal import decimate
from scipy.io import wavfile
import numpy as np

# Функция для нормализации и построения спектра
def plot_fft(signal, fs, title, pos, normalize=False, y_max=None, x_max=None):
    N = len(signal)  # Количество отсчетов
    T = 1 / fs       # Период дискретизации
    yf = fft(signal) # Преобразование Фурье
    xf = fftfreq(N, T)[:N // 2]  # Частоты для первой половины спектра
    A_spectr = 2 / N * np.abs(yf[:N // 2])  # Нормализация амплитудного спектра
    
    if normalize:
        A_spectr = A_spectr / 10  # Масштабирование амплитуд после прореживания

    # Построение графика
    plt.subplot(2, 1, pos)
    plt.plot(xf, A_spectr)
    plt.title(title)
    plt.xlabel('Частота (Гц)')
    plt.ylabel('Амплитуда')
    plt.grid(True)

    if y_max is not None:  # Если передан предел для оси Y
        plt.ylim(0, y_max)
    if x_max is not None:  # Если передан предел для оси X
        plt.xlim(0, x_max)

    # Дополнительный вывод информации о ширине спектра
    max_i = np.argmax(A_spectr)
    max_f = xf[max_i]
    f_min = xf[0]
    f_max = max_f
    width = f_max - f_min
    print(f"Ширина спектра для '{title}': {width:.2f} Гц")

# Чтение файла со звуком
fs_voice, y_voice = wavfile.read('C:/Users/user/Downloads/ExpRecord.wav')

# Прореживание сигнала (уменьшение частоты дискретизации в 10 раз)
y_voice_downsampled = decimate(y_voice, 10)

# Частота дискретизации после прореживания
fs_voice_downsampled = fs_voice // 10

# Визуализация амплитудных спектров
plt.figure(figsize=(12, 6))

# Определяем максимальные значения амплитуды и частоты для исходного сигнала
Y_voice = fft(y_voice)
A_spectr_voice = 2 / len(y_voice) * np.abs(Y_voice[:len(Y_voice) // 2])
y_max = np.max(A_spectr_voice)
freqs_voice = fftfreq(len(y_voice), 1 / fs_voice)
x_max = np.max(freqs_voice[:len(freqs_voice)//2])  # Максимальная частота

# Амплитудный спектр исходного сигнала
plot_fft(y_voice, fs_voice, "Амплитудный спектр исходного сигнала", 1, y_max=y_max, x_max=x_max)

# Амплитудный спектр прореженного сигнала (с масштабированием)
plot_fft(y_voice_downsampled, fs_voice_downsampled, "Амплитудный спектр прореженного сигнала", 2, normalize=True, y_max=y_max, x_max=x_max)

plt.tight_layout()
plt.show()
