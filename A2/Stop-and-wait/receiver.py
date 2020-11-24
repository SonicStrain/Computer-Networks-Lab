import time
import socket
import sys
import random
import array
from utility import unpacker,injectError,CRCcheck

#__________________________Establish connection______________________#
s = socket.socket()
host1 = socket.gethostname()
ip = socket.gethostbyname(host1)

host = str(ip)

port = 1234
name = 'Receiver_Station_SAW'

#Connect to remote ADDR, and then wraps the connection in an SSL channel
s.connect((host,port))

s.send(name.encode())
s_name = s.recv(1518)
s_name = s_name.decode()

print("Connected to ",s_name)

#_____________________________________________________________________#

f = s.recv(1518)
f = f.decode()
f = int(f)


while True:

    counter = 0
    message = []
    polynomial = '1011'

    while counter < f:
        #receive the data packet
        temp = s.recv(1518)
        #a1 = time.time()
        temp = unpacker(temp)
        
        #injet an error
        temp = injectError(temp)
        
        #validate the data
        error = CRCcheck(temp,polynomial)
        #random time delay
        a = random.randint(0,4)
        time.sleep(a)
        print("Time: ",a)
        #----> 1 represent error and 0 represent no error <----#
        e = str(error)
        #if timeout happens nothing is being sent
        if a < 3:
            s.send(e.encode())
            #b1 = time.time()
            #print(b1-a1)
        else:
            error = 1
        
        if a < 3:
            if e != "1":
                print("\n>>",temp[:-3],"\n")
                counter = counter + 1

    s.close()
    break