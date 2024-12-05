import os
import time
import uasyncio as asyncio
from machine import Pin
from time import sleep, ticks_ms
import machine
import network
from umqtt.simple import MQTTClient

import WiFi 

machine.freq(270000000)

# Hyper Variables
# Debounce time in milliseconds
debounce_time = 0

# MQTT Configuration
MQTT_BROKER = '192.168.0.30'  # Replace with the IP address of your PC
MQTT_TOPIC = 'trigger/data'
MQTT_CLIENT_ID = 'pi_pico_w'

# WiFi Configuration
static_ip = '192.168.0.95'
WiFi.connect_to_wifi(static_ip)

# Function to write a new line to the log file
# def write_log(message):
#     try:
#         timestamp = time.localtime()
#         formatted_time = "{:04}-{:02}-{:02} {:02}:{:02}:{:02}".format(
#             timestamp[0], timestamp[1], timestamp[2], timestamp[3], timestamp[4], timestamp[5]
#         )
#         with open("log.txt", "a") as log_file:
#             log_file.write(f"{formatted_time}::{message}\n")
#     except Exception as e:
#         print(f"Error writing to log file: {e}")

# def start_test():
#     write_log("")
#     write_log("----------------------------------------")
#     write_log("Test Start")
#     write_log("----------------------------------------")
#     write_log("")
    
# def end_test():
#     write_log("")
#     write_log("----------------------------------------")
#     write_log("Test End")
#     write_log("----------------------------------------")
#     write_log("")

# Define the button pin
photo_eye_pin = Pin(14, Pin.IN)

# Variables to store the last state and time
last_state = photo_eye_pin.value()
last_time = ticks_ms()

# Function to log state changes
def log_state_change(pin):
    global last_state, last_time
    timestamp = time.localtime()
    formatted_time = "{:04}-{:02}-{:02} {:02}:{:02}:{:02}".format(
        timestamp[0], timestamp[1], timestamp[2], timestamp[3], timestamp[4], timestamp[5]
    )
    current_time = ticks_ms()
    if current_time - last_time > debounce_time:
        current_state = pin.value()
        if current_state != last_state:
            state = 'high' if current_state else 'low'
            print(f"PE {state} at {current_time} ms")
            string_to_send = f"{formatted_time}::{state}::{current_time}"
            # send_data(string_to_send.encode())
            send_mqtt(string_to_send.encode())
            last_state = current_state
            last_time = current_time

# Attach an interrupt to the button pin
photo_eye_pin.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=log_state_change)

# Function to send data to MQTT server
def send_data(data):
    try:
        print("Attempting to send data to MQTT...")
        client.publish(MQTT_TOPIC, data)
        print(f"Data sent to MQTT: {data}")
    except Exception as e:
        print(f"Error sending data to MQTT: {e}")

def send_mqtt(data):
    # Connect to MQTT broker
    client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER)
    client.connect()
    # Publish message
    client.publish(MQTT_TOPIC, data)
    print(f'Message "{data}" sent to topic "{MQTT_TOPIC}"')



# # Connect to MQTT server
# client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT)
# client.connect()

# start_test()

async def main():
    try:
        while True:
            await asyncio.sleep(1)  # Sleep to reduce CPU usage
    except KeyboardInterrupt:
        print("Program stopped")
    finally:
        # end_test()
        print("end_test() called")

# Run the main loop
async def run():
    await asyncio.gather(main())

# Start the asyncio event loop
asyncio.run(run())