# Test edge cases (e.g., empty files, malformed data, network issues).
# Consider additional logging for better debugging.
# If scalability is needed, look into asyncio instead of threading.

import matplotlib.pyplot as plt
import pandas as pd
import time
import socket
import threading
import os

triggers_to_view = 7
log_file_path = 'local_files/received_data.txt'

os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

# Function to read the last 10 lines of the log file and parse the data
def read_log_file(file_path):
    try:
        times, states = [], []
        lines_to_read = -triggers_to_view * 2 - 1

        with open(file_path, 'r') as file:
            lines = file.readlines()[lines_to_read:] # Use deque from collections for better performance if file size grows.
            for line in lines:
                try:
                    parts = line.strip().split('::')
                    time_in_ms = int(parts[2])
                    state = parts[1]
                    times.append(time_in_ms)
                    states.append(1 if state == 'high' else 0)
                except (IndexError, ValueError):
                    continue  # Skip malformed lines
        return times, states
    except FileNotFoundError:
        print("Log file not found.")
        return [], []


# Function to plot the graph with zoom and scroll functionality
def plot_graph(file_path):
    plt.ion()
    fig, ax = plt.subplots(figsize=(12, 6))
    line, = ax.plot([], [], drawstyle='steps-post', color='red', linewidth=4)

    ax.set_xlabel('Time (ms)')
    ax.set_ylabel('Signal State')
    ax.set_title('Signal High/Low States Over Time')
    plt.grid(True)

    while True:
        times, states = read_log_file(file_path)
        if times and states:
            line.set_data(times, states)
            ax.relim()
            ax.autoscale_view()
        plt.pause(1)


# Function to start the server
server_running = True  # Add a global flag

def start_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', port))
    server_socket.listen(1)
    print(f"Server listening on port {port}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")
        try:
            data = client_socket.recv(1024)
            if data:
                print(f"Received data: {data.decode()}")
                with open('local_files/received_data.txt', 'a') as f:
                    f.write(data.decode() + '\n')
        except Exception as e:
            print(f"Error receiving data: {e}")
        finally:
            client_socket.close()



# Main function to run the server and display the graph
def main():
    log_file_path = 'local_files/received_data.txt'  # Replace with the path to your log file
    port = 6781

    # Start the server in a separate thread
    server_thread = threading.Thread(target=start_server, args=(port,))
    server_thread.daemon = True
    server_thread.start()

    # Start plotting the graph
    plot_graph(log_file_path)

if __name__ == '__main__':
    main()
