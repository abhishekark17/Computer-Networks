import sys
import os
import time
import matplotlib.pyplot as plt


WEBSITE = sys.argv[1]
ttl = 1
ip = []
rtt=[]

while True:
    # find the intermediate route for a particular ttl 
    os.system("ping4 -c 1 -t "+str(ttl)+" " + WEBSITE + " > temp.txt")
    # time.sleep(1)  # to be able to write to file
    # read the ip address of the intermediate source
    fileToRead = open("temp.txt", "r")
    lines = fileToRead.readlines()
    ipOfHost = lines[0].split(" ")[2]
    if(ttl == 1):
        print("ip of Website", ipOfHost)

    ipOfIntermediateServer=""

    # if website is reached break from the loop
    if lines[1].split(" ")[-1] == "ms\n":
        ipOfIntermediateServer = lines[1].split(" ")[4][1:-2]
        # print(ipOfIntermediateServer)

    # In case router/switch does not respond
    if(lines[1] == "\n"):
        ttl += 1
        ip.append("No Reply")
        rtt.append(float(0))
        print(ttl,"\tNo reply\t",0.0)
        fileToRead.close()
        continue
    
    # If the website was not reached
    if ipOfIntermediateServer=="":
        ipOfIntermediateServer = lines[1].split(" ")[1]
        if(ord(ipOfIntermediateServer[0])<49 or ord(ipOfIntermediateServer[0])>58):
            ipOfIntermediateServer = lines[1].split(" ")[2][1:-1]
    
    ip.append(ipOfIntermediateServer)

    # To find the rtt of the router where the packet was lost
    command = "ping4 -c 1 " + ipOfIntermediateServer + ">pinged.txt"
    os.system(command)
    
    # Get the rtt of the corresponding server
    Pinged = open("pinged.txt", "r")
    line = Pinged.readlines()
    if(line[1]!='\n' and line[1].split(" ")[-1]=="ms\n"): # if there is no error (just for safety)
        rtt.append(float(line[1].split(" ")[-2].split("=")[-1]))
    else:
        rtt.append(float(0))
    
    Pinged.close()
    fileToRead.close()
    print(f'{ttl}\t{ipOfIntermediateServer}\t{rtt[-1]}')
    ttl += 1

    # if the website is reached break the loop
    if(ipOfHost[1:-1] == ipOfIntermediateServer or lines[1].split(" ")[-1]=="ms\n"):
        break

# print(ip)
# print(rtt)
ttlList = [i for i in range(1,len(ip)+1)]
# plt.plot(ttlList,rtt,'bo',label=)


fig, ax = plt.subplots()
plt.xlim(0,len(ip)+1)
        
ax.scatter(ttlList, rtt)
fig.suptitle('RTT vs Hop Number')
ax.set_ylabel('RTT (msec)')
ax.set_xlabel('Hop Number')
for i, txt in enumerate(ip):
    ax.annotate(str(i+1), (ttlList[i], rtt[i]))

plt.savefig("result.png")
plt.show()