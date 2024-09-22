from scipy.io import wavfile

# Чтение файла со звуком
fs_voice, y_voice = wavfile.read('C:/Users/user/Downloads/ExpRecord.wav')

# Определение частоты дискретизации
duration = len(y_voice) / fs_voice
print(f"Частота дискретизации: {fs_voice} Гц")
print(f"Длительность записи: {duration} секунд")
