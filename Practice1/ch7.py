from scipy.interpolate import interp1d
import numpy as np
import matplotlib.pyplot as plt

f = 8  # частота
fs_high = 256  # увеличенная частота дискретизации
n_samples_high = fs_high
t = np.linspace(0, 1, 1000)  # временной интервал от 0 до 1 с шагом для графика
y = np.cos(2 * np.pi * f * t) + np.cos(8 * np.pi * f * t)  # исходный сигнал


t_discrete_high = np.linspace(0, 1, n_samples_high, endpoint=False)
y_discrete_high = np.cos(2 * np.pi * f * t_discrete_high) + np.cos(8 * np.pi * f * t_discrete_high)
t = np.clip(t, t_discrete_high.min(), t_discrete_high.max()) # обрезаем время, чтобы не превышало пределы диапазона

# Линейная интерполяция для восстановленного сигнала
f_interp_high = interp1d(t_discrete_high, y_discrete_high, kind='linear')
y_restored_high = f_interp_high(t)

# Визуализация исходного и восстановленного сигнала при высокой частоте дискретизации
plt.plot(t, y, label="Исходный сигнал")
plt.plot(t, y_restored_high, '--', label="Восстановленный сигнал с fs=256 Гц", alpha=1)
plt.legend()
plt.xlabel("Время (с)")
plt.ylabel("Амплитуда")
plt.grid(True)
plt.show()
