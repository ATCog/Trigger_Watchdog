import socket

port = 6781

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', port))  # Listen on all interfaces
    server_socket.listen(1)
    print(f'Server listening on port {port}')

    while True:
        client_socket, addr = server_socket.accept()
        print(f'Connection from {addr}')
        data = client_socket.recv(1024)
        if data:
            with open('local_files/received_data.txt', 'a') as f:
                f.write(data.decode() + '\n')
        client_socket.close()

if __name__ == '__main__':
    start_server()
