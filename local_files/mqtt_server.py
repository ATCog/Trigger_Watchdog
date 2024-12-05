import paho.mqtt.client as mqtt
import time

# Define the MQTT broker and topic
broker = "192.168.0.30"
topic = "test/topic"
log_file = "mqtt_log.txt"

# Callback function when a message is received
def on_message(client, userdata, message):
    msg = message.payload.decode()
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    log_entry = f"{timestamp} - {message.topic}: {msg}\n"
    print(log_entry)
    with open(log_file, 'a') as file:
        file.write(log_entry)

# Set up the MQTT client
client = mqtt.Client()
client.on_message = on_message

# Connect to the broker and subscribe to the topic
client.connect(broker)
client.subscribe(topic)

# Start the MQTT client loop
client.loop_start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    client.loop_stop()
    client.disconnect()