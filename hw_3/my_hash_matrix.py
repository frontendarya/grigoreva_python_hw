from hw_3.matrix import Matrix
import numpy as np

class MatrixHashMixin:
    # Хэш-функция: суммируем произведения элементов матрицы на их индексы
    def __hash__(self):
        h = 0
        for i in range(len(self.data)):
            for j in range(len(self.data[0])):
                h += (i + 1) * (j + 1) * self.data[i][j]
        return h

class MyHashMatrix(MatrixHashMixin, Matrix):
    def __init__(self, data):
        super().__init__(data)
        self.data = data

    def __hash__(self):
        return super().__hash__()

    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        args = [x.data if isinstance(x, Matrix) else x for x in inputs]
        result = getattr(ufunc, method)(*args, **kwargs)
        if isinstance(result, np.ndarray):
            return MyHashMatrix(result)
        return result

    # Кэшированное произведение матриц
    def cached_matmul(self, other):
        cache = {}
        # Генерация ключа для кэша
        key = (self.__hash__(), other.__hash__())

        if key in cache:
            return cache[key]
        result = MyHashMatrix(self.data @ other.data)
        cache[key] = result
        return result

    def __repr__(self):
        return f"MyHashMatrix({self.data})"

    def write_to_file(self, file_path):
        np.savetxt(file_path, self.data, delimiter=',', fmt='%d')

if __name__ == '__main__':
    np.random.seed(10)
    A = MyHashMatrix(np.random.randint(0, 10, (10, 20)))
    B = MyHashMatrix(np.random.randint(0, 10, (20, 10)))
    C = MyHashMatrix(np.random.randint(0, 10, (10, 20)))
    D = MyHashMatrix(np.random.randint(0, 10, (20, 10)))

    # Проверка коллизий (hash(A) == hash(C)) and (A != C) and (B == D) and (A @ B != C @ D)
    assert A.__hash__() == C.__hash__(), 'Hash function causes collision!'
    assert B == D, 'Matrices B and D must be equal!'

    AB = A @ B
    CD = C @ D

    assert not np.array_equal(AB.data, CD.data)

    A.write_to_file('artifacts/3_3/A.txt')
    B.write_to_file('artifacts/3_3/B.txt')
    C.write_to_file('artifacts/3_3/C.txt')
    D.write_to_file('artifacts/3_3/D.txt')

    result = A.cached_matmul(B)
    result.write_to_file('artifacts/3_3/AB.txt')

    MyHashMatrix.matrix_operation_to_file('artifacts/3_3/A@B.txt', 'matmul', A, B)
    MyHashMatrix.matrix_operation_to_file('artifacts/3_3/CD.txt', 'matmul', C, D)

    with open('hash.txt', 'w') as f:
        f.write(f"hash(A @ B): {AB.__hash__()}\n")
        f.write(f"hash(C @ D): {CD.__hash__()}\n")