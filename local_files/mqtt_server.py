import paho.mqtt.client as mqtt
import pandas as pd

# Initialize an empty DataFrame to store the received data
df = pd.DataFrame(columns=['timestamp', 'topic', 'message'])

# Callback when a message is received
def on_message(client, userdata, msg):
    global df
    timestamp = pd.Timestamp.now()
    topic = msg.topic
    message = msg.payload.decode()
    print(f"Received message: {message} on topic: {topic} at {timestamp}")
    
    # Append the received data to the DataFrame
    df = df.append({'timestamp': timestamp, 'topic': topic, 'message': message}, ignore_index=True)

# Create an MQTT client instance
client = mqtt.Client()

# Assign the on_message callback function
client.on_message = on_message

# Connect to the broker
client.connect("localhost", 1883, 60)

# Subscribe to a topic
client.subscribe("trigger/data")

# Start the MQTT client loop
client.loop_start()

# Keep the script running
try:
    while True:
        pass
except KeyboardInterrupt:
    print("Exiting...")
    client.loop_stop()
    client.disconnect()
    print("Final DataFrame:")
    print(df)