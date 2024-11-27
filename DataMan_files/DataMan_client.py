import socket
import pandas as pd
import json

def tcp_client(host, port):
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = (host, port)
    print(f"Connecting to {server_address}")
    sock.connect(server_address)

    try:
        while True:
            # Receive data from the server
            data = sock.recv(1024)
            if data:
                # Decode the data and print it
                decoded_data = data.decode('utf-8')
                print(f"Received: {decoded_data}")

                # Remove any non-JSON characters if necessary
                json_data = decoded_data.strip('☻♥')

                # Check if the data is valid JSON
                try:
                    data_dict = json.loads(json_data)
                    # Append the dictionary to the DataFrame
                    df = pd.DataFrame([data_dict])
                    # Open the CSV file in append mode and write the DataFrame
                    with open('received_data.csv', 'a', newline='') as f:
                        df.to_csv(f, header=f.tell()==0, index=False)
                except json.JSONDecodeError:
                    print("Received data is not valid JSON")
            else:
                break
    finally:
        print("Closing connection")
        sock.close()

# Example usage
tcp_client('192.168.0.31', 10000)
