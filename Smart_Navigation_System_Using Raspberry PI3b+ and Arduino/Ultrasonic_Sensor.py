import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import RPi.GPIO as GPIO
import time
import ultr1 as u
import ultr2 as t
import gps2
from sqliteDatabase import Database


# GPIO Mode (Board / BCM)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Set GPIO Pins
GPIO_TRIG = 6
GPIO_ECHO = 5
BUZZER_PIN = 4  # Assuming the buzzer is connected to GPIO pin 4

# Set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIG, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

def distance():
    """
    Calculate distance measured by the ultrasonic sensor.
    """
    GPIO.output(GPIO_TRIG, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIG, False)

    StartTime = time.time()
    StopTime = time.time()

    timeout = time.time() + 1  # 1 second timeout for the loop
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
        if time.time() > timeout:
            return float('inf')  # Indicate timeout
    
    timeout = time.time() + 1  # 1 second timeout for the loop
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
        if time.time() > timeout:
            return float('inf')  # Indicate timeout
    
    TimeElapsed = StopTime - StartTime
    distance = (TimeElapsed * 34300) / 2
    return distance

def buzz(pitch, duration):
    """
    Generate sound from the buzzer at the specified pitch and duration.
    """
    period = 1.0 / pitch
    delay = period / 2
    cycles = int(duration * pitch)
    for i in range(cycles):
        GPIO.output(BUZZER_PIN, GPIO.HIGH)
        time.sleep(delay)
        GPIO.output(BUZZER_PIN, GPIO.LOW)
        time.sleep(delay)

def play_buzzer(distance, distance2, distance3):
    """
    Control the buzzer based on the distances measured by the sensors.
    """
    buzzer_on = False
    if distance < 50:  # Adjust this threshold according to your needs
        buzzer_on = True
        buzz(1000, 0.1)
    if distance2 < 50:  # Adjust this threshold according to your needs
        buzzer_on = True
        buzz(1000, 0.1)
    if distance3 < 50:  # Adjust this threshold according to your needs
        buzzer_on = True
        buzz(1000, 0.1)

    if not buzzer_on:
        GPIO.output(BUZZER_PIN, GPIO.LOW)

def send_email_alert():
    sender_email = 'tshiamo846@gmail.com'
    receiver_emails = ['219019556@tut4life.ac.za', '219019556@tut4life.ac.za']  # Replace with actual emails
    subject = 'EMERGENCY from Smart Blind Navigation System Alert'
    body = 'Warning! All three ultrasonic sensors have detected a distance of less than 50 cm. IT IS AN EMERGENCY PLEASE ATTEND!'

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = ', '.join(receiver_emails)
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, 'xumtjycwhhigbott')
            text = msg.as_string()
            server.sendmail(sender_email, receiver_emails, text)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")


if __name__ == '__main__':
    db = Database('project_data.db')
    try:
        while True:
            dist = distance()
            dist2 = t.dist2()
            dist3 = u.dist1()
            print("ULTRASONIC ONE")
            print("Measured Distance = %.1f cm" % dist)
            print("ULTRASONIC TWO")
            print("Measured Distance = %.1f cm" % dist2)
            print("ULTRASONIC THREE")
            print("Measured Distance = %.1f cm" % dist3)
            play_buzzer(dist, dist2, dist3)
            
            # Insert data into the database and send email if all distances are less than 50 cm
            if dist < 50 or dist2 < 50 or dist3 < 50:
                
                if dist and 50 and dist2 < 50 and dist3 < 50:
                    if latitude and longitude:
                        db.insert_data(timestamp, dist, dist2, dist3, latitude, longitude, date)
                        send_email_alert()
                        print("Data inserted and email sent")
                    
                timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
                latitude, longitude, date = gps2.read_gps()
                if latitude and longitude:
                    db.insert_data(timestamp, dist, dist2, dist3, latitude, longitude, date)
                    print("Data inserted")
            time.sleep(1)

    except KeyboardInterrupt:
        print("Measurement stopped by User")
    finally:
        GPIO.cleanup()
        db.close()



