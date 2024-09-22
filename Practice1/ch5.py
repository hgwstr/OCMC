from scipy.fft import fft, fftfreq
import numpy as np
import matplotlib.pyplot as plt

f = 8  # частота
fs = 64  # частота дискретизации
n_samples = fs  # число отсчетов за 1 секунду
t_discrete = np.linspace(0, 1, n_samples, endpoint=False)
y_discrete = np.cos(2 * np.pi * f * t_discrete) + np.cos(8 * np.pi * f * t_discrete)

# Преобразование Фурье
Y = fft(y_discrete)
freqs = fftfreq(n_samples, 1 / fs)

# Построение амплитудного спектра
plt.plot(freqs[:n_samples // 2], np.abs(Y[:n_samples // 2]))  # отображаем только положительные частоты
plt.title("Амплитудный спектр сигнала")
plt.xlabel("Частота (Гц)")
plt.ylabel("Амплитуда")
plt.grid(True)
plt.show()
