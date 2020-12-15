import multiprocessing
import random
import sys
import threading
import time
import continuous_threading
sys.path.append(".")
from channel import Channel, nodeToChannel
from sender import Sender, sendData

if __name__ == '__main__':

    #Initialize the Channel
    '<--------------------------------------------------------------------------------------->'
    #one common Channel
    carrier = Channel()
    '<--------------------------------------------------------------------------------------->'
    #create sender nodes
    senders = []
    print("Enter the number of senders: ")
    senderNodenumber = int(input())
    
    # creating n numbers of sender nodes
    for i in range(senderNodenumber):
        senders.append(Sender(i,carrier))
    #node1.sendData()
    #carrier.nodeToChannel()

    '<--------------------------------------------------------------------------------------->'
    senderToChannel , channelToSender = multiprocessing.Pipe()
    #receiverToChannel , channelToreceiver = multiprocessing.Pipe()
    '<--------------------------------------------------------------------------------------->'
    cq = multiprocessing.Queue()
    cq.put([channelToSender,carrier,senders])
    c = continuous_threading.ContinuousThread(target=nodeToChannel,args={cq,})
    
    senderNodes = []
    q = multiprocessing.Queue()
    for i in range(senderNodenumber):
        q.put([senderToChannel,senders[i],carrier])
        senderNodes.append(continuous_threading.ContinuousThread(target=sendData,args={q,}))
    
    
    for i in range(senderNodenumber):
        senderNodes[i].start()

    #start the channel
    c.start()
    




