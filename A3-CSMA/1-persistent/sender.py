#sender class
import multiprocessing
import random
import time
import threading
import sys
sys.path.append(".")
from channel import Channel,getChannelStatus
from packet import packet

temp1 , temp2 = multiprocessing.Pipe()

class Sender:
    #class attributes
    def __init__(self,address,ch):
        self.address = address
        self.pipe = temp1
        self.c = ch
        self.collision = False
        self.totalPacketTranmitted = 0
        self.notsuccessfulPacketTransmitted = 0
        self.successfulPacketTransmitted = 0
        self.transmissionTime = time.time()

    # randomly selects receiver node
    def selectReceiverNode(self,receiverNumber):
        return random.randint(0,receiverNumber-1)

    #sense the carrier/channel
    def senseChannel(self):
        return self.c.isBusy()
    
    def backoff(self):
        a = random.randint(10,100)
        self.collision = False
        time.sleep(a/100) #goes for backoff

    def successfulTransmission(self):
        self.successfulPacketTransmitted = self.successfulPacketTransmitted + 1

    def totalTransmission(self):
        self.totalPacketTranmitted = self.totalPacketTranmitted + 1

    def notSuccesfulTransmission(self):
        self.notsuccessfulPacketTransmitted = self.notsuccessfulPacketTransmitted + 1

    def setTransmissionTime(self):
        self.transmissionTime = time.time()

    def setCollision(self):
        self.collision = True

    


def sendData(q):
    lock = threading.Lock()
    lock.acquire()
    p = q.get()
    raw_data = ["1010101","111001","10101010","101010101"]
    data = []
    x = 0
    for x in range(len(raw_data)):
        data.append(packet(raw_data[x]))

    startTime = time.time()
    #<-------------------------------------------------------->
    #check if channel is busy continuously sense the channel
    i = 0
    while i < len(data):
        #print("<--------------> ",i," <--------------->")
        if(p[1].collision == True):
            #backs off for random ammount of time
            print("\n******COLLISION******","\n____backing off____","node ID: ",str(p[1].address),"\n")
            p[1].backoff()
            #retransmit the previous data
            i = i - 1
            if i < 0:
                i = 0
            p[1].notSuccesfulTransmission()
        else:
            a = random.randint(0,10)
            if(a>8):
                #backs off for random ammount of time
                print("\n******COLLISION******","\n____backing off____","node ID: ",str(p[1].address),"\n")
                p[1].backoff()
                #retransmit the previous data
                i = i - 1
                if i < 0:
                    i = 0
                p[1].notSuccesfulTransmission()

        #check if channel is busy continuously sense the channel
        while(getChannelStatus()):
            continue
        
        prob = 1 #probability by which the sender transmits
        rint = random.randint(0,9)

        if(prob*10>rint):
            print("node ID: ",p[1].address)
            temp = "Sending from node ID:" + str(p[1].address)
            p[1].setTransmissionTime()
            p[0].send(data[i])
            p[0].send(p[1].address)
            p[1].totalTransmission()
            i = i + 1
            time.sleep(0.2)
        else:
            print("Data not sent")
            i = i - 1
            if i < 0:
                i = 0
    
    endTime = time.time()
    print("\n<---------------------------------------------------->","\nNode ID : ",p[1].address,"\nThroughput: ",float((p[1].totalPacketTranmitted - p[1].notsuccessfulPacketTransmitted))/float((endTime-startTime)),"\nTotal time taken: ",endTime-startTime,"\n<---------------------------------------------------->")
    
    lock.release()


