# Birthday: 11/1/2024
import os
import time
import uasyncio as asyncio
from machine import Pin
from time import sleep, ticks_ms
import socket

import WiFi

# Hyper Variables
# Debounce time in milliseconds
debounce_time = 50
static_ip = '192.168.0.44'

WiFi.connect_to_wifi(static_ip)


# Function to write a new line to the log file
def write_log(message):
    timestamp = time.localtime()
    formatted_time = "{:04}-{:02}-{:02} {:02}:{:02}:{:02}".format(
        timestamp[0], timestamp[1], timestamp[2], timestamp[3], timestamp[4], timestamp[5]
    )
    with open("log.txt", "a") as log_file:
        log_file.write(f"{formatted_time}::{message}" + "\n")

def start_test():
    write_log("")
    write_log("----------------------------------------")
    write_log("Test Start")
    write_log("----------------------------------------")
    write_log("")
    
def end_test():
    write_log("")
    write_log("----------------------------------------")
    write_log("Test End")
    write_log("----------------------------------------")
    write_log("")

# Define the button pin
photo_eye_pin = Pin(14, Pin.IN, Pin.PULL_DOWN)

# Variables to store the last state and time
last_state = photo_eye_pin.value()
last_time = ticks_ms()

# Function to log state changes
def log_state_change(pin):
    global last_state, last_time
    current_time = ticks_ms()
    if current_time - last_time > debounce_time:
        current_state = pin.value()
        if current_state != last_state:
            state = 'high' if current_state else 'low'
            print(f"PE {state} at {current_time} ms")
            write_log(f"{state}::{current_time}")
            last_state = current_state
            last_time = current_time

# Attach an interrupt to the button pin
photo_eye_pin.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=log_state_change)

start_test()

async def web_server():
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket()
    s.bind(addr)
    s.listen(1)
    print('Listening on', addr)

    try:
        while True:
            cl, addr = s.accept()
            print('Client connected from', addr)
            request = cl.recv(1024)
            request = str(request)
            print('Request:', request)

            if 'GET /log.txt' in request:
                with open("log.txt", "r") as log_file:
                    lines = log_file.readlines()
                    last_20_lines = lines[-20:]  # Get the last 20 lines
                    log_content = "".join(last_20_lines)
                response = """HTTP/1.1 200 OK
Content-Type: text/plain

{}""".format(log_content)
            else:
                response = """HTTP/1.1 200 OK
Content-Type: text/html

<!DOCTYPE html>
<html>
<head>
    <title>Trigger Watchdog</title>
</head>
<body>
    <h1>Status</h1>
    <pre id="Status"></pre>
</body>
</html>
"""

            cl.send(response)
            cl.close()
    except Exception as e:
        print(f"Exception in web server: {e}")
    finally:
        s.close()
        print("Socket closed.")
    return s

async def main():
    server_socket = await web_server()  # Get the server socket
    try:
        while True:
            await asyncio.sleep(1)  # Sleep to reduce CPU usage
    except KeyboardInterrupt:
        print("Program stopped")
        server_socket.close()  # Close the server socket
        print("Server socket closed.")
    finally:
        end_test()
        print("end_test() called")

# Run the web server and main loop
async def run():
    await asyncio.gather(main())

# Start the asyncio event loop
asyncio.run(run())





