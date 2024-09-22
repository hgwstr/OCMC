import numpy as np
import matplotlib.pyplot as plt

f = 8  # частота
fs = 64  # частота дискретизации
n_samples = fs  # число отсчетов за 1 секунду
t_discrete = np.linspace(0, 1, n_samples, endpoint=False)
y_discrete = np.cos(2 * np.pi * f * t_discrete) + np.cos(8 * np.pi * f * t_discrete)

# Визуализация дискретного сигнала
plt.stem(t_discrete, y_discrete, 'r', markerfmt='ro', basefmt=" ")
plt.title("Оцифрованный сигнал (частота дискретизации = 64 Гц)")
plt.xlabel("Время (с)")
plt.ylabel("Амплитуда")
plt.grid(True)
plt.show()
