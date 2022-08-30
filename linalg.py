def swap_row(M, i, j):
    M[i], M[j] = M[j], M[i]

def multiply_row(M, i, c):
    for j in range(len(M[0])):
        M[i][j] *= c

def combine_row(M, add, mul, c):
    for j in range(len(M[0])):
        M[add][j] += c * M[mul][j]

def gaussian_elimination(M):
    """gaussian elimination by row, ie, inferior diagonal becomes 0."""
    if len(M) == 0:
        return
    
    num_rows, num_cols = len(M), len(M[0])
    i, j = 0, 0

    while True:
        if i >= num_rows or j >= num_cols:
            break

        if M[i][j] == 0:
            row_nonzero = i

            while row_nonzero < num_rows and M[row_nonzero][j] == 0:
                row_nonzero += 1

            if row_nonzero == num_rows:
                j += 1
                continue

            swap_row(M, i, row_nonzero)

        for row in range(i+1, num_rows):
            if M[row][j] != 0:
                factor = - (M[row][j] / M[i][j])
                combine_row(M, row, i, factor)

        i, j = i+1, j+1

def count_pivots(M):
    """Count the number of pivots of a matrix.

    Recall that, if a matrix is in echelon form, then the number of
    pivots is the same as the dimension of the image of the matrix.
    """
    if len(M) == 0:
        return 0

    zeros = [0.0 for _ in range(len(M[0]))]
    dim = 0
    
    for i in range(len(M)):
        if M[i] != zeros:
            dim += 1

    return dim
