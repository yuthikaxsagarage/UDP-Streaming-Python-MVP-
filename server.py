#!/usr/bin/env python
# coding: utf-8

import socket
import cv2
import time
import logging
from timeit import default_timer as timer
class Broker():



    def __init__(self):
        logging.info('Initializing Broker')
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_address = ('', 5000)
        self.sock.bind(self.server_address)
        self.clients_list = []

    def talkToClient(self):

        frame_idx = 0
        buffer_array = []
        t0 = time.time()
        broadcast_frame_idx = 0

        while True:

            data, address = self.sock.recvfrom(65507)

            if data == b'0':
                print('requested from army')
                self.sock.sendto(buffer_array[len(buffer_array) - 1], address)
                broadcast_frame_idx += 1
            elif len(data) > 10000:
                print('requested from camera')
                #self.sock.sendto("from server saying hello to camera".encode('utf-8'), address)
                buffer_array.append(data)

                cv2.waitKey(1)
            else:
                self.sock.sendto("kaduna".encode('utf-8'), address)

            logging.info("Sending 'ok' to %s", address)


if __name__ == '__main__':
    # Make sure all log messages show up
    logging.getLogger().setLevel(logging.DEBUG)

    b = Broker()
    b.talkToClient()

