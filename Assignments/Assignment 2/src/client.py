import socket
import threading
import argparse
import sys


class Client:
    def __init__(self, SERVER, PORT, UserName):
        self.socketIN = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socketOUT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.HOST = SERVER  # server host name
        self.PORT = PORT  # server port number
        self.UserName = UserName  # user name
        self.isClosed = False

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
            print(AckOUT.split("\n")[0])
            if(AckOUT == f"REGISTERED TOSEND {self.UserName}\n \n"):
                self.socketIN.send(
                    f"REGISTER TORECV {self.UserName}\n \n".encode())
                while True:
                    AckIN = self.socketIN.recv(1024).decode()
                    if AckIN == f"REGISTERED TORECV {self.UserName}\n \n":
                        print(AckIN.split("\n")[0])
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
        message = message.split("\n")
        # print(message)
        if len(message) != 4:
            return False
        else:
            if len(message[0].split(" ")) != 2 or message[0].split(" ")[0] != "FORWARD":
                return False
            else:
                if len(message[1].split(" ")) != 2 or message[1].split(" ")[0] != "Content-length:":
                    return False
                # elif len(message[2].split(" ")) != 0:
                #     return False
                elif int(message[1].split(" ")[1]) != len(message[3]):
                    return False
        return True

    def send_Handler(self):
        while True:
            message = input()
            recipient = message.split(" ")[0][1:-1]
            messageOriginal = " ".join(message.split(" ")[1:])
            messageFinal = f"SEND {recipient}\nContent-length: {1}\n \n{messageOriginal}"
            self.socketOUT.send(
                messageFinal.encode())
            while True:
                ack = self.socketOUT.recv(1024).decode()
                # print(ack.split("\n")[0])
                if ack == f"SEND {recipient}\n \n":
                    print(f"Message Delivered successfully to {recipient}")
                    break
                elif ack == f"ERROR 102 Unable to send\n \n":
                    print(ack.split("\n")[0])
                    break
                elif ack == f"ERROR 104 Recipient Side Failure\n \n":
                    print(ack.split("\n")[0])
                    break
                elif ack == f"ERROR 103 Header Incomplete\n \n":
                    print(ack.split("\n")[0])
                    self.isClosed = True
                    sys.exit()
                    return

    def recv_Handler(self):
        while not self.isClosed:
            message = self.socketIN.recv(1024).decode()
            if(self.right_format(message)):
                try:
                    sender = message.split("\n")[0].split(" ")[1]
                    messageOriginal = message.split("\n")[3]
                    self.socketIN.send(f"RECEIVED {sender}\n \n".encode())
                    # print("Sent Receive Ack")
                except:
                    self.socketIN.send(
                        f"ERROR 103 Header Incomplete\n \n".encode())
                    # print("Message Not Forwaded Properly")

                    continue
                print(f"@{sender}: {messageOriginal}")
            else:
                if not self.isClosed:
                    self.socketIN.send(
                        f"ERROR 103 Header Incomplete\n \n".encode())
                    continue


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--Server", help="Provide the name of the server", required=True)
    parser.add_argument("--username", type=str,
                        help="Provide the UserName", required=True)
    parser.add_argument("--Port", default=1234, type=int,
                        help="Provide the Port number of the server")
    opt = parser.parse_args()
    SERVER = opt.Server
    PORT = int(opt.Port)
    Username = opt.username
    client = Client(SERVER, PORT, Username)
    client.connect()
