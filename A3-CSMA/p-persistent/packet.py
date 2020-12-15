##############################################################################################

#-----------------------------> CYCLIC REDUNDANCY CHECK <------------------------------------#

#polynomial = '1011' #CRC-4

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



#--------------------------------------------------------------------------------------------#
#------------------------------------   PACKET   --------------------------------------------#
#--------------------------------------------------------------------------------------------#




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
#MAX SIZE  = 1518 Bytes
######################################################################

'7s --> 7 byte string'
's --> 1 byte string'
'6s --> 6 byte string'
'6s --> 6 byte string'
'2s --> 2 byte string'
'xs --> x byte string'
'4s --> 4 byte string'

'format expression: !8s6s6s2s36s'

'8s == PREMBLE : 7 byte + sfd : 1 bytes'
'36s == Data : 32 bytes + CRC : 4 bytes'

#TOTAL SIZE : 7 + 1 + 6 + 6 + 2 + 32 + 4 = 58 bytes

########################################################################

import struct

'@function: Create data packet in 802.3 IEEE format'
'@type: Sender Side'

def packet(data):

    premble = '10101010'
    sfd = '10101011'

    destination = '111001'
    source = '100111'
    length = str(bin(len(data))[2:])

    dataAndCRC = CRCutil(data,'1101')

    #convert strings into Bytes
    premble = premble + sfd
    premble = bytes(premble,'utf-8')

    destination = bytes(destination,'utf-8')
    source = bytes(source,'utf-8')
    length = bytes(length,'utf-8')

    dataAndCRC = bytes(dataAndCRC,'utf-8')

    #return data packet with network endian
    return struct.pack('8s6s6s2s36s',premble,destination,source,length,dataAndCRC)

#------------------> DATA PACKET UNPACKER <---------------------#

def unpacker(data):
    data = struct.unpack('6s8s6s2sh36s',data)
    #remove preamble and sfd
    data = data[5]
    seq = data[4]
    data = str(data)
    return seq
