from comUtil import getDword,readMsg,writeMsg,getFullMsg,injectError
from schmLib import CRCutil,CRCcheck
import sys

'@author: Sagen Soren'
'@CNL'
'@file: Vertical Redundancy Check'

if __name__ == "__main__":
    with open(sys.argv[1],'r') as f:
        codeword = f.read()
    #get the dataword
    print("Data : " + codeword)
    print("\n")
    polynomial = '1101'
    #create the codeword with remainder using CRC
    codeword = CRCutil(codeword,polynomial)
    #write the message to send.txt
    writeMsg(codeword)
    print("Data sending in progress...\n")
    print("Want to inject Errors? Enter y for yes!")
    eflag = input()
    if eflag == 'y':
        injectError()
    else:
        print("\nNo error injected!")
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
    #validate the data
    CRCcheck(rCodeword,polynomial)
    print("\n")
    #CRC completed

    
