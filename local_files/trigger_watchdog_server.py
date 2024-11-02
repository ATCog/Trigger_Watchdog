import matplotlib.pyplot as plt
import pandas as pd
import time
import socket
import threading

# Function to read the last 10 lines of the log file and parse the data
def read_log_file(file_path):
    times = []
    states = []
    
    with open(file_path, 'r') as file:
        lines = file.readlines()[-10:]  # Read only the last 10 lines
        for line in lines:
            parts = line.strip().split('::')
            time_in_ms = int(parts[2])
            state = parts[1]
            times.append(time_in_ms)
            states.append(1 if state == 'high' else 0)
    
    return times, states

# Function to plot the graph with zoom and scroll functionality
def plot_graph(file_path):
    plt.ion()  # Turn on interactive mode
    fig, ax = plt.subplots(figsize=(12, 6))
    
    while True:
        times, states = read_log_file(file_path)
        
        # Clear the previous plot
        ax.clear()
        
        # Create a DataFrame for easier plotting
        df = pd.DataFrame({'Time (ms)': times, 'State': states})
        
        # Plot the signal graph with linear time on the X axis and correct scaling for time intervals
        ax.plot(df['Time (ms)'], df['State'], drawstyle='steps-post')
        ax.set_xlabel('Time (ms)')
        ax.set_ylabel('Signal State')
        ax.set_title('Signal High/Low States Over Time')
        plt.xticks(rotation=45)
        plt.grid(True)
        
        # Draw the updated plot
        plt.tight_layout()
        plt.draw()
        
        # Pause to allow the plot to update
        plt.pause(1)

# Function to start the server
def start_server(port):
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
