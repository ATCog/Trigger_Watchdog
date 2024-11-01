import os
import socket
import network
import secrets
import time

def is_port_free(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind(('0.0.0.0', port))
        s.close()
        return True
    except OSError:
        return False

def free_port(port):
    # Attempt to bind to the port to release it if it's in use
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind(('0.0.0.0', port))
        s.close()
        print(f"Port {port} is now free.")
    except OSError as e:
        print(f"Failed to free port {port}: {e}")
    time.sleep(1)  # Give it a moment to release the port

def connect_to_wifi(static_ip, subnet='255.255.255.0', gateway='192.168.1.1', dns='8.8.8.8', ssid=secrets.SSID, password=secrets.PASSWORD, port=80):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    # Configure the static IP
    wlan.ifconfig((static_ip, subnet, gateway, dns))
    
    # Connect to the Wi-Fi network
    wlan.connect(ssid, password)
    
    # Wait for connection
    max_wait = 10
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        print('Waiting for connection...')
        time.sleep(1)
    
    # Check if connected
    if wlan.status() != 3:
        raise RuntimeError('Wi-Fi connection failed')
    else:
        print('Connected')
        print('IP:', wlan.ifconfig()[0])
