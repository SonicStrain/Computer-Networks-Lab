import multiprocessing
import random
import sys
import threading
import time
import continuous_threading
sys.path.append(".")
from channel import Channel, nodeToChannel
from sender import Sender, sendData
from walsh import walsh_code

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

    '<----------------------------------------------------------------------------------------->'

    #generate walsh table
    chips = walsh_code(senderNodenumber)
    storage = []
    print("\n....................... WALSH TABLE ...................................")
    for i in range(0,len(chips)):
        print(chips[i])
        storage.append(chips[i])
    print("-----------------------------------------------------------------------")

    
    #data = ["1010101010101","111000101","110101011","1101","000101"]
    data = ["1010","1-0-","1111","0000","----","--11","-100"] #"-" denotes idleness

    print("<--------------------------------------------------------------------->")
    # creating n numbers of sender nodes
    for i in range(senderNodenumber):
        d = random.randint(0,len(data)-1) #random allocation of data
        print("Node ID: ",i," Data: ",data[d])
        senders.append(Sender(i,data[d]))
    
    print("<--------------------------------------------------------------------->")
    print("-----------------------------------------------------------------------")


    '<--------------------------------------------------------------------------------------->'
    #pipeline connnecting the senders and channel
    senderToChannel , channelToSender = multiprocessing.Pipe()
    '<--------------------------------------------------------------------------------------->'
    cq = multiprocessing.Queue()
    cq.put([channelToSender,senderNodenumber,chips,senderNodenumber])
    c = continuous_threading.ContinuousThread(target=nodeToChannel,args={cq,})
    
    senderNodes = []
    q = multiprocessing.Queue()
    for i in range(senderNodenumber):
        q.put([senderToChannel,senders[i],senderNodenumber,chips[i]])
        senderNodes.append(continuous_threading.ContinuousThread(target=sendData,args={q,}))
    
    
    for i in range(senderNodenumber):
        senderNodes[i].start()

    #start the channel
    c.start()

    for i in range(senderNodenumber):
        senderNodes[i].join()
    
    c.join()
    




