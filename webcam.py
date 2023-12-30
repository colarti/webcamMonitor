import os
import cv2
import time
from sendMessage import send_email
from pathlib import Path
from threading import Thread


def delete_folder(folder):
    files = os.listdir(folder)
    for file in files:
        os.remove(f'{folder}\\{file}')

def check_for_images():
    if 'images' in os.listdir():
        pass
    else:
        os.mkdir('images')


#initialize camera
cam = cv2.VideoCapture(0)   #0 is the intenral integrated camera
time.sleep(1)

first_frame = None
status_list = list()
idx = 1

dir = 'C:\\Users\\cmola\\OneDrive\\Documents\\Python\\55_UDemy_60MegaApps\\App9-WebcamMonitor\\webcamMonitor'
os.chdir(dir)
check_for_images()

while True:
    status = 0
    check, frame = cam.read()
    
    file = f'{dir}\\images\\img{idx}.png'

    grey_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    grey_frame_gau = cv2.GaussianBlur(grey_frame, (11, 11), 0)

    if first_frame is None:
        first_frame = grey_frame_gau
    else:
        diff_frame = cv2.absdiff(first_frame, grey_frame_gau)
        thresh_frame = cv2.threshold(diff_frame, 40, 255, cv2.THRESH_BINARY)[1]
        dilate_frame = cv2.dilate(thresh_frame, None, iterations=2)

        contours, chk = cv2.findContours(dilate_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        day = time.strftime('%A')
        date = time.strftime('%Y-%m-%d')
        tm = time.strftime('%H:%M:%S')

        cv2.putText(frame, text=day, org=(30,30), fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1,
                    color=(255,255,255), thickness=1, lineType=cv2.LINE_AA)

        cv2.putText(frame, text=date, org=(30,50), fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1,
                    color=(255,255,0), thickness=1, lineType=cv2.LINE_AA)
        
        cv2.putText(frame, text=tm, org=(30,70), fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1,
                    color=(255,0,0), thickness=1, lineType=cv2.LINE_AA)

        for contour in contours:
            if cv2.contourArea(contour) < 5000:
                continue
            x,y,w,h = cv2.boundingRect(contour)
            rectangle = cv2.rectangle(frame, (x,y), (x+w,y+h), (0, 255, 0), 3)
            if rectangle.any():
                status = 1
                cv2.imwrite(file, frame)
                idx += 1
    
        status_list.append(status)  # detecting motion or no motion
        status_list = status_list[-2:]  # just capture the last values

        file_pick = None
        if status_list[0] == 1 and status_list[1] == 0: #this tracks when an object is detected then leaves the scene
            image_list = os.listdir('.\\images\\')
            while file_pick not in image_list:
                file_pick = image_list[len(image_list)//2]
                print(f'file_pick: {file_pick}')

            file_image = f'images\\{file_pick}'
            email_thread = Thread(target=send_email, args=(file_image,))
            email_thread.daemon = True
            delete_thread = Thread(target=delete_folder, args=('images',))
            delete_thread.daemon = True
            idx = 1

            email_thread.start()
            
        cv2.imshow('Camera Video', frame)

    #keyboard push button detection for 'q'
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

cam.release()
delete_thread.start()
