import os
import cv2
import time

#initialize camera
cam = cv2.VideoCapture(0)   #0 is the intenral integrated camera

while True:
    check, frame = cam.read()
    # time.sleep(1)

    cv2.imshow('Camera Video', frame)

    key = cv2.waitKey(1)

    if key == ord('q'):
        break

cam.release()


print(check)
print(frame)