# import os
# import cv2
# import numpy as np
# import RPi.GPIO as GPIO
# import time
# import ultr1 as u
# import ultr2 as t
# import gps2
# from sqliteDatabase import Database
# from object_detection_tflite import ObjectDetection
# 
# # GPIO Mode (Board / BCM)
# GPIO.setmode(GPIO.BCM)
# GPIO.setwarnings(False)
# 
# # Set GPIO Pins
# GPIO_TRIG = 3
# GPIO_ECHO = 2
# BUZZER_PIN = 4  # Assuming the buzzer is connected to GPIO pin 4
# 
# # Set GPIO direction (IN / OUT)
# GPIO.setup(GPIO_TRIG, GPIO.OUT)
# GPIO.setup(GPIO_ECHO, GPIO.IN)
# GPIO.setup(BUZZER_PIN, GPIO.OUT)
# 
# # Initialize Object Detection
# model_path = '/home/sipho/Desktop/Final_Project/detect.tflite'
# labels_path = '/home/sipho/Desktop/Final_Project/coco_labels.txt'
# object_detector = ObjectDetection(model_path, labels_path)
# 
# def distance():
#     """
#     Calculate distance measured by the ultrasonic sensor.
#     """
#     GPIO.output(GPIO_TRIG, True)
#     time.sleep(0.00001)
#     GPIO.output(GPIO_TRIG, False)
# 
#     StartTime = time.time()
#     StopTime = time.time()
# 
#     timeout = time.time() + 1  # 1 second timeout for the loop
#     while GPIO.input(GPIO_ECHO) == 0:
#         StartTime = time.time()
#         if time.time() > timeout:
#             return float('inf')  # Indicate timeout
#     
#     timeout = time.time() + 1  # 1 second timeout for the loop
#     while GPIO.input(GPIO_ECHO) == 1:
#         StopTime = time.time()
#         if time.time() > timeout:
#             return float('inf')  # Indicate timeout
#     
#     TimeElapsed = StopTime - StartTime
#     distance = (TimeElapsed * 34300) / 2
#     return distance
# 
# def buzz(pitch, duration):
#     """
#     Generate sound from the buzzer at the specified pitch and duration.
#     """
#     period = 1.0 / pitch
#     delay = period / 2
#     cycles = int(duration * pitch)
#     for i in range(cycles):
#         GPIO.output(BUZZER_PIN, GPIO.HIGH)
#         time.sleep(delay)
#         GPIO.output(BUZZER_PIN, GPIO.LOW)
#         time.sleep(delay)
# 
# def play_buzzer(distance, distance2, distance3):
#     """
#     Control the buzzer based on the distances measured by the sensors.
#     """
#     buzzer_on = False
#     if distance < 50:  # Adjust this threshold according to your needs
#         buzzer_on = True
#         buzz(1000, 0.1)
#     if distance2 < 50:  # Adjust this threshold according to your needs
#         buzzer_on = True
#         buzz(1000, 0.1)
#     if distance3 < 50:  # Adjust this threshold according to your needs
#         buzzer_on = True
#         buzz(1000, 0.1)
# 
#     if not buzzer_on:
#         GPIO.output(BUZZER_PIN, GPIO.LOW)
# 
# if __name__ == '__main__':
#     db = Database('project_data.db')
#     dataset_count = 0
# 
#     # Initialize video stream
#     cap = cv2.VideoCapture(0)
#     
#     try:
#         while cap.isOpened():
#             ret, frame = cap.read()
#             if not ret:
#                 break
# 
#             frame, detected_objects = object_detector.detect_objects(frame)
#             cv2.imshow('Object Detection', frame)
# 
#             dist = distance()
#             dist2 = t.dist2()
#             dist3 = u.dist1()
#             print("ULTRASONIC ONE")
#             print("Measured Distance = %.1f cm" % dist)
#             print("ULTRASONIC TWO")
#             print("Measured Distance = %.1f cm" % dist2)
#             print("ULTRASONIC THREE")
#             print("Measured Distance = %.1f cm" % dist3)
#             play_buzzer(dist, dist2, dist3)
#             
#             # Insert data into the database if any of the distances are less than 50 cm
#             if dist < 50 or dist2 < 50 or dist3 < 50:
#                 timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
#                 latitude, longitude, date = gps2.read_gps()
#                 if latitude and longitude:
#                     db.insert_data(timestamp, dist, dist2, dist3, latitude, longitude, date, detected_objects)
#                     dataset_count += 1
# 
#                     # Clear the database after 5 datasets
#                     if dataset_count >= 5:
#                         db.clear()
#                         dataset_count = 0
#             
#             if cv2.waitKey(1) & 0xFF == ord('q'):
#                 break
# 
#             time.sleep(1)
# 
#     except KeyboardInterrupt:
#         print("Measurement stopped by User")
#     finally:
#         cap.release()
#         cv2.destroyAllWindows()
#         GPIO.cleanup()
#         db.close()



