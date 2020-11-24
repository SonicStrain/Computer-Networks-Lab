#---------------------------------------------------------------#

def decimalToBinary(n):  
    return n.replace("0b", "")


def binarycode(s):
    a_byte_array = bytearray(s, "utf8")

    byte_list = []

    for byte in a_byte_array:
        binary_representation = bin(byte)
        byte_list.append(decimalToBinary(binary_representation))

    #print(byte_list)
    
    return byte_list

#----------------------------------------------------------------#

##############################################################################################

#ERROR DETECTION

#polynomial = '1011' #CRC-4

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
        return 0
    else:
        print(">> Remainder : " + remainder)
        return 1
    

'@end of CRC_________________________________________________________________________________'
##############################################################################################

##############################################################################################
# IN CHANNEL PROCESS #
import random

def injectError(L):

    t = random.randint(0,6)
    size = len(L)
    if t==1:
        i = random.randint(0,size-1)
        if L[i]=='0':
            L=L[:i]+'1'+L[i+1:]
        else:
            L=L[:i]+'0'+L[i+1:]

    elif t== 2:
        n = random.randint(0,size-1)
        for x in range(n):
            i = random.randint(0,size-1)
            if L[i]=='0':
                L=L[:i]+'1'+L[i+1:]
            else:
                L=L[:i]+'0'+L[i+1:]

    else:
        print("No error injected!")

    return L

##############################################################################################

######################################################################
#----------> Ethernet Frame Format IEEE 802.3 Standard <-------------#
'PREMBLE - 7 Bytes'
'SFD[Start of frame delimiter] - 1 Byte : 10101011'
'______________________________'
'Destination Address - 6 Bytes'
'Source Address - > 6 Bytes'
'Length -> 2 Bytes'
'______________________________'
'Data -> Max 1500 Bytes'
'Cyclic Redundancy Check - 4 Bytes'
######################################################################


import struct

def packet_maker(data):
    premble = "10101010" * 7
    sfd = "10101011"
    da = "11000000" + "10100010" + "00111000" + "00000001" #destination address
    sa = "11000000" + "10100010" + "00111000" + "00000001" #sender address
    l = len(data) #size of the data
    s = bin(20+l)[2:] #size
    s = str(s)
    # data = data + CRC
    #packet = premble + sfd + data[data + CRC]
    #convert it into data packets
    premble = premble + sfd #(Total 8 bytes)
    premble = int(premble,2)
    da = int(da,2)
    sa = int(sa,2)
    s = int(s,2)
    #sfd = int(sfd,2)
    data = int(data,2)
    return struct.pack('!QQQQQ',premble,da,sa,s,data)

def packets(L):
    s = len(L)
    frames = []
    for i in range(0,s):
        frame = packet_maker(L[i])
        frames.append(frame)
    
    return frames

#------------------> DATA PACKET UNPACKER <---------------------#

def unpacker(data):
    data = struct.unpack('!QQQQQ',data)
    #remove preamble and sfd
    data = data[4]
    data = bin(data)[2:]
    data = str(data)
    return data

#########################################################################