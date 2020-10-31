from comUtil import getDword,readMsg,writeMsg,getFullMsg,injectError
from schmLib import VRCutil,VRCcheck
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
    #read the codeword and break it into dataword
    getDword(codeward,div)
    #collect the dataword into a list
    L = readMsg() 
    #VRC and send codeword
    L = VRCutil(L)
    #write the message to send to text
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
    print("Enter y to proceed to the receiver side!")
    flag = input()
    print("\nprogressing...\n")
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
    #VRC and check
    getDword(rCodeword,div+1) #read the codeword and break it into dataword
    rL = readMsg() #store into list
    print("\n")
    VRCcheck(rL) #validate at the receiver side
    #VRC completed

    
