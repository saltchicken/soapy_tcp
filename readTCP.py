import socket
import numpy as np
import time
import zmq

TCP_IP = '192.168.1.46'
TCP_PORT = 1234

context = zmq.Context()
socket = context.socket(zmq.PAIR)
socket.connect('tcp://{}:{}'.format(TCP_IP, TCP_PORT))

RECEIVED = 0

try:
    while True:
        data = socket.recv()
        print(len(data))
        if not data: print('no data') # break
        data = np.frombuffer(data, np.complex64)
        RECEIVED += 1
        # time.sleep(.1)
        # print('Received data:', data)
        # print(data.size)
except KeyboardInterrupt:
    print("Breaking loop")
    socket.send_string('quit')

print(RECEIVED)
# header = s.recv(12)
# print(header)
# data = s.recv(1024)
# print(data)
# print(np.frombuffer(data, dtype=np.float64))

