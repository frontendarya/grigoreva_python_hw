import time
from threading import Thread
from multiprocessing import Process

# Рекурсивное вычисление числа Фибоначчи
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

# Функция для замера времени выполнения синхронного подхода
def run_synchronously(n, repetitions):
    start_time = time.time()
    for _ in range(repetitions):
        fibonacci(n)
    end_time = time.time()
    print(f"Synchronous execution: {end_time - start_time:.2f} s")

# Функция для запуска потоков
def run_with_threads(n, repetitions):
    threads = []
    start_time = time.time()
    for _ in range(repetitions):
        thread = Thread(target=fibonacci, args=(n,))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
    end_time = time.time()
    print(f"Execution with threads: {end_time - start_time:.2f} s")

# Функция для запуска процессов
def run_with_processes(n, repetitions):
    processes = []
    start_time = time.time()
    for _ in range(repetitions):
        process = Process(target=fibonacci, args=(n,))
        processes.append(process)
        process.start()
    for process in processes:
        process.join()
    end_time = time.time()
    print(f"Execution with processes: {end_time - start_time:.2f} s")

if __name__ == "__main__":
    n = 30
    repetitions = 10

    run_synchronously(n, repetitions)
    run_with_threads(n, repetitions)
    run_with_processes(n, repetitions)