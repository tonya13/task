import multiprocessing
import sys

def read_matrix(filename):
    with open(filename, 'r') as f:
        matrix = []
        for line in f:
            line = line.strip()
            str_numbers = line.split()
            row = [float(num) for num in str_numbers]
            matrix.append(row)
    return matrix

def compute_and_write_element(args):
    index, A, B, filename, lock = args
    i, j = index
    res = 0
    N = len(A[0])
    for k in range(N):
        res += A[i][k] * B[k][j]
    line = f"{i} {j} {res}\n"
    with lock:
        with open(filename, 'a') as f:
            f.write(line)

def main():
    if len(sys.argv) != 3:
        sys.exit(1)

    matrix1_file = sys.argv[1]
    matrix2_file = sys.argv[2]

    A = read_matrix(matrix1_file)
    B = read_matrix(matrix2_file)

    if len(A[0]) != len(B):
        print("Матрицы не могут быть перемножены: число столбцов A не равно числу строк B")
        sys.exit(1)

    result_rows = len(A)
    result_cols = len(B[0])

    indices = []
    for i in range(result_rows):
        for j in range(result_cols):
            indices.append((i, j))

    num_processes = 4

    manager = multiprocessing.Manager()
    lock = manager.Lock()

    intermediate_file = 'intermediate_results.txt'

    open(intermediate_file, 'w').close()

    args = []
    for index in indices:
        args.append((index, A, B, intermediate_file, lock))

    with multiprocessing.Pool(processes=num_processes) as pool:
        pool.map(compute_and_write_element, args)

    result_matrix = []
    for i in range(result_rows):
        result_matrix.append([0] * result_cols)

    with open(intermediate_file, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            i_str, j_str, value_str = line.split()
            i = int(i_str)
            j = int(j_str)
            value = float(value_str)
            result_matrix[i][j] = value

    with open('result_matrix.txt', 'w') as f:
        for row in result_matrix:
            str_numbers = [str(num) for num in row]
            line = ' '.join(str_numbers) + '\n'
            f.write(line)

if __name__ == '__main__':
    main()