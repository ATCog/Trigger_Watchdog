import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 6781))
server_socket.listen(1)
print("Server is listening...")

while True:
    client_socket, addr = server_socket.accept()
    print(f"Connection from {addr}")
    data = client_socket.recv(1024)
    if data:
        print(f"Received: {data.decode()}")
    client_socket.close()
