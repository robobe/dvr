import threading
import time
import numpy as np
import cv2
import traceback
from collections import deque


class camera(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.__cap = None
        self.__q = deque(maxlen=1)
        self.__tmp_img = np.ones([480,640,3],dtype=np.uint8)

    def run(self):
        name = "/dev/video2"
        while True:
            try:
                self.__cap = cv2.VideoCapture(name)
                try:
                    while(True):
                        ret, frame = self.__cap.read()
                        if not ret:
                            frame = self.__tmp_img
                        self.__q.append(frame)
                except:
                    print(traceback.format_exc())
                    self.__cap.release()
                time.sleep(1)
            except:
                print(traceback.format_exc())
                time.sleep(1)
                name = "/dev/video3"


    def grab(self):
        if len(self.__q) > 0:
            img = self.__q.popleft()
            return True, img
        return False, None

    def release(self):
        self.__cap.release()
