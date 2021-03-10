#sender class
import multiprocessing
import random
import time
import threading
import sys
sys.path.append(".")
from channel import Channel,getChannelStatus
from walsh import cdmaEncoding,chipXdata


class Sender:
    #class attributes
    def __init__(self,ID,data):
        self.ID = ID
        self.data = data

    # randomly selects receiver node
    def selectReceiverNode(self,receiverNumber):
        return random.randint(0,receiverNumber-1)

    


def sendData(q):
    lock = threading.Lock()
    lock.acquire()
    p = q.get() #[pipe||sender object||total number of senders]
    #<-------------------------------------------------------->
    i=0
    while i<len(p[1].data):
        while(getChannelStatus()):
            continue
        
        data = cdmaEncoding(p[1].data[i])
        cIdI = chipXdata(p[3],data)
        p[0].send(cIdI)
        i = i + 1
        time.sleep(1.3)
    lock.release()


