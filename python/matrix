"""
Matrix.py
A program to manipulate 2-D matrices

Author: Karsten Ladner
Date: 5/24/2018
"""


def print_matrix(matrix):
    '''
    print a 3x3 matrix using two nested loops

    matrix: a list of lists
    '''

    for row in matrix:
        for num in row:
            print("{0}\t".format(num), end="")
        print("\n")
    print("\n")


def add(m1, m2):
    '''
    add two matrices
    results are stored in m1

    m1: a list of lists that have items each
    m2: a list of lists that have items each
    '''

    for i in range(len(m1)):
        # access each row
        for j in range(len(m1[i])):
            # add both numbers
            m1[i][j] += m2[i][j]


def multiply(m1, m2):
    '''
    multiply matrix m1 by matrix m2

    m1: a list of lists
    m2: a list of lists
    mat: resulting matrix
    '''

    mat = list()
    for row_num in range(len(m1)):
        #iterate through every row of the first matrix

        current_row = list() # row to append the list
        
        for col in range(len(m2[row_num])):
            # iterate through every column of the active row

            cell = 0 # value to be stored in the cell

            num = 0 # counter variable
            while num < len(m1[row_num]):
                
                # the column is changing in the first matrix
                # the row is changing in the second matrix
                cell += m1[row_num][num] * m2[num][col]

                num += 1

            current_row.append(cell)
        mat.append(current_row)
    return mat


if __name__ == '__main__':

    m1 = [[1, 2, 3], [4, 5, 6]]
    m2 = [[7, 8], [9, 10], [11, 12]]

    '''
    mat = list()
    for i in range(3):
        # create a list of from comma-separated numbers
        row = input("Please list a comma-separated "
                + "row:").strip().split(",")
        # convert the type of the numbers to float
        row = [float(num) for num in row]
        # append the row to the list
        mat.append(row)
    '''
    print_matrix(m1)
    print_matrix(multiply(m1, m2))
