from facedetection.send_emails import send_mail_test
import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import time
from scipy.spatial import distance as dist
from imutils.video import VideoStream
from imutils import face_utils
from threading import Thread

import pyglet
import argparse
import imutils

import dlib


# Face detection in Real Time detection
# First Step: Loading the known images files 
 
path = '../fd_database'
employee_images = []
employee_names = []
images_list = os.listdir(path)
# print(images_list)
for cl in images_list:
    curImg = cv2.imread(f'{path}/{cl}')
    employee_images.append(curImg)
    employee_names.append(os.path.splitext(cl)[0])
# print(employee_names)

# Getting the encodings for the known faces 
def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

def face_comparison(train_encode,test_encode):
    # Fourth step: Comaring between the the test image and train image measurements
    results = face_recognition.compare_faces(train_encode,test_encode)
    return results
print(face_comparison([findEncodings(employee_images)[0]],findEncodings(employee_images)[0]))

# Drowsy Detection:
def sound_alarm(path):
    music = pyglet.resource.media("alarm.wav")
    music.play()
    pyglet.app.run()

def eye_aspect_ratio(eye):
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    # print (ear)
    return ear

ap = argparse.ArgumentParser()

ap.add_argument("-w", "--webcam", type=int, default=0,
	help="index of webcam on system")
ap.add_argument("-a", "--alarm", type=int, default=0,
 	help="path alarm .WAV file")               
args = vars(ap.parse_args())

EYE_THRESHOLD = 0.3
EYE_CONSEC_FRAMES = 10

COUNTER = 0
ALARAM = False

print("[INFO] loading facial landmark predictor...")
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("facedetection/68_face_landmarks.dat")

(left_Start, left_End) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(right_Start, right_End) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

print( "[INFO] starting video thread ..")

# sleep_times=0
def drwosy(imgS,sleep_times=0):
    rects = detector(imgS, 0)
    for rect in rects:
        shape = predictor(imgS, rect)
        shape = face_utils.shape_to_np(shape)
        leftEye = shape[left_Start:left_End]
        rightEye = shape[right_Start:right_End]
        leftEAR = eye_aspect_ratio(leftEye)
        rightEAR = eye_aspect_ratio(rightEye)
        ear = (leftEAR + rightEAR) / 2.0
        leftEyeHull = cv2.convexHull(leftEye)
        rightEyeHull = cv2.convexHull(rightEye)
        # cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
        # cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)
        if ear < EYE_THRESHOLD:
            COUNTER += 1
            if COUNTER >= EYE_CONSEC_FRAMES:
                
                if not ALARAM:
                    ALARAM = True
                    # t = Thread(target=sound_alarm,args=(args["alarm"],))
                    # t.deamon = True
                    # t.start()
                    print('alarm')
                    COUNTER = 0
                    sleep_times+=1
                    if sleep_times == 4:
                        print('send email')
                        sleep_times =0 
                cv2.putText(imgS, "DROWSINESS ALERT!", (10, 30),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                cv2.putText(imgS, f"sleep times={sleep_times}", (100,70),cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        else:
                        COUNTER = 0
                        ALARAM = False  
        cv2.putText(imgS, "EAR: {:.2f}".format(ear), (300, 30),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    return imgS

def detection_real_time():
    Keyboard=KeyboardInterrupt()
    encodeListKnown = findEncodings(employee_images)
    print('Encoding Complete')
    cap = cv2.VideoCapture(0)
    counter=0
   
    while cap.isOpened():
        success, img = cap.read()
        
        
        imgS = cv2.resize(img,(0,0),None,0.25,0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
        # The Second Step: Get the face location fpr each face in each image. 
        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS,facesCurFrame)
         # The Third step: Get the face encodings,for each face in each image file . 
        for encodeFace,faceLoc in zip(encodesCurFrame,facesCurFrame):
            results = face_comparison(encodeListKnown,encodeFace)
            face_dis = face_recognition.face_distance(encodeListKnown,encodeFace)
            
            matchIndex = np.argmin(face_dis)

            if results[matchIndex]:
                name = employee_names[matchIndex].upper()
                
                y1,x2,y2,x1 = faceLoc
                y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4
                cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
                cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
                cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
                print("Hi",name)
                drwosy(imgS)
               
            else:
                print(results[matchIndex])
               
        # To show the images            
        cv2.imshow('Face Recognition',img)
        # The time lag 
        # cv2.waitKey(1) 
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
        
     
    cap.release()

if __name__== '__main__':

   detection_real_time()