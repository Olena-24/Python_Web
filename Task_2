import time
from multiprocessing import Pool, cpu_count

def factorize(number):
    factors = []
    for i in range(1, number + 1):
        if number % i == 0:
            factors.append(i)
    return factors

def sync_factorize(numbers):
    return [factorize(n) for n in numbers]

# Тестирование синхронной версии
start_time = time.time()
a, b, c, d = sync_factorize([128, 255, 99999, 10651060])
end_time = time.time()

print(f"Sync version took: {end_time - start_time} seconds")

def parallel_factorize(numbers):
    with Pool(cpu_count()) as pool:
        return pool.map(factorize, numbers)

if __name__ == "__main__":


    # Тестирование многопроцессорной версии
    start_time = time.time()
    a, b, c, d = parallel_factorize([128, 255, 99999, 10651060])
    end_time = time.time()
    print(f"Parallel version took: {end_time - start_time} seconds")

    # Тестирование многопроцессорной версии
    start_time = time.time()
    a, b, c, d = parallel_factorize([128, 255, 99999, 10651060])
    end_time = time.time()

    print(f"Parallel version took: {end_time - start_time} seconds")
