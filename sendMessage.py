import smtplib, requests, ssl
from email.message import EmailMessage
import os
import imghdr

def send_email(img):
    host = 'smtp.gmail.com'
    port = 587

    uname = 'learnpython407@gmail.com'
    pw = os.getenv('WEBCAM_API_KEY')

    receiver = 'learnpython407@gmail.com'
    context = ssl.create_default_context()

    # print(os.getcwd())

    # os.chdir('.\\App9-WebcamMonitor\\webcamMonitor\\')

    print(os.getcwd())

    message = EmailMessage()
    message['Subject'] = 'Motion Detected'
    message.set_content('Something new was detected')
    
    with open(img, 'rb') as f:
        content = f.read()
    
    message.add_attachment(content, maintype='image', subtype=imghdr.what(None, content))

    # with smtplib.SMTP_SSL(host, port, context=context) as server:
    #     server.login(uname, pw)
    #     server.sendmail(uname, receiver, message)

    gmail = smtplib.SMTP(host, port)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(uname, pw)
    gmail.sendmail(uname, receiver, message.as_string())
    gmail.quit()


if __name__ == '__main__':
    send_email('.\\images\\img11.png')