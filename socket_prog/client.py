from email import message
import socket

# MAXIMUM AMOUNT OF ALLOWED BYTES
HEADER = 64
FORMAT = "UTF_8"
DISCONNECTED_MSG = "!DISCONNECTED"
PORT = 5050
SERVER = "192.168.1.18"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT) # ENCODE THE STR INTO BYTE OBJECT
    message_len = len(message)

    send_len = str(message_len).encode(FORMAT)
    # AMOUNT OF BYTES WILL BE SENT
    send_len += b' ' * (HEADER - len(send_len))
    # FIRST THE NUM BYTES 
    client.send(send_len)
    # THEN THE TEXT MESG 
    client.send(message)
    # RECIEVE FROM THE SERVER
    print(client.recv(2048).decode(FORMAT))

send("Hello Python !")
send("Hello Imen !")
send("Hello World !")
send(DISCONNECTED_MSG)