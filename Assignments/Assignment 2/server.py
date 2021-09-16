import socket
import threading
import sys
import argparse

HOST = "127.0.0.1"
PORT = 1234


class Server:
    def __init__(self, maxClient):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.recv_clients = {}  # Dictionary of username->client_IN socket
        self.send_clients = {}  # Dictionary of username->clinet_OUT socket
        self.socket.bind((HOST, PORT))
        self.socket.listen(maxClient)
        self.username = {}
        print(f"Host Running on HOST: {HOST} and PORT: {PORT}")
        while True:
            client, addr = self.socket.accept()
            new_thread = threading.Thread(
                target=self.Registration, args=(client,))
            new_thread.start()

    def notWellFormed(self, username):
        for c in username:
            if (ord(c)-ord("a") >= 0 and ord(c)-ord("a") <= 25) or (ord(c)-ord("A") >= 00 and ord(c)-ord("A") <= 25) or (ord(c)-ord("0") >= 0 and ord(c)-ord("0") <= 10):
                continue
            else:
                return True
        return False

    def Registration(self, client):
        message = client.recv(1024).decode()
        if message.split('\n')[0].split(" ")[0] != "REGISTER":
            client.send(f"ERROR 101 No User Registered\n \n".encode())
        else:
            if message.split("\n")[0].split(" ")[1] == "TORECV":  # Handle this later
                username = message.split("\n")[0].split(" ")[2]
                if(self.notWellFormed(username)):
                    client.send(f"ERROR 100 Malformed username\n \n".encode())
                    return
                self.recv_clients[username] = client
                self.username[client] = username
                client.send(f"REGISTERED TORECV {username}\n \n".encode())
                sys.exit()
            elif message.split("\n")[0].split(" ")[1] == "TOSEND":
                username = message.split("\n")[0].split(" ")[2]
                if(self.notWellFormed(username)):
                    client.send(f"ERROR 100 Malformed username\n \n".encode())
                    return
                self.send_clients[username] = client
                self.username[client] = username
                client.send(f"REGISTERED TOSEND {username}\n \n".encode())
                self.handle_message(client)

    def handle_message(self, client):
        while True:
            message = client.recv(1024).decode()
            if len(message) > 1:
                try:
                    recipient = message.split("\n")[0].split(" ")[1]
                    messageOriginal = message.split("\n")[3]
                except:
                    client.send(f"ERROR 102 Unable to send\n \n".encode())
                    continue

                recipient_sockets = []  # For broadcasting purpose
                if recipient == "all":
                    for key, value in self.recv_clients.items():
                        if self.send_clients[self.username[value]] != client:
                            recipient_sockets.append(value)
                else:
                    try:
                        recipient_sockets.append(self.recv_clients[recipient])
                    except:
                        client.send(f"ERROR 102 Unable to send\n \n".encode())
                        continue
                for recipient_socket in recipient_sockets:
                    recipient_socket.send(
                        f"FORWARD {self.username[client]}\n Content-length {len(messageOriginal)}\n \n{messageOriginal}".encode())
                    while True:
                        recipient_ack = recipient_socket.recv(1024).decode()
                        if recipient_ack == f"RECEIVED {self.username[client]}\n \n":
                            client.send(f"SEND {recipient}\n \n".encode())
                            break
                        elif recipient_ack == f"ERROR 103 Header incomplete\n \n":
                            client.send(recipient_ack.encode())
                            break


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=10,
                        help="Maximum Number of clients")
    opt = parser.parse_args()
    Max_clients = int(opt.n)
    server = Server(Max_clients)
