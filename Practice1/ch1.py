import numpy as np
import matplotlib.pyplot as plt

# Параметры сигнала
f = 8  # частота
t = np.linspace(0, 1, 1000)  # временной интервал от 0 до 1 с шагом для графика
y = np.cos(2 * np.pi * f * t) + np.cos(8 * np.pi * f * t)  # исходный сигнал

# Визуализация
plt.plot(t, y)
plt.title("Непрерывный сигнал")
plt.xlabel("Время (с)")
plt.ylabel("Амплитуда")
plt.grid(True)
plt.show()
