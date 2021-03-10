#walsh table generation
#generate chips for each node

#IDEA:
#<---------------------------------------------------------------------------->
#w1 = [+1]
#w2n = [[Wn,Wn],[Wn,bar(Wn)]]

#The number of sequences needs to be a power of 2
#for any k which is not a satisfies 2^m then k<2^n
#<---------------------------------------------------------------------------->

def walsh_code(nodes):
    n = 0
    while pow(2,n)<nodes:
        n = n + 1
    r=range(2**n)
    chips = [[int(bin(x&y),13)%2or-1for x in r]for y in r]
    return chips
        
#<---------------------------------------------------------------------------->

def cdmaEncoding(code):
    if code == "1":
        return 1
    if code == "0":
        return -1
    if code == "-":
        return 0

#<---------------------------------------------------------------------------->

def chipXdata(chip,data):
    newChip = []
    for i in range(len(chip)):
        newChip.append(chip[i]*data)
    return newChip

#<----------------------------------------------------------------------------->

import numpy as np

def addcIdI(cIdIList):
    sum = []
    i=0
    for i in range(len(cIdIList[0])):
        sum.append(0)
    
    j=0
    for j in range(len(cIdIList)):
        sum = np.add(sum,cIdIList[j])

    return sum

#<----------------------------------------------------------------------------->

def cdmaDecoding(sumcIdI,chip):
    
    codeSignal = int(np.sum(np.dot(sumcIdI,chip)))
    #print(codeSignal)
    if codeSignal != 0:
        if codeSignal<0:
            codeSignal=-1
        else:
            codeSignal=1
    #print(codeSignal)
    # Generate appropriate message
    if codeSignal==1:
        print("Received code: 1")
    if codeSignal==0:
        print("No code detected! The sender node is idle!")
    if codeSignal==-1:
        print("Received code: 0")
    
#<----------------------------------------------------------------------------->