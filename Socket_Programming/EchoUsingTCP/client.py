import socket
import selectors
sel = selectors.DefaultSelector()
HOST = "127.0.0.1" # IP of server
PORT = 8080 # Port of server
messages = [b'Message 1 from client.', b'Message 2 from client.']

def singleConnection:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as c:
        c.connect((HOST, PORT)) # connect to port open on host and port 
        c.sendall(b"Hello World!")
        data = c.recv(1024) # receive data from server

    print("client", repr(data))

def multiConnection:
    server_addr = (HOST,PORT)
    for i in range(5):
        print("starting connection",i+1)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)
        sock.connect_ex(server_addr)
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        data = types.SimpleNamespace(connid=i+1,msg_total=sum(len(m) for m in messages), recv_total=0, messages=list(messages),outb=b'')
        sel.register(sock, events,data = data)
