import socket
import selectors # for multiConnection
HOST = "127.0.0.1"
PORT = 8080
sel = selectors.DefaultSelector()

def singleConnection():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))  # bind this socket to this IP and port
        s.listen()  # listen for incoming connections
        conn, addr = s.accept()  # accept incoming connections and get its socket and IP
        with conn:  # while connection is opened
            print("Connected by ", addr)  # print the address of client
            data = conn.recv(1024)  # receive from client
            if not data:  # if no data is sent break the conn
                exit(1)
            # send the data back to client (echo) if there is data to send
            conn.sendall(data)

def accept_connection(sock):
    conn,addr = sock.accept()
    print("accepted connection from",addr) 
    conn.setblocking(False)
    data  = type.SimpleNamespace(addr,inb = b'',outb = b'') # Type of data set for the client
    events = selectors.EVENT_READ | selectors.EVENT_WRITE 
    sel.register(conn,events,data = data) # register this client

def service_connection(key,mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:# if the event is read event
        recv = sock.recv(1024)
        if recv:
            data.outb += recv
        else:
            print("Closing connection ",data.addr) 
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            print("echoing",repr(data.outb),"to",data.addr)
            sent = sock.send(data.outb)
            outb = outb[sent:]


def multiConnection():
    lsock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    lsock.bind((HOST, PORT))
    lsock.listen()
    print("Listening on ",HOST,PORT)
    lsock.setblocking(False) # it allows for many connection
    sel.register(lsock,selectors.EVENT_READ,data = None) # register server for read only 
    while True:
        events = sel.select(timeout=None)
        for key , mask in events:
            if key.data is None: # this client was not registered with the selector
                accept_connection(key.fileobj) # key.fileObj is socket of the client

            else:
                service_connection(key,mask)







