# -*- coding: utf-8 -*-
"""
    Created on Thu Apr 11 01:48:57 2019
    @author: ANDRE
    """
#    import smbus
#    import numpy as np
#    import urllib.request
import cv2
import pygame
import time
#    import os
#    import math
#    import requests
#    import json

# Code to create the Accelerometer Module and obtain data from its.
# class MMA7455():
#     bus = smbus.SMBus(1)
#     def __init__(self):
#         self.bus.write_byte_data(0x1D, 0x16, 0x55) # Setup the Mode
#         self.bus.write_byte_data(0x1D, 0x10, 0) # Calibrate
#         self.bus.write_byte_data(0x1D, 0x11, 0) # Calibrate
#         self.bus.write_byte_data(0x1D, 0x12, 0) # Calibrate
#         self.bus.write_byte_data(0x1D, 0x13, 0) # Calibrate
#         self.bus.write_byte_data(0x1D, 0x14, 0) # Calibrate
#         self.bus.write_byte_data(0x1D, 0x15, 0) # Calibrate
#     def getValueX(self):
#         return self.bus.read_byte_data(0x1D, 0x06)
#     def getValueY(self):
#         return self.bus.read_byte_data(0x1D, 0x07)
#     def getValueZ(self):
#         return self.bus.read_byte_data(0x1D, 0x08)
# #Audio File attached in the repository or hackster page
file = 'b.mp3'
# Initialization of pygame to play audio.
pygame.init()
pygame.mixer.init()
# The haarcascades are attached in the respository and hackster tutorial.
face_cascade = cv2.CascadeClassifier(
    'haarcascade/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade/haarcascade_eye.xml')
# Input Camera Source.
cap = cv2.VideoCapture(0)
# Url to send data to Soracom and Obtain Location
url = 'http://funnel.soracom.io'
send_url = 'http://freegeoip.net/json'
# Count Variables
nf = 1  # Number of Faces
ne = 1  # Number of Eyes
count = 0  # Special Counter
# mma = MMA7455()
# Memory X,Y and Z values to compare
#    xmem=mma.getValueX()
#    ymem=mma.getValueY()
#    zmem=mma.getValueZ()
# Converting signed byte values to unsigned byte
# if(xmem > 127):
#     xmem=xmem-255
# if(ymem > 127):
#     ymem=ymem-255
# if(zmem > 127):
#     zmem=zmem-255

# Seed Time values
time1 = time.time()
time2 = time.time()

while 1:
    # x = mma.getValueX()
    # y = mma.getValueY()
    # z = mma.getValueZ()
    # if(x > 127):
    #     x=x-255
    # if(y > 127):
    #     y=y-255
    # if(z > 127):
    #     z=z-255

    # We need compare the memory value and the actual value to determine the acceleration, if the acceleration is more than 10, we determine the car crash, you can adjust this value for your convenience.
    # if(abs(xmem-x)>10):
    #     print('crash')
    #     # to obtain our location we send a request to "send_url" url to obtain our position
    #     r = requests.get(send_url)
    #     j = json.loads(r.text)
    #     # We convert json to string
    #     lat = j['latitude']
    #     lon = j['longitude']
    #     # We create the payload and headers
    #     payload = '{"deviceid" : "Car 0001",    "lat" : lat, "lon" :lon}'
    #     headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
    #     # We send to soracom the notification
    #     r = requests.post(url, data=payload, headers=headers)
    #     exit()
    # if(abs(ymem-y)>10):
    #     print('crash')
    #     # to obtain our location we send a request to "send_url" url to obtain our position
    #     r = requests.get(send_url)
    #     j = json.loads(r.text)
    #     # We convert json to string
    #     lat = j['latitude']
    #     lon = j['longitude']
    #     # We create the payload and headers
    #     payload = '{"deviceid" : "Car 0001",    "lat" : lat, "lon" :lon}'
    #     headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
    #     # We send to soracom the notification
    #     r = requests.post(url, data=payload, headers=headers)
    #     exit()

    # if(abs(zmem-z)>10):
    #     print('crash')
    #     # to obtain our location we send a request to "send_url" url to obtain our position
    #     r = requests.get(send_url)
    #     j = json.loads(r.text)
    #     # We convert json to string
    #     lat = j['latitude']
    #     lon = j['longitude']
    #     # We create the payload and headers
    #     payload = '{"deviceid" : "Car 0001",    "lat" : lat, "lon" :lon}'
    #     headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
    #     # We send to soracom the notification
    #     r = requests.post(url, data=payload, headers=headers)
    #     exit()

    # We obtain an image from our source of images (in this case the camera)
    ret, img = cap.read()
    # through the following algorithm we get the number of faces and eyes that the camera can see
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray, 1.3, 40)
        ne = len(eyes)
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey),
                            (ex+ew, ey+eh), (0, 255, 0), 2)
    # Since we have the number of faces we will check that the algorithm can see at least one face and at least one open eye, if it is able to see a face and does not detect any open eye, after 3 seconds it will start to sound an annoying noise that will wake up to the condutor
    nf = len(faces)
    if (nf > 0 and ne < 1):
        time1 = time.time()
        print(time1-time2)
        if ((time1-time2) >= 3):
            pygame.mixer.music.load(file)
            pygame.mixer.music.play()
    else:
        pygame.mixer.music.stop()
        time1 = time.time()
        time2 = time1
    cv2.imshow('img', img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cv2.destroyAllWindows()
