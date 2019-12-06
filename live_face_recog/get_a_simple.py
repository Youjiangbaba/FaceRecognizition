#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2

import argparse



parser = argparse.ArgumentParser()
parser.add_argument('Capture_string', help='0 王小二 0012')
parser.add_argument('name_string', help='example:0 王小二 0012')
parser.add_argument('number_string', help='example:0 王小二 0012')
args = parser.parse_args()

face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
if len(args.Capture_string) == 1:   #摄像头读取
	args.Capture_string = ord(args.Capture_string) - ord('0')

cap = cv2.VideoCapture(args.Capture_string)
flag = 0
while True:
    ret,img = cap.read()

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray, 1.3, 5)
 
    for (x,y,w,h) in faces:
        flag = 1
        cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)     
        face = img[y:y+h,x:x+w].copy()

    cv2.imshow("img",img)

    key = cv2.waitKey(50)
    if key == 27:
        if flag == 1:
            cv2.imwrite("./img/face_recognition/"+args.name_string+'_'+ args.number_string+'.png',face)
            print ("having saved")
            cv2.imshow("face",face)
            flag = 0
            break

cv2.waitKey(0)
cap.release()
cv2.destroyAllWindows()
