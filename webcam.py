import os
import cv2
import time

#initialize camera
cam = cv2.VideoCapture(0)   #0 is the intenral integrated camera
time.sleep(1)

while True:
    check, frame = cam.read()
    
    cv2.imshow('Camera Video', frame)

    #keyboard push button detection for 'q'
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

cam.release()


print(check)
print(frame)
