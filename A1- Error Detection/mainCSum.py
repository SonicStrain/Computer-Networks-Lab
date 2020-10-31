from comUtil import getDword,readMsg,writeMsg,getFullMsg,injectError
from schmLib import CSutil,CScheck
import sys

'@author: Sagen Soren'
'@CNL'
'@file: Vertical Redundancy Check'

if __name__ == "__main__":
    with open(sys.argv[1],'r') as f:
        codeward = f.read()
    #size of each dataword
    print("Enter the size of each dataword:")
    div = int(input())
    print("\n")
    #creating dataword of size div
    getDword(codeward,div)
    L = readMsg() #read the codeword and break it into dataword and add it to a list
    #CheckSum and append the redundancy bits
    L = CSutil(L,div)
    #write the message to send.txt
    writeMsg(L)
    print("Data sending in progress...\n")
    print("Want to inject Errors? Enter y for yes!")
    eflag = input()
    if eflag == 'y':
        injectError()
    else:
        print("No error injected!")
    print("\nThe message has been sent!\n")
    print("\n###############################################################################################\n")
    print("Enter y to transfer to the receiver side!")
    flag = input()
    if flag == 'y':
        print("\n***********************       Welcome to receiver side!         *******************************")
        print("\n###############################################################################################\n")
    else:
        print("\n###############################################################################################\n")
        print("Program is closing!")
        exit()
    print("The received message : ")
    rCodeword = getFullMsg('sent.txt') # received codeword
    print(rCodeword)
    #CheckSum and check
    #read the codeword and break it into dataword
    getDword(rCodeword,div)
    #store the values in list 
    rL = readMsg()
    print("\n")
    CScheck(rL,div) #validate at the receiver side
    #CheckSum completed

    
