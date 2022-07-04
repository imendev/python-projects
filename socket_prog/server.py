import socket
import threading

# MAXIMUM AMOUNT OF ALLOWED BYTES
HEADER = 64
FORMAT = "utf_8"
DISCONNECTED_MSG = "!DISCONNECTED"
PORT = 5050

SERVER = socket.gethostbyname(socket.gethostname())

ADDR = (SERVER, PORT)
# CREATE A SOCKET OVER INTERNET AF_INET
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
# BIND THE SOCKET TO THE ADDR
server.bind(ADDR)

# SET UP THE SOCKET TO BEING IN LESTEN MODE
def handle_client(conn, addr):
    print(f"|NEW CONNECTION| {addr} connected.")

    connected = True
    while connected:
        msg_len = conn.recv(HEADER).decode(FORMAT)
       
        if msg_len:
            
            msg_len = int(msg_len)
            msg = conn.recv(msg_len).decode(FORMAT)

            if msg == DISCONNECTED_MSG:
                connected = False

            print(f"[{addr}] {msg} ")
            conn.send("Message recived".encode(FORMAT))
    
    conn.close()

# START THE SOCKET
def start():
    server.listen()
    print(f"|LISTENING| Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        # each entred client connection, the server create a thread
        thread = threading.Thread(target=handle_client, args=(conn, addr))  
        thread.start()
        # WHEN 3 CLIENTS ARE CONNECTED => 1 IS HANDLED AND 2 ARE IN ACTIVE CONNECTION MODE
        print(f"|ACTIVE CONNECTIONS| {threading.activeCount() - 1}")



print("Server is starting ...")
start()