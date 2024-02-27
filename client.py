#!/usr/bin/env python
# coding: utf-8

import socket

import time
import argparse
import video_grabber

parser = argparse.ArgumentParser()

parser.add_argument('--host', type=str, help='The IP at the server is listening', required=True)
parser.add_argument('--port', type=int, help='The port on which the server is listening', required=True)
parser.add_argument('--jpeg_quality', type=int, help='The JPEG quality for compressing the reply', default=50)
parser.add_argument('--encoder', type=str, choices=['cv2','turbo'], help='Which library to use to encode/decode in JPEG the images', default='cv2')

args = parser.parse_args()

jpeg_quality = args.jpeg_quality
encoder = args.encoder


# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.settimeout(2.0)
host = args.host
port = args.port
server_address = (host, port)
# sock.bind(('127.0.0.1', 5000))

t0 = time.time()
frame_idx = 0
iter = 0

grabber = video_grabber.VideoGrabber(jpeg_quality)
grabber.start()
get_message = lambda: grabber.get_buffer()

while(True):
    iter += 1
    buffer = get_message()
    if buffer is None:
        continue
    if len(buffer) > 65507:
        print(
            "The message is too large to be sent within a single UDP datagram. We do not handle splitting the message in multiple datagrams")
        sock.sendto("FAIL".encode('utf-8'), server_address)

        continue
    sock.sendto(buffer, server_address)
    time.sleep(0.2)
    #try:
        #data, address = sock.recvfrom(65507)
    #except:
        #print('Timed out ', iter)


grabber.join()
sock.close()
