from walsh import walsh_code,cdmaEncoding,cdmaDecoding,chipXdata,addcIdI

var=""
print("<------------------------------------------------------>")
print("Enter 0 and 1, To mark idle enter -")
print("<------------------------------------------------------>\n")


while var != "n":
    
    print("Enter the number of nodes:")
    nodes = int(input())

    #create the walsh table
    chips = walsh_code(nodes)
    storage = []
    
    print("\n....................... WALSH TABLE ...................................")
    for i in range(0,len(chips)):
        print(chips[i])
        storage.append(chips[i])
    print("-----------------------------------------------------------------------")

    print("Enter the value [1/0/-]")
    #take the input from nodes
    cIdIs = []
    i=0
    while i<nodes:
        print("Enter code for Node : ",i," >>")
        temp = input()
        if temp == "1" or temp == "0" or temp == "-":
            ecdTemp = cdmaEncoding(temp)
            cIdI = chipXdata(chips[i],ecdTemp)
            cIdIs.append(cIdI)
            i = i + 1
        else:
            print("WARNING ENTER VALID CODE!!")
            i = i - 1
            if i<0:
                i = 0

    #Generates C1*D1 + C2*D2 ... + CN*DN  
    cIdIsum = addcIdI(cIdIs)

    print("-------------------------------------------------------------------------")
    #Enter node ID you want to listen from
    print("\nEnter Node ID from where you want to listen:")
    id = int(input())
    while id<0 or id>=nodes:
        print("Enter valid ID: [",0,"-",nodes-1,"]")
        id = int(input())
    #print(chips)
    cdmaDecoding(cIdIsum,chips[id])
    
    print("\nWant to listen from another Node/[y/n]")
    var2 = input()

    while var2 != "n":
        print("\nEnter Node ID from where you want to listen:")
        id = int(input())
        while id<0 or id>=nodes:
            print("Enter valid ID: [",0,"-",nodes-1,"]")
            id = int(input())
        cdmaDecoding(cIdIsum,chips[id])
        
        print("\nWant to listen from another Node/[y/n]")
        var2 = input()

    
    cIdIs.clear()

    print("Want to run again?[y/n]")
    var = input()
