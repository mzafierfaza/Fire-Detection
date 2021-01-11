import cv2
import time, threading
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os.path

fire_cascade = cv2.CascadeClassifier('/home/pi/IPCAM/fire_detection.xml')
cap = cv2.VideoCapture("rtsp://192.168.43.75:554/unicast")

email = 'ipcamerafornotif@gmail.com'
password = 'akubaiknian'
send_to_email = 'zafierfazamuhammad@gmail.com'
subject = 'Api terdeteksi!'
message = 'Hai Nadila, Api telah terdeteksi. berikut gambarnya'
file_location = '/home/pi/IPCAM/api.jpg'


last = time.perf_counter()
current = last

def setup_email():
    global msg
    global filename
    global attachment
    global part
    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = send_to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain'))

    #Setup the attachment
    filename = os.path.basename(file_location)
    attachment = open(file_location, "rb")
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    # Attach the attachment to the MIMEMultipart object
    msg.attach(part)

def kirim_email():
    global server
    global text
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email, password)
    text = msg.as_string()
    server.sendmail(email, send_to_email, text)
    server.quit()


while True:
    
    current = time.perf_counter()
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    fire = fire_cascade.detectMultiScale(gray, 1.2, 5)
    for (x,y,w,h) in fire:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
        cv2.imwrite('/home/pi/IPCAM/api.jpg',frame)
        setup_email()
        if current - last > 5.:
            last = current
            print('Gambar Telah di Capture')
            kirim_email()
            print('Email Telah di Kirim---')
            

    cv2.imshow('Fire Detection',frame)    
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
