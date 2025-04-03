import math
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import time
from functools import partial
import multiprocessing

def integrate_chunk(f, a, b, n_iter):
    acc = 0
    step = (b - a) / n_iter
    for i in range(n_iter):
        acc += f(a + i * step) * step
    return acc

def integrate(f, a, b, *, n_jobs=1, n_iter=10000000, executor_type="thread"):
    step = (b - a) / n_jobs
    ranges = [(a + i * step, a + (i + 1) * step) for i in range(n_jobs)]
    chunk_iter = n_iter // n_jobs  # Количество итераций на каждый подотрезок

    Executor = ThreadPoolExecutor if executor_type == "thread" else ProcessPoolExecutor

    with Executor(max_workers=n_jobs) as executor:
        results = executor.map(partial(integrate_chunk, f, n_iter=chunk_iter),
                               [r[0] for r in ranges], [r[1] for r in ranges])
    return sum(results)

if __name__ == "__main__":
    f = math.cos
    a = 0
    b = math.pi / 2
    n_iter = 10_000_000
    cpu_count = multiprocessing.cpu_count()

    print(f"CPU count: {cpu_count}")

    for executor_type in ["thread", "process"]:
        print(f"Using {executor_type.capitalize()}PoolExecutor:")
        for n_jobs in range(1, cpu_count * 2 + 1):
            start_time = time.time()
            result = integrate(f, a, b, n_jobs=n_jobs, n_iter=n_iter, executor_type=executor_type)
            elapsed_time = time.time() - start_time
            print(f"n_jobs={n_jobs}, result={result:.6f}, time={elapsed_time:.4f} seconds")
        print()