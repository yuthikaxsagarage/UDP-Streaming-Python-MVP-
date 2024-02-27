import cv2
from threading import Thread, Lock
import time


import utils

class VideoGrabber(Thread):

    def __init__(self, jpeg_quality):

        Thread.__init__(self)
        self.cap = cv2.VideoCapture(0)

        self.running = True
        self.buffer = None
        self.lock = Lock()
        self.jpeg_encode_func = lambda img, jpeg_quality=jpeg_quality: utils.cv2_encode_image(img, jpeg_quality)

    def stop(self):
        self.running = False

    def get_buffer(self):

        if self.buffer is not None:
            self.lock.acquire()
            cpy = self.buffer
            self.lock.release()
            return cpy

    def run(self):
        while self.running:
            success, img = self.cap.read()
            if not success:
                continue

            self.lock.acquire()
            self.buffer = self.jpeg_encode_func(img)
            self.lock.release()


if __name__ == '__main__':

    jpeg_quality = 100

    grabber = VideoGrabber(jpeg_quality)
    grabber.start()
    time.sleep(0.001)
    grabber.stop()

