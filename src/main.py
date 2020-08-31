import numpy as np
import cv2
from cap import camera

cam = camera()
cam.start()

while(True): 
    ret, frame = cam.grab()
    if ret:
        cv2.imshow('Original', frame) 
  
    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break
  
# Close the window / Release webcam 
cam.release() 
cv2.destroyAllWindows() 