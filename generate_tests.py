import math
import random

maxlen_x = [64,64,128,64,128,256,256,512,512,1024,1024]
maxlen_y = [64,128,128,256,256,256,512,512,1024,512,1024]

s1="ACTG"
s2="TACG"

for i in range(11):
    file_name = "New Test Cases/gen_input"+str(i)+".txt"
    f = open(file_name,"w")
    f.write(s1+"\n")
    c=4
    h=4
    str1 = ""
    str2 = ""
    j= int(math.log(maxlen_x[i]/4,2))
    k = int(math.log(maxlen_y[i] / 4, 2))
    for i in range(j):
        a=random.randrange(0,c)
        f.write(str(a)+"\n")
        c=2*c
    f.write(s2+"\n")
    for i in range(k):
        b = random.randrange(0,h)
        f.write(str(b)+"\n")
        h=2*h
