import threading
import time
import numpy as np
import cv2
from collections import deque


class camera(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.__cap = cv2.VideoCapture("/dev/video2")
        self.__q = deque(maxlen=1)

    def run(self):
        while(True):
            ret, frame = self.__cap.read()
            self.__q.append(frame)

    def grab(self):
        if len(self.__q) > 0:
            img = self.__q.popleft()
            return True, img
        return False, None

    def release(self):
        self.__cap.release()