# import RPi.GPIO as GPIO
# import time
# import ultr1 as u
# import ultr2 as t
# import gps2
# from sqliteDatabase import Database
# 
# # GPIO Mode (Board / BCM)
# GPIO.setmode(GPIO.BCM)
# GPIO.setwarnings(False)
# 
# # Set GPIO Pins
# GPIO_TRIG = 3
# GPIO_ECHO = 2
# BUZZER_PIN = 4  # Assuming the buzzer is connected to GPIO pin 4
# 
# # Set GPIO direction (IN / OUT)
# GPIO.setup(GPIO_TRIG, GPIO.OUT)
# GPIO.setup(GPIO_ECHO, GPIO.IN)
# GPIO.setup(BUZZER_PIN, GPIO.OUT)
# 
# def distance():
#     """
#     Calculate distance measured by the ultrasonic sensor.
#     """
#     GPIO.output(GPIO_TRIG, True)
#     time.sleep(0.00001)
#     GPIO.output(GPIO_TRIG, False)
# 
#     StartTime = time.time()
#     StopTime = time.time()
# 
#     timeout = time.time() + 1  # 1 second timeout for the loop
#     while GPIO.input(GPIO_ECHO) == 0:
#         StartTime = time.time()
#         if time.time() > timeout:
#             return float('inf')  # Indicate timeout
#     
#     timeout = time.time() + 1  # 1 second timeout for the loop
#     while GPIO.input(GPIO_ECHO) == 1:
#         StopTime = time.time()
#         if time.time() > timeout:
#             return float('inf')  # Indicate timeout
#     
#     TimeElapsed = StopTime - StartTime
#     distance = (TimeElapsed * 34300) / 2
#     return distance
# 
# def buzz(pitch, duration):
#     """
#     Generate sound from the buzzer at the specified pitch and duration.
#     """
#     period = 1.0 / pitch
#     delay = period / 2
#     cycles = int(duration * pitch)
#     for i in range(cycles):
#         GPIO.output(BUZZER_PIN, GPIO.HIGH)
#         time.sleep(delay)
#         GPIO.output(BUZZER_PIN, GPIO.LOW)
#         time.sleep(delay)
# 
# def play_buzzer(distance, distance2, distance3):
#     """
#     Control the buzzer based on the distances measured by the sensors.
#     """
#     buzzer_on = False
#     if distance < 50:  # Adjust this threshold according to your needs
#         buzzer_on = True
#         buzz(1000, 0.1)
#     if distance2 < 50:  # Adjust this threshold according to your needs
#         buzzer_on = True
#         buzz(1000, 0.1)
#     if distance3 < 50:  # Adjust this threshold according to your needs
#         buzzer_on = True
#         buzz(1000, 0.1)
# 
#     if not buzzer_on:
#         GPIO.output(BUZZER_PIN, GPIO.LOW)
# 
# if __name__ == '__main__':
#     db = Database('project_data.db')
#     try:
#         while True:
#             dist = distance()
#             dist2 = t.dist2()
#             dist3 = u.dist1()
#             print("ULTRASONIC ONE")
#             print("Measured Distance = %.1f cm" % dist)
#             print("ULTRASONIC TWO")
#             print("Measured Distance = %.1f cm" % dist2)
#             print("ULTRASONIC THREE")
#             print("Measured Distance = %.1f cm" % dist3)
#             play_buzzer(dist, dist2, dist3)
#             
#             # Insert data into the database if any of the distances are less than 50 cm
#             if dist > 50 or dist2 > 50 or dist3 > 50:
#                 timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
#                 latitude, longitude, date = gps2.read_gps()
#                 if latitude and longitude:
#                     db.insert_data(timestamp, dist, dist2, dist3, latitude, longitude, date)
#                     print("Data inserted")
#             time.sleep(1)
# 
#     except KeyboardInterrupt:
#         print("Measurement stopped by User")
#     finally:
#         GPIO.cleanup()
#         db.close()

