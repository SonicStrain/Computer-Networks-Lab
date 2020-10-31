'@author: Sagen Soren'
'@CNL'
'@file: Scheme Library'
#library VRC, LRC , CheckSum , CRC

#vertical redundancy check
'@start of VRC___________________________________________________________________________________'

'__function for VRC : VRCutil(list L) && VRCcheck(list L)'

def VRC(dataword):
    oneCount = 0
    for ones in dataword:
        if ones == '1':
            oneCount = oneCount + 1
        
    if oneCount%2 == 0:
        dataword = dataword + '0' #even parity
    else:
        dataword = dataword + '1' #odd parity
    return dataword

'@function: utility for VRC'
'@type: Sender Side'

def VRCutil(L):
    for i in range(len(L)):
        L[i] = VRC(L[i])
    return L

#check the dataword if it is valid or not

def VRCparity(dataword):
    oneCount = 0
    for ones in dataword:
        if ones == '1':
            oneCount = oneCount + 1
        
    if oneCount%2 == 0:
        print("Data Accepted! >> dataword: "+ dataword[0:4] + " PASS!")
    else:
        
        print("Corrupted Data received: " + dataword[0:4] + " Parity bit: " + dataword[4] + " FAIL!")
    


'@function: Test the received codeword'
'@type: Receiver Side'
def VRCcheck(L):
    for i in range(len(L)):
        VRCparity(L[i])
    

'@end of VRC___________________________________________________________________________________'

#Longitudinal Redundancy Check

'@start of LRC_________________________________________________________________________________'

'__function for LRC : LRCutil(list L) && LRCcheck(list L)'

def LRC(L):
    rbit = []
    oneCount = 0
    for i in range(len(L[0])):
        oneCount = 0
        for j in range(len(L)):
            if L[j][i] == '1':
                oneCount += 1
        #print(oneCount)    
        if oneCount%2 == 0:
            rbit.append('0')
        else:
            rbit.append('1')
        
    return rbit

'@function: utility for LRC'
'@type: Sender Side'

def LRCutil(L):
    rbits = LRC(L)
    separator = ''
    rb = separator.join(rbits)
    #print(rb)
    L.append(rb)
    return L

#to validate LRC at the receiver side

'@function: validator for LRC'
'@type: Receiver Side'

def LRCcheck(L):
    oneCount = 0
    flag = 0
    for i in range(len(L[0])):
        oneCount = 0
        for j in range(len(L)):
            if L[j][i] == '1':
                oneCount += 1
        #print(oneCount)    
        if oneCount%2 == 0:
            #if even parity data is valid
            print("data at column " + str(i) + " accepted!")
        else:
            print("corrupted data at column " + str(i) + " rejected!")
            flag =1
        
    if flag == 1:
        print("\n>> Error Detected in the data!\n")
        print("\nFAIL!")
    else:
        print("\n>> No error detected! Data accepted!\n")
        print("\nPASS!")

'@end of LRC_________________________________________________________________________________'

#checkSum

'@start of CheckSum___________________________________________________________________________'

'__function for CheckSum : CSutil(list L,dataword-size div) && CScheck(list L,dataword-size div)'

#function to add two binary numbers for checkSum

def binSum(bn1,bn2,div):
    
    s1=bin(int(bn1,2)+int(bn2,2))
    
    if len(s1)==div+3:
        carry='1'
        s2=s1[3:]
        #print(s2)
        s1= binSum(s2,carry,div)
        return s1
    else:
        return s1[2:]

#get the checkSum
def CheckSum(L,div):
    
    temp = L[0]

    for i in range(len(L)-1):
        temp = binSum(temp,L[i+1],div)
        if len(temp) != div:
            for i in range(div-len(temp)):
                temp = '0' + temp
        #print(temp)
    
    checkSum = temp
    
    #print(checkSum)

    #make 1's complement
    for i in range(len(checkSum)):
        if checkSum[i]=='0':
            checkSum=checkSum[:i]+'1'+checkSum[i+1:]
        else:
            checkSum=checkSum[:i]+'0'+checkSum[i+1:]
    return checkSum

'@function: utility for CheckSum'
'@type: Sender Side'

def CSutil(L,div):
    csum = CheckSum(L,div)
    L.append(csum)
    return L

'@function: validator for CheckSum'
'@type: Receiver Side'

def CScheck(L,div):
    csum = CheckSum(L,div)
    flag = 0
    for i in range(len(csum)):
        if csum[i] == '1':
            flag = 1
            break
    
    if flag == 0:
        print(">> checksum : " + csum)
        print("\n>> Data accepted! No error found!")
        print("\nPASS!")
    else:
        print(">> checksum : " + csum)
        print("\n>> Error Detected in data!")
        print("\nFAIL!")

'@end of CheckSum______________________________________________________________________________'

#cyclic redundancy check

'@start of CRC_________________________________________________________________________________'

#XOR function for binary division
def XOR(a,b):
    result = []
    separator = ''
    
    for i in range(1,len(b)):
        if a[i] == b[i]:
            result.append('0')
        else:
            result.append('1')
        
    return separator.join(result)

#CRC function which peforms binary division and returns the remainder

def CRC(codeword,polynomial):
    div = len(polynomial)
    temp = codeword[0 : div]

    while div < len(codeword):
        if temp[0] == '1':
            temp = XOR(polynomial, temp) + codeword[div]
        else:
            temp = XOR('0'*div,temp) + codeword[div]
        
        div += 1
    if temp[0] == '1':
        temp = XOR(polynomial,temp)
    else:
        temp = XOR('0'*div,temp)
    
    return temp

'@function: utility for CRC'
'@type: Sender Side'
#returns the codeword with redundent bits
def CRCutil(data,polynomial):
    l = len(polynomial)
    codeword = data + '0'*(l-1)
    remainder = CRC(codeword,polynomial)
    codeword = data + remainder
    return codeword

'@function: Validate data using CRC'
'@type: Receiver Side'

def CRCcheck(data,polynomial):
    l = len(polynomial)
    codeword = data + '0'*(l-1)
    remainder = CRC(codeword,polynomial)
    flag = 1
    for i in range(0,len(remainder)):
        if remainder[i] == '1':
            flag = 0
            break

    if flag == 1:
        print(">> Remainder : " + remainder)
        print(">> No Error Detected!")
        print("\n>>PASS!")
    else:
        print(">> Remainder : " + remainder)
        print(">> Corrupt data received!")
        print("\n>>FAIL!")
    

'@end of CRC_________________________________________________________________________________'