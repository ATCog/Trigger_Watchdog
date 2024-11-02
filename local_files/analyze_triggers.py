import matplotlib.pyplot as plt
import pandas as pd

# Function to read the log file and parse the data
def read_log_file(file_path):
    times = []
    states = []
    
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split('::')
            time_in_ms = int(parts[2])
            state = parts[1]
            times.append(time_in_ms)
            states.append(1 if state == 'high' else 0)
    
    return times, states

# Function to plot the graph with zoom and scroll functionality
def plot_graph(file_path):
    times, states = read_log_file(file_path)
    
    # Create a DataFrame for easier plotting
    df = pd.DataFrame({'Time (ms)': times, 'State': states})
    
    # Plot the signal graph with linear time on the X axis and correct scaling for time intervals
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(df['Time (ms)'], df['State'], drawstyle='steps-post')
    ax.set_xlabel('Time (ms)')
    ax.set_ylabel('Signal State')
    ax.set_title('Signal High/Low States Over Time')
    plt.xticks(rotation=45)
    plt.grid(True)
    
    # Enable zoom and scroll functionality
    plt.tight_layout()
    plt.show()

# Example usage
log_file_path =  'C:/Users/athompso/OneDrive - Cognex Corporation/Work Main/.Internal/Trigger_Watchdog/local_files/received_data.txt'  # Replace with the path to your log file
plot_graph(log_file_path)
