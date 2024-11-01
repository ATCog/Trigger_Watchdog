import os
import time
import uasyncio as asyncio
from machine import Pin
from time import sleep, ticks_ms

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

# Debounce time in milliseconds
debounce_time = 50

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

# Web server to display the log file
async def web_server():
    import socket
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket()
    s.bind(addr)
    s.listen(1)
    print('Listening on', addr)

    while True:
        cl, addr = s.accept()
        print('Client connected from', addr)
        request = cl.recv(1024)
        request = str(request)
        print('Request:', request)

        response = """HTTP/1.1 200 OK
Content-Type: text/html

<!DOCTYPE html>
<html>
<head>
    <title>Log Output</title>
</head>
<body>
    <h1>Log Output</h1>
    <pre>{}</pre>
</body>
</html>
""".format(open("log.txt").read())

        cl.send(response)
        cl.close()

# Main loop to keep the program running
async def main():
    try:
        while True:
            await asyncio.sleep(1)  # Sleep to reduce CPU usage
    except KeyboardInterrupt:
        print("Program stopped")
    finally:
        end_test()
        print("end_test() called")

# Run the web server and main loop
async def run():
    await asyncio.gather(web_server(), main())

# Start the asyncio event loop
asyncio.run(run())
