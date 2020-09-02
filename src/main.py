import numpy as np
import cv2
from cap import camera
import time

cam = camera()
cam.setDaemon(True)
cam.start()
prev = None
img = np.zeros([960,1280,3],dtype=np.uint8)

out_pipe = "appsrc ! video/x-raw,width=1280,height=960,framerate=10/1 ! videoconvert ! timeoverlay xpad=100 ypad=100 ! autovideosink sync=false"
out = cv2.VideoWriter(out_pipe, 0, 10.0, (1280,960))
while(True): 
    ret, frame = cam.grab()
    if not ret:
        continue
    # prev = frame.copy()
    img[0:480,0:640,:] = frame
    img[480:,640:,:] = frame
    out.write(img)
    if ret:
        pass
        # cv2.imshow('Original', img) 
  
    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break
    time.sleep(1/10)
# Close the window / Release webcam 
cam.release() 
out.release()
cv2.destroyAllWindows() 