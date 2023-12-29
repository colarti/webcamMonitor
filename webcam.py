import os
import cv2
import time
from sendMessage import send_email


#initialize camera
cam = cv2.VideoCapture(0)   #0 is the intenral integrated camera
time.sleep(1)

first_frame = None
status_list = list()
while True:
    status = 0
    check, frame = cam.read()
    grey_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    grey_frame_gau = cv2.GaussianBlur(grey_frame, (11, 11), 0)

    if first_frame is None:
        first_frame = grey_frame_gau
    else:
        diff_frame = cv2.absdiff(first_frame, grey_frame_gau)
        thresh_frame = cv2.threshold(diff_frame, 40, 255, cv2.THRESH_BINARY)[1]
        dilate_frame = cv2.dilate(thresh_frame, None, iterations=2)

        contours, chk = cv2.findContours(dilate_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            if cv2.contourArea(contour) < 5000:
                continue
            x,y,w,h = cv2.boundingRect(contour)
            rectangle = cv2.rectangle(frame, (x,y), (x+w,y+h), (0, 255, 0), 3)
            if rectangle.any():
                status = 1
    
        status_list.append(status)  # detecting motion or no motion
        status_list = status_list[-2:]  # just capture the last values

        if status_list[0] == 1 and status_list[1] == 0: #this tracks when an object is detected then leaves the scene
            send_email(frame)

        cv2.imshow('Camera Video', frame)





    #keyboard push button detection for 'q'
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

cam.release()


print(check)
print(frame)
