'@author: Sagen Soren'
'@CNL'
'@file: Common Utility'
'@file-info: MemMsg.txt . . . @description: common workspace'
'@file-info: sent.txt . . . @description: sender side generated codeword transmitted to the receiver side'

'@file-description: Inter Process Communication support functions and utilities for program management'
#converts the codeword to k dataword of size n and store it to a file
def getDword(b,div):
    codeword = []
    for x in range(0,len(b),div):
        codeword.append(b[x:x+div])
        x = x + div
    
    with open('MemMsg.txt','w') as f:
        for info in range(0, len(codeword)):
            f.writelines(codeword[info]+'\n')
        
#get the full message in a file
def getFullMsg(filename):
    f = open(filename,'r')
    codeword = f.read()
    return codeword    

#read the datawords from file and append it to a list
def readMsg():
    f = open('MemMsg.txt','r')
    datawords = []
    for items in f:
        datawords.append(items.strip()) # removes the newlines
    return datawords


#write the values of list into sent.txt
def writeMsg(L):
    with open('sent.txt','w') as f:
        for i in range(0, len(L)):
            f.write(L[i])
    

#inject error to the codeword
def injectError():
    
    with open('sent.txt','r') as f:
        L = f.read()
    print("Size of the codeword[Size] " + str(len(L)))
    print("Choose type of error:\n1.Enter 1 for Bit Error\n2.Enter 2 for Burst Error")
    t = int(input())
    if t==1:
        print("Inject error at position[0,Size-1] : ")
        i = int(input())
        if L[i]=='0':
            L=L[:i]+'1'+L[i+1:]
        else:
            L=L[:i]+'0'+L[i+1:]

    elif t== 2:
        print("How many errors do you want to inject?")
        n = int(input())
        for x in range(n):
            print("Inject error at position[0,Size-1] : ")
            i = int(input())
            if L[i]=='0':
                L=L[:i]+'1'+L[i+1:]
            else:
                L=L[:i]+'0'+L[i+1:]

    else:
        print("No error injected!")

    writeMsg(L)

