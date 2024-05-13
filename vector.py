def dot_product(matrix1, matrix2):
    # Error handling
    if len(matrix1[0]) != len(matrix2):
        raise ValueError("Number of columns in matrix1 must be equal to number of rows in matrix2")

    result = []
    for i in range(len(matrix1)):
        row = []
        for j in range(len(matrix2[0])):
            # Compute dot product for each element of the result matrix
            product = sum(matrix1[i][k] * matrix2[k][j] for k in range(len(matrix1[0])))
            row.append(product)
        result.append(row)
    return result

def dot_product_with_point(vector,matrix):
    return [sum(vector[j] * matrix[i][j] for j in range(len(vector))) for i in range(len(matrix))]