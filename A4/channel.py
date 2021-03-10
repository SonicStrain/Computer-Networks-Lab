# Channel is connected to all the station nodes
import multiprocessing
import random
import time
import threading
from walsh import addcIdI,cdmaDecoding


class Channel:
    def __init__(self):
        self.busy = 0

# Generates C1*D1 + C2*D2 ... + CN*DN
def commonData(L):
    data = 0
    i = 0
    data = L[0] - L[0]
    for i in range(0,len(L)):
        data = data + L[i]
    
    return data

#<--------------------------------------------------------------------->

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


#<--------------------------------------------------------------------->

def nodeToChannel(p):
    lock = threading.Lock()
    lock.acquire()
    pipe = p.get()
    run = True
    while run:
        i = 0
        cIdIs = []
        while i<pipe[1]:
            temp = pipe[0].recv()
            cIdIs.append(temp)
            i = i + 1
        makeChannelBusy()
        '<----------------------------------------------------------->'
        cIdIsum = addcIdI(cIdIs)
        
        id = random.randint(0,pipe[3]-1)
        print("Node ID: ",id)
        cdmaDecoding(cIdIsum,pipe[2][id])
        
        cIdIs.clear()
        print("----------------------------")
        time.sleep(1)
        '<----------------------------------------------------------->'
        makeChannelidle()
    lock.release()