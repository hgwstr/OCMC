import random
import time
import matplotlib.pyplot as plt

def calculate_crc(data, generator):
    augmented_data = data + [0] * (len(generator) - 1)
    remainder = augmented_data[:]
    for i in range(len(data)):
        if remainder[i] == 1:
            for j in range(len(generator)):
                remainder[i + j] ^= generator[j]
    return remainder[-(len(generator) - 1):]

def check_data(data_with_crc, generator):
    remainder = data_with_crc[:]
    for i in range(len(data_with_crc) - len(generator) + 1):
        if remainder[i] == 1:
            for j in range(len(generator)):
                remainder[i + j] ^= generator[j]
    return all(bit == 0 for bit in remainder[-(len(generator) - 1):])

def generate_random_data(size):
    return [random.randint(0, 1) for _ in range(size)]

def test_variable_polynomial_lengths():
    times = []
    lengths = []
    data = generate_random_data(250)

    for length in range(4, 1001, 2):
        generator = [1] * length

        start_time = time.time()
        crc = calculate_crc(data, generator)
        data_with_crc = data + crc
        check_data(data_with_crc, generator)
        end_time = time.time()

        elapsed_time = (end_time - start_time) * 1e6
        times.append(elapsed_time)
        lengths.append(length)
        print(f"Polynomial length: {length}, Time: {elapsed_time:.2f} microseconds")

    plt.plot(lengths, times, marker='o')
    plt.xlabel("Polynomial Length")
    plt.ylabel("Computation Time (microseconds)")
    plt.title("CRC Computation Time vs Polynomial Length")
    plt.grid()
    plt.show()

if __name__ == "__main__":
    print("Testing variable polynomial lengths:")
    test_variable_polynomial_lengths()
