import sys
import socket
import time
import multiprocessing as mp
from utility import packets,CRCutil,packet_maker

'@author : Sagen Soren'
'@Computer Networks Lab'
'@Assignment 2'

#_____________________Establish Connection______________________#
s = socket.socket()
host = socket.gethostname()
ip = socket.gethostbyname(host)
port = 1234
#s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((host,port))
name = 'Sender_Station_SAW'

#_____________________connect to receiver end____________________#
s.listen(1)
print("\nWaiting for connection...\n")
# get the socket object and address info from the receiver end
conn, addr = s.accept()
print("connecting to...", addr[0], "(", addr[1], ")")

#buffer size = 1518
s_name = conn.recv(1518)
s_name = s_name.decode()
print("\nConnected to ",s_name)
conn.send(name.encode())

#_________________________________________________________________#


'Get the dataframes'

#message=[]
#message=binarycode(m) #converted to binary code

# _________________________________________________________________#
#get values to send
m = ["1010","101011","10101111","1100","1010110101","10101101"]
print(m)

#-------------------------------------------------->

#apply CRC to all
polynomial = '1011'

message = []

for i in range(0,len(m)):
    message.append(CRCutil(m[i],polynomial))

#generate data frames to send
message = packets(message)
print(message)


# _________________________________________________________________#

f=str(len(message))#length of the array
conn.send(f.encode())
f = int(f)


print("Enter the size of the sliding window : ")
n = input()
conn.send(n.encode())
n = int(n)

#####################################################################

while True:

    # _________________________________________________________________#

    'In go-back-n n frames are transmitted before receiving an acknowledgement'
    #First dataframes are transmitted before receiving an ack
    for j in range(0,n):
        time.sleep(1)
        conn.send(message[j])
        print(".")
        time.sleep(1)

    i=n
    counter = 0 #acknowledgement counter
    TIMEOUT = 3
    
    switch = 0
    hpass = 0
    holder = message[0]
    windowEdge = n - 1
    while counter < f:
        #receive ack signals
        #time1 = time.time()
        conn.settimeout(3)
        try:
            ack = conn.recv(1518)
            ack = ack.decode()
        except socket.timeout:
            print("Timeout Error")
            ack = "1"
        #conn.settimeout(None)
        
        if i < f:
            switch = 0
        else:
            switch = 1
        
        #only ack left
        if switch == 1:
            if ack != "1":
                print("\nAck ",counter)
                print("\n")
                time.sleep(1)
                #hpass = 1
                a = message[counter]
                holder = a
                counter = counter + 1
                windowEdge = windowEdge + 1
                if windowEdge >= f:
                    windowEdge = f - 1
            else:
                #for nack
                print("\nNack ",counter)
                print("Resending the frame ",counter,"\n")
                #hpass = 0
                #holder = message[counter]
        
        if switch == 0:
            #transmit the next dataframe
            if ack != "1":
                print("\nAck ",counter)
                print("Sending the next frame...",(counter + n),"\n")
                time.sleep(1)
                holder = message[counter]
                i = i + 1
                counter = counter + 1
                windowEdge = windowEdge + 1
                if windowEdge >= f:
                    windowEdge = f - 1
            else:
                print("\nNack ",counter)
                print("Resending the frame ",counter,"\n")
                #holder = message[counter]

        # how many frames need to be Sent
        if ack != "1":
            conn.send(holder)
        else:
            a1 = windowEdge - (n-1)
            a2 = windowEdge + 1
            for a in range(a1,a2):
                time.sleep(1)
                conn.send(message[a])
                print(".")
                time.sleep(1)

    
        
    #__________________________________________________________________#
    conn.close()
    break

