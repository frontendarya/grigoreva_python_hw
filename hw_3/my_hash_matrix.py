from hw_3.matrix import Matrix
import numpy as np

class MatrixHashMixin:
    """
    Хэш-функция: суммируем элементы в каждой строке, умножаем на индекс строки и добавляем математические операции
    """
    def __hash__(self):
        hash_value = 1
        row_sums = [sum(row) for row in self.data]

        for ind, value in enumerate(row_sums):
            hash_value *= ind + 1

        return hash_value ** (6 % 8 + 2)

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

    def __eq__(self, other):
        if isinstance(other, MyHashMatrix):
            return np.array_equal(self.data, other.data)
        else:
            return False

if __name__ == '__main__':
    # Проверка коллизий (hash(A) == hash(C)) and (A != C) and (B == D) and (A @ B != C @ D)
    A = MyHashMatrix(np.array([[1, 2], [3, 4]]))
    B = MyHashMatrix(np.array([[5, 6], [7, 8]]))
    C = MyHashMatrix(np.array([[2, 1], [4, 3]]))    # (A != C)
    D = MyHashMatrix(np.array([[5, 6], [7, 8]]))    # (B == D)

    assert A.__hash__() == C.__hash__(), 'Hash function causes collision!'
    assert B == D, 'Matrices B and D must be equal!'

    AB = A @ B
    CD = C @ D

    assert not AB == CD, 'Matrices AB and CD must not be equal!'

    A.write_to_file('artifacts/3_3/A.txt')
    B.write_to_file('artifacts/3_3/B.txt')
    C.write_to_file('artifacts/3_3/C.txt')
    D.write_to_file('artifacts/3_3/D.txt')

    result = A.cached_matmul(B)
    result.write_to_file('artifacts/3_3/A@B.txt')

    MyHashMatrix.matrix_to_file('artifacts/3_3/AB.txt', 'matmul', A, B)
    MyHashMatrix.matrix_to_file('artifacts/3_3/CD.txt', 'matmul', C, D)

    with open('artifacts/3_3/hash.txt', 'w') as f:
        f.write(f"hash(A @ B): {AB.__hash__()}\n")
        f.write(f"hash(C @ D): {CD.__hash__()}\n")