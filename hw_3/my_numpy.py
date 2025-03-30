import numpy as np
from numpy.lib.mixins import NDArrayOperatorsMixin


# Примесь для записи объекта в файл и чтения из файла
class FileMixin:
    def _matrix_to_output_view(self):
        output = ''
        for row in self.data:
            output += ' '.join(map(str, row)) + '\n'
        return output

    def matrix_operation_to_file(file_path, func, matrix_1, matrix_2):
        with open(file_path, 'w', encoding='utf-8') as f:
            # 3.9 не поддерживает match, поэтому обычное ветвление
            if func == 'add':
                res = '1st matrix\n' + matrix_1._matrix_to_output_view() + '\n2nd matrix\n' + matrix_2._matrix_to_output_view() + '\n'
                add_matrix = matrix_1 + matrix_2
                res += 'add result:\n' + add_matrix._matrix_to_output_view()
            elif func == 'mul':
                res = '1st matrix\n' + matrix_1._matrix_to_output_view() + '\nScalar\n' + str(matrix_2) + '\n'
                mul_matrix = matrix_1 * matrix_2
                res += 'mul result:\n' + mul_matrix._matrix_to_output_view()
            elif func == 'matmul':
                res = '1st matrix\n' + matrix_1._matrix_to_output_view() + '\n2nd matrix\n' + matrix_2._matrix_to_output_view() + '\n'
                matmul_matrix = matrix_1 @ matrix_2
                res += 'matmul result:\n' + matmul_matrix._matrix_to_output_view()
            else:
                raise ValueError('Function must be "add", "mul", or "matmul"')
            f.write(res)

    def write_to_file(self, file_path):
        np.savetxt(file_path, self.data, delimiter=',', fmt='%d')


# Примесь для отображения в консоли
class DisplayMixin:
    def __str__(self):
        return f"Matrix:\n{self.data}"


# Основной класс (арифметические операции)
class MyNumpyMatrix(NDArrayOperatorsMixin, FileMixin, DisplayMixin):
    def __init__(self, data):
        self._data = np.array(data)

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = np.array(value)

    # Метод для поддержки арифметических операций
    def _binary_op(self, other, op):
        if isinstance(other, MyNumpyMatrix):
            other = other.data
        return MyNumpyMatrix(op(self.data, other))

    # Основные арифметические операции
    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        args = [x.data if isinstance(x, MyNumpyMatrix) else x for x in inputs]
        result = getattr(ufunc, method)(*args, **kwargs)
        if isinstance(result, np.ndarray):
            return MyNumpyMatrix(result)
        return result


if __name__ == '__main__':
    m1 = MyNumpyMatrix(np.random.randint(0, 10, (10, 10)))
    m2 = MyNumpyMatrix(np.random.randint(0, 10, (10, 10)))
    scalar = 4

    print('First matrix:\n', m1)
    print('Second matrix:\n', m2)

    add_matrix = m1 + m2
    mul_matrix = m1 * scalar
    matmul_matrix = m1 @ m2

    # Вывод в консоль
    print(f'Add: {add_matrix}')
    print(f'Mul: {mul_matrix}')
    print(f'Matmul: {matmul_matrix}')

    MyNumpyMatrix.matrix_operation_to_file('artifacts/3_2/matrix+.txt', 'add', m1, m2)
    MyNumpyMatrix.matrix_operation_to_file('artifacts/3_2/matrix-mul.txt', 'mul', m1, scalar)
    MyNumpyMatrix.matrix_operation_to_file('artifacts/3_2/matrix@.txt', 'matmul', m1, m2)