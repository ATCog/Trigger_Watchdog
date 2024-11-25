import socket

addr = ('192.168.5.2', 6781)  # Replace with your PC's IP and port
s = socket.socket()
s.connect(addr)
s.send(b"Test message from Pico W")
s.close()
