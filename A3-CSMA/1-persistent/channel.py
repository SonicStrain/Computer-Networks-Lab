# Channel is connected to all the station nodes
import multiprocessing
import random
import time
import threading
from packet import unpacker


def check_collision(sendersList):
    #if any two transmits at the same time collision happens
    for i in range(len(sendersList)):
        for j in range(len(sendersList)):
            if(sendersList[i].transmissionTime == sendersList[j].transmissionTime):
                sendersList[i].setTransmissionTime()
                sendersList[i].setCollision()
                sendersList[j].setCollision()
            else:
                collide = random.randint(0,10)
                if(collide > 7):
                    if(round(sendersList[i].transmissionTime)==round(sendersList[j].transmissionTime)):
                       sendersList[i].setTransmissionTime()
                       sendersList[i].setCollision()
                       sendersList[j].setCollision()
                       break

class Channel:
    def __init__(self):
        self.busy = 0

    def isBusy(self):
        if self.busy == 0:
            return False
        if self.busy == 1:
            return True
    
    def idleStatus(self):
        self.busy = 0
    
    def busyStatus(self):
        self.busy = 1

channelStatus = 0

def makeChannelBusy():
    channelStatus = 1

def makeChannelidle():
    channelStatus = 0

def getChannelStatus():
    if channelStatus == 1:
        return True
    if channelStatus == 0:
        return False



def nodeToChannel(p):
    lock = threading.Lock()
    lock.acquire()
    pipe = p.get()
    while True:
        #receive the data
        data = pipe[0].recv()
        val = pipe[0].recv()
        #set the Channel as busy
        makeChannelBusy()
        
        print("Packet from node: ",val)
        #check for potential collisions
        check_collision(pipe[2])
        #set it is as not busy
        time.sleep(0.2)
        makeChannelidle()
    lock.release()