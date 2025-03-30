import numpy as np

class Matrix:
    def __init__(self, matrix: np.ndarray):
        self.check_matrix(matrix)
        self.matrix = matrix

    @staticmethod
    def check_matrix(matr):
        if not isinstance(matr, np.ndarray):
            raise TypeError('Matrix must be a numpy array')
        if not np.issubdtype(matr.dtype, np.number):
            raise ValueError("The values in the matrix must be numbers.")

    # Сложение
    def __add__(self, other):
        if not isinstance(other, Matrix):
            raise TypeError("Operand must be an instance of Matrix")
        if self.matrix.shape != other.matrix.shape:
            raise ValueError("Matrix shapes do not match")

        result = np.empty_like(self.matrix)
        for i in range(self.matrix.shape[0]):  # row
            for j in range(self.matrix.shape[1]):  # col
                result[i][j] = self.matrix[i][j] + other.matrix[i][j]
        return Matrix(result)

    # Скалярное умножение
    def __mul__(self, scalar):
        if not np.issubdtype(type(scalar), np.number):
            raise ValueError("Scalar must be number.")

        result = self.matrix
        for i in range(result.shape[0]):  # row
            for j in range(result.shape[1]):  # col
                result[i][j] *= scalar
        return Matrix(result)

    # Покомпонентное умножение
    def __matmul__(self, other):
        if not isinstance(other, Matrix):
            raise TypeError("Operand must be an instance of Matrix")
        if self.matrix.shape != other.matrix.shape:
            raise ValueError("Matrix shapes do not match for element-wise multiplication")

        result = np.empty_like(self.matrix)
        for i in range(self.matrix.shape[0]):  # row
            for j in range(self.matrix.shape[1]):  # col
                result[i][j] = self.matrix[i][j] * other.matrix[i][j]
        return Matrix(result)

    def __str__(self):
        return self._matrix_to_output_view()

    def matrix_to_output_view(self):
        output = ''
        for row in self.matrix:
            output += ' '.join(map(str, row)) + '\n'
        return output

    def matrix_to_file(file_path, func, matrix_1, matrix_2):
        with open(file_path, 'w', encoding='utf-8') as f:
            # 3.9 не поддерживает match, поэтому обычное ветвление
            if func == 'add':
                res = '1st matrix\n' + matrix_1.matrix_to_output_view() + '\n2nd matrix\n' + matrix_2.matrix_to_output_view() + '\n'
                add_matrix = matrix_1 + matrix_2
                res += 'add result:\n' + add_matrix.matrix_to_output_view()
            elif func == 'mul':
                res = '1st matrix\n' + matrix_1.matrix_to_output_view() + '\nScalar\n' + str(matrix_2) + '\n'
                mul_matrix = matrix_1 * matrix_2
                res += 'mul result:\n' + mul_matrix.matrix_to_output_view()
            elif func == 'matmul':
                res = '1st matrix\n' + matrix_1.matrix_to_output_view() + '\n2nd matrix\n' + matrix_2.matrix_to_output_view() + '\n'
                matmul_matrix = matrix_1 @ matrix_2
                res += 'matmul result:\n' + matmul_matrix.matrix_to_output_view()
            else:
                raise ValueError('Function must be "add", "mul", or "matmul"')
            f.write(res)



if __name__ == '__main__':
    np.random.seed(0)
    matrix_1 = Matrix(np.random.randint(0, 10, (10, 10)))
    matrix_2 = Matrix(np.random.randint(0, 10, (10, 10)))
    Matrix.matrix_to_file('artifacts/3_1/matrix+.txt', 'add', matrix_1, matrix_2)
    Matrix.matrix_to_file('artifacts/3_1/matrix-mul.txt', 'mul', matrix_1, 4)
    Matrix.matrix_to_file('artifacts/3_1/matrix@.txt', 'matmul', matrix_1, matrix_2)