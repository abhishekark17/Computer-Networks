import socket
import sys
try:
    HOST = gethostbyname(sys.argv[1])
except socket.gaierror as e:
    print("Invalid Host Name ",e)
    exit(-1)

PORT = 80
message = "Hello, world!"
print(HOST, PORT)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(bytes(message, 'utf-8'), (HOST, PORT))
