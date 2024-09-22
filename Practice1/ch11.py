import matplotlib.pyplot as plt
from scipy.signal import decimate
from scipy.io import wavfile

# Чтение файла со звуком
fs_voice, y_voice = wavfile.read('C:/Users/user/Downloads/ExpRecord.wav')

# Прореживание сигнала (уменьшение частоты дискретизации в 10 раз)
y_voice_downsampled = decimate(y_voice, 10)

# Частота дискретизации после прореживания
fs_voice_downsampled = fs_voice // 10

# Визуализация исходного и прореженного сигнала
plt.figure(figsize=(12, 6))

# Исходный сигнал
plt.subplot(2, 1, 1)
plt.plot(y_voice[:40000])  # первые 5000 отсчетов для наглядности
plt.title("Исходный сигнал")
plt.xlabel("Отсчеты")
plt.ylabel("Амплитуда")

# Прореженный сигнал
plt.subplot(2, 1, 2)
plt.plot(y_voice_downsampled[:4000])  # первые 500 отсчетов для наглядности (в 10 раз меньше)
plt.title("Прореженный сигнал (уменьшена частота дискретизации в 10 раз)")
plt.xlabel("Отсчеты")
plt.ylabel("Амплитуда")

plt.tight_layout()
plt.show()

fs_voice_downsampled, len(y_voice_downsampled)
