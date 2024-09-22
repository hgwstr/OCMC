from scipy.interpolate import interp1d
import numpy as np
import matplotlib.pyplot as plt

f = 8  # частота
fs = 64  # частота дискретизации
n_samples = fs  # число отсчетов за 1 секунду
t = np.linspace(0, 1, 1000)  # временной интервал от 0 до 1 с шагом для графика
y = np.cos(2 * np.pi * f * t) + np.cos(8 * np.pi * f * t)  # исходный сигнал

t_discrete = np.linspace(0, 1, n_samples, endpoint=False)
y_discrete = np.cos(2 * np.pi * f * t_discrete) + np.cos(8 * np.pi * f * t_discrete)
t = np.clip(t, t_discrete.min(), t_discrete.max()) # обрезаем время, чтобы не превышало пределы диапазона
# Линейная интерполяция
f_interp = interp1d(t_discrete, y_discrete, kind='linear')
y_restored = f_interp(t)

# Визуализация исходного и восстановленного сигнала
plt.plot(t, y, label="Исходный сигнал")
plt.plot(t, y_restored, '--', label="Восстановленный сигнал", alpha=1.0)
plt.legend()
plt.xlabel("Время (с)")
plt.ylabel("Амплитуда")
plt.grid(True)
plt.show()
