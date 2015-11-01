def knapsack():
    knapsack = [1]
    tmp = 0
    for i in range(100):
        for j in range(i):
            tmp += knapsack[j]
        tmp +=5
        knapsack.append(tmp)
    return knapsack


def ciphergen():
    f = open("a.txt","r")
    ptxt = f.read()
    ctxt = 0
    supsack = knapsack()
    for i in range(len(supsack)):
        print supsack[i]
    for i in range(len(ptxt)):
        if ptxt[i]== '1':
            ctxt += supsack[i]
    return ctxt


ciphertxt = ciphergen()

print ciphertxt
