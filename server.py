import socket
import threading

HOST= '127.0.0.1'
PORT = 9090

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

server.listen()

clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        client.send(message)


def handle(client):
    while True:
        try:
            message = client.recv()
            print(f"{nicknames[clients.index(client)]} says {message}")
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            break

def recieve():
    while True:
        client, address = server.accept()
        print(f"Connected to {str(address)}")
        client.send("NICK".encode('utf-8'))

        nickname = client.recv(1024)
        nicknames.append(nickname)
        client.append(clients)

        print(f"Nickname of the client is {nickname}")
        broadcast(f"{nickname}nickname connected to server!\n".encode('utf-8'))
        client.send("Connected to the server".encode('utf-8'))
        
        thread = threading.Thread(target=handle, args=(client))
        thread.start()
print("Server is running...")
recieve()