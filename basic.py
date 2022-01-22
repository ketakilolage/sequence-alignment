from __future__ import division
import time, os, psutil, sys


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


def alignment(X, Y):
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
    if i == 0 and j != 0:
        seq1.append(X[0:j])
        for p in range(j):
            seq2.append('_')
    if j == 0 and i != 0:
        seq2.append(Y[0:i])
        for p in range(i):
            seq1.append('_')
    seq1.reverse()
    seq2.reverse()
    return A, seq1, seq2


if __name__ == '__main__':
    start = time.time()
    s1, s2 = string_generator(sys.argv[1])
    A, seq1, seq2 = alignment(s1, s2)
    seq1S = ''.join(seq1)
    seq2S = ''.join(seq2)

    fileW = open('output.txt', 'w')
    if len(seq1S) > 50:
        fileW.write(seq1S[0:50] + ' ' + seq1S[len(seq1S) - 50:len(seq1S)])
    else:
        fileW.write(seq1S + ' ' + seq1S)    
    fileW.write('\n')
    if len(seq2S) > 50:
        fileW.write(seq2S[0:50] + ' ' + seq2S[len(seq2S) - 50:len(seq2S)])
    else:
        fileW.write(seq2S + ' ' + seq2S)    
    fileW.write('\n' + str(A[len(s2)][len(s1)]) + '\n')

    process = psutil.Process(os.getpid())

    end = time.time()
    fileW.write(str(end - start) + '\n')
    fileW.write(str(process.memory_info().rss / 1024.0))
    fileW.close()