import numpy as np
import cv2
from cap import camera
import time

cam = camera()
cam.setDaemon(True)
cam.start()
prev = None
img = np.zeros([960,1280,3],dtype=np.uint8)
while(True): 
    ret, frame = cam.grab()
    if not ret:
        continue
    # prev = frame.copy()
    img[0:480,0:640,:] = frame
    img[480:,640:,:] = frame
    if ret:
        cv2.imshow('Original', img) 
  
    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break
    time.sleep(1/10)
# Close the window / Release webcam 
cam.release() 
cv2.destroyAllWindows() 