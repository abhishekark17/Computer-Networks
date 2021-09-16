import socket
import threading
import argparse


class Client:
    def __init__(self, SERVER, PORT, UserName):
        self.socketIN = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socketOUT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.HOST = SERVER  # server host name
        self.PORT = PORT  # server port number
        self.UserName = UserName  # user name

    def connect(self):
        while True:
            try:
                self.socketIN.connect((self.HOST, self.PORT))
                self.socketOUT.connect((self.HOST, self.PORT))
                break
            except:
                print("Couldn't connect to server")
                return

        # UserName = input("Enter UserName: ")
        self.socketOUT.send(f"REGISTER TOSEND {self.UserName}\n \n".encode())
        while True:
            AckOUT = self.socketOUT.recv(1024).decode()
            if(AckOUT == f"REGISTERED TOSEND {self.UserName}\n \n"):
                self.socketIN.send(
                    f"REGISTER TORECV {self.UserName}\n \n".encode())
                while True:
                    AckIN = self.socketIN.recv(1024).decode()
                    if AckIN == f"REGISTERED TORECV {self.UserName}\n \n":
                        print(f"{self.UserName} is successfully registered")
                        break
                    elif AckIN == f"ERROR 100 Malformed username\n \n":
                        print("UserName not Valid. Start the connection again...")
                        self.socketIN.close()
                        self.socketOUT.close()
                        return
                break
            elif AckOUT == f"ERROR 100 Malformed username\n \n":
                print("Invalid username. Start the connection again...")
                self.socketIN.close()
                self.socketOOUT.close()
                return
        send_handler = threading.Thread(target=self.send_Handler)
        recv_handler = threading.Thread(target=self.recv_Handler)
        send_handler.start()
        recv_handler.start()

    def right_format(self, message):
        # message = message.split("\n")
        # if len(message) != 4:
        # 	return False
        # else:
        # 	if len(message[0]) != 2 or message[0].split(" ")[0] != "SEND":
        # 		return False
        # 	else:
        # 		if len(message[1] != 2) or message[1].split(" ")[0] != "Content-length:":
        # 			return False
        # 		elif len(messsage[2]) != 0:
        # 			return False
        return True

    def send_Handler(self):
        while True:
            message = input()
            recipient = message.split(" ")[0][1:]
            messageOriginal = " ".join(message.split(" ")[1:])
            if self.right_format(message):
                self.socketOUT.send(
                    f"SEND {recipient}\nContent-length: {len(messageOriginal)}\n \n{messageOriginal}".encode())
                while True:
                    ack = self.socketOUT.recv(1024).decode()
                    if ack == f"SEND {recipient}\n \n":
                        print(f"Message Delivered successfully to {recipient}")
                        break
                    elif ack == f"ERROR 102 Unable to send\n \n":
                        print("ERROR 102 Unable To Send")
                        break
                    elif ack == f"ERROR 103 Header incomplete\n \n":
                        print("ERROR 103 Header incomplete")
                        break
            else:
                print("Wrong message format. Send again with right message format...")

    def recv_Handler(self):
        while True:
            message = self.socketIN.recv(1024).decode()
            try:
                sender = message.split("\n")[0].split(" ")[1]
                messageOriginal = message.split("\n")[3]
                self.socketIN.send(f"RECEIVED {sender}\n \n".encode())
            except:
                self.socketIN.send(f"ERROR 103 Header incomplete\n \n")
                continue
            print(f"{sender}: {messageOriginal}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--Server", help="Provide the name of the server",required=True)
    parser.add_argument("--username",type=str, help="Provide the UserName",required=True)
    parser.add_argument("--Port", default=1234, type=int,
                        help="Provide the Port number of the server")
    opt = parser.parse_args()
    SERVER = opt.Server
    PORT = int(opt.Port)
    Username = opt.username
    client = Client(SERVER, PORT, Username)
    client.connect()
