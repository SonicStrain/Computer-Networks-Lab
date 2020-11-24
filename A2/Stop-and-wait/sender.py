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
print("\n<------------------------------------------------------------>")

#####################################################################

while True:

    counter = 0

    while counter < f:
        #send the dataframe
        conn.send(message[counter])
        #print(time.time())

        #set timeout
        conn.settimeout(3)
        try:
            ack = conn.recv(1518)
            ack = ack.decode()
        except socket.timeout:
            print("Timeout!")
            ack = "1"
        
        if ack != "1":
            print("ACk received!")
            counter = counter + 1
            time.sleep(1)
        else:
            print("Resending!")
            time.sleep(1)
    
        
    #__________________________________________________________________#
    conn.close()
    break

