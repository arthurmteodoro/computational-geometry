import sys

# algorithm for http://www.geeksforgeeks.org/printing-brackets-matrix-chain-multiplication-problem/
# algorithm for print best parenthesis in matrix multiplication

class HoldName:
    def __init__(self, name):
        self.name = name


def printParenthesis(i: int, j: int, n: int, backets, name: HoldName):
    if i == j:
        print(chr(name.name), end="")
        name.name += 1
        return

    print("(", end="")
    printParenthesis(i, backets[i][j], n, backets, name)
    printParenthesis(backets[i][j]+1, j, n, backets, name)
    print(")", end="")


def MatrixChainOrder(p, n):
    m = [[0 for x in range(n)] for x in range(n)]
    backets = [[0 for x in range(n)] for x in range(n)]

    for i in range(1, n):
        m[i][i] = 0

    # L is chain length.
    for L in range(2, n):
        for i in range(1, n - L + 1):
            j = i + L - 1
            m[i][j] = 9999999999
            for k in range(i, j):

                # q = cost/scalar multiplications
                q = m[i][k] + m[k + 1][j] + p[i - 1] * p[k] * p[j]
                if q < m[i][j]:
                    m[i][j] = q

                    backets[i][j] = k

    hold_name = HoldName(ord('A'))
    print("Optimal Parenthesization: ", end="")
    printParenthesis(1, n-1, n, backets, hold_name)
    print("\nOptimal Cost is: "+str(m[1][n-1]))


if __name__ == '__main__':
    arr = [40, 20, 30, 10, 30]
    MatrixChainOrder(arr, len(arr))
