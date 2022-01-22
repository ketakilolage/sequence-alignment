from __future__ import division
from math import inf
import time, os, psutil, sys

DELTA_E = 30
ALPHA = [[0, 110, 48, 94], [110, 0, 118, 48], [48, 118, 0, 110], [94, 48, 110, 0]]
INDEX_OF = {}
INDEX_OF["A"] = 0
INDEX_OF["C"] = 1
INDEX_OF["G"] = 2
INDEX_OF["T"] = 3


def Alignment(X, Y):
    delta = 30
    m, n = len(X), len(Y)
    indices = dict()
    indices['A'] = 0
    indices['C'] = 1
    indices['G'] = 2
    indices['T'] = 3
    alpha = [[0, 110, 48, 94], [110, 0, 118, 48], [48, 118, 0, 110], [94, 48, 110, 0]]

    A = [[0 for i in range(m + 1)] for j in range(n + 1)]
    for i in range(m + 1):
        A[0][i] = i * delta
    for i in range(n + 1):
        A[i][0] = i * delta
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            matchCost = alpha[indices[X[j - 1]]][indices[Y[i - 1]]] + A[i - 1][j - 1]
            xMismatchCost = delta + A[i - 1][j]
            yMismatchCost = delta + A[i][j - 1]
            A[i][j] = min(matchCost, xMismatchCost, yMismatchCost)

    seq1, seq2 = [], []
    i = n
    j = m
    while i > 0 and j > 0:
        if A[i][j] - alpha[indices[X[j - 1]]][indices[Y[i - 1]]] == A[i - 1][j - 1]:
            seq1.append(X[j - 1])
            seq2.append(Y[i - 1])
            # P.append((prefix + j-1, prefix + i-1))
            i -= 1
            j -= 1
        #            print('diag', seq1, seq2, i, j)
        elif A[i][j] - delta == A[i - 1][j]:
            seq1.append('_')
            seq2.append(Y[i - 1])
            i -= 1
        #            print('hori', seq1, seq2, i, j)
        else:
            seq1.append(X[j - 1])
            seq2.append('_')
            #            print('vert', seq1, seq2, i, j)
            j -= 1
    if i == 0 and j!=0:
        seq1.append(X[0:j])
        for p in range(j):
            seq2.append('_')
    if j == 0 and i!=0:
        seq2.append(Y[0:i])
        for p in range(i):
            seq1.append('_')
    seq1.reverse()
    seq2.reverse()
    return seq1, seq2, A


def string_generator(inputFile):
    file1 = open(inputFile, 'r')
    lines = file1.readlines()
    count = 0
    count1, count2 = 0, 0
    len1, len2 = 0, 0
    current_string = ""
    for line in lines:
        # print("Line{}: {}: {}".format(count, line.strip(), line.strip().isnumeric()))
        count = count + 1
        if not line.strip().isnumeric():
            if count == 1:
                current_string = line.strip()
                len1 = len(current_string)
            else:
                string1 = current_string
                count1 = count - 2
                current_string = line.strip()
                len2 = len(current_string)
            # print("Line{}: {}".format(count, line.strip()))
        else:
            s = current_string
            current_string = s[0:int(line.strip()) + 1] + s + s[int(line.strip()) + 1:len(s)]
    string2 = current_string
    count2 = count - 2 - count1
    if (2 ** count1) * len1 != len(string1) or (2 ** count2) * len2 != len(string2):
        os._exit(1)
    #    print("string 1 : {}".format(string1))
    #    print("string 2 : {}".format(string2))
    return string1, string2


def space_efficient_alignment(X, Y):
    # Array B[0...m,0...1]
    # Declare the dp array
    # print(ALPHA[INDEX_OF[X[0]]][INDEX_OF[Y[0]]])
    #    print(X, Y, "inside space_efficient_alignment")
    m = len(X)
    n = len(Y)
    B = [[0 for j in range(2)] for i in range(m + 1)]
    for i in range(m + 1):
        B[i][0] = i * DELTA_E
    # print("B with init", B)
    for j in range(1, n + 1):
        B[0][1] = j * DELTA_E
        for i in range(1, m + 1):
            # print(j, i)
            # print(ALPHA[INDEX_OF[X[i-1]]][INDEX_OF[Y[j-1]]] + B[i-1][0], "Alpha related")
            B[i][1] = min(ALPHA[INDEX_OF[X[i - 1]]][INDEX_OF[Y[j - 1]]] + B[i - 1][0],
                          DELTA_E + B[i - 1][1],
                          DELTA_E + B[i][0])
        for i in range(m + 1):
            B[i][0] = B[i][1]

    #    print("Last Value", B[m][1])
    return B


P = []
optValue = 0


def DivideAndConquer(X, Y):
    m = len(X)
    n = len(Y)
#    print(X, Y)
    global optValue, P
    if n == 0:
        P.append(([X], ['_' for i in range(len(X))]))
        optValue += DELTA_E * len(X)
        return

    if m <= 2 and n <= 2:
        ans1, ans2, opt_value = Alignment(X, Y)
        P.append((ans1, ans2))
        # print((ans1, ans2))
        optValue += opt_value[-1][-1]
        return
    space_efficient_alignment_values = space_efficient_alignment(X, Y[:n // 2])
    backward_space_efficient_alignment_values = space_efficient_alignment(X[::-1], Y[n // 2:][::-1])
    min_value = float(inf)
    min_index = -1

    # print(space_efficient_alignment_values)
    # print(backward_space_efficient_alignment_values)
    for i in range(0, m + 1):
        if min_value > space_efficient_alignment_values[i][-1] + backward_space_efficient_alignment_values[m - i][-1]:
            min_value = space_efficient_alignment_values[i][-1] + backward_space_efficient_alignment_values[m - i][-1]
            min_index = i
    #            print("mins", min_value, min_index, "---")
    #    print(min_index, n // 2)
    #    print(X[:min_index], Y[:n // 2], "<--- chopping this off")
    #    print(X[min_index:], Y[n // 2:], "<----- anther chopping happening")
    DivideAndConquer(X[:min_index], Y[:n // 2])
    # P.append((min_index, n//2, X[min_index], Y[n//2]))
    DivideAndConquer(X[min_index:], Y[n // 2:])


if __name__ == "__main__":
    start = time.time()
    s1, s2 = string_generator(sys.argv[1])
    DivideAndConquer(s1, s2)
    fileW = open('output.txt', 'w')

    seq1 = []
    seq2 = []
    attach = 0
    for x in P:
        for z in x:
            if attach == 0:
                seq1.append(''.join(z))
                attach = 1
            else:
                seq2.append(''.join(z))
                attach = 0

#    fileW.write(''.join(seq1) + '\n')
#    fileW.write(''.join(seq2) + '\n')
    seq1S = ''.join(seq1)
    seq2S = ''.join(seq2)
    if len(seq1S) > 50:
        fileW.write(seq1S[0:50] + ' ' + seq1S[len(seq1S) - 50:len(seq1S)])
    else:
        fileW.write(seq1S + ' ' + seq1S)    
    fileW.write('\n')
    if len(seq2S) > 50:
        fileW.write(seq2S[0:50] + ' ' + seq2S[len(seq2S) - 50:len(seq2S)])
    else:
        fileW.write(seq2S + ' ' + seq2S)    
    fileW.write('\n' + str(optValue) + '\n')
    process = psutil.Process(os.getpid())

    end = time.time()
    fileW.write(str(end - start) + '\n')
    fileW.write(str(process.memory_info().rss / 1024.0))
    fileW.close()