from facedetection.send_emails import send_email
import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import time
from facedetection.drowsiness import drowsiness_detection
from imutils.video import VideoStream
# Face detection in Real Time detection
# First Step: Loading the known images files 
 
path = 'fd_database'
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
def detection_real_time():
    Keyboard=KeyboardInterrupt()
    encodeListKnown = findEncodings(employee_images)
    print('Encoding Complete')
    # cap = cv2.VideoCapture(0)
    cap = VideoStream(0).start()
    counter=0
    counter_sending=0
    flag=True
    while True:
        img = cap.read()
    
        #img = captureScreen() 
        imgS = cv2.resize(img,(0,0),None,0.25,0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
        # The Second Step: Get the face location fpr each face in each image. 
        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS,facesCurFrame)
         # The Third step: Get the face encodings,for each face in each image file . 
        
        for encodeFace,faceLoc in zip(encodesCurFrame,facesCurFrame):
            results = face_comparison(encodeListKnown,encodeFace)
            face_dis = face_recognition.face_distance(encodeListKnown,encodeFace)
            #print(faceDis)
            matchIndex = np.argmin(face_dis)

            if results[matchIndex]:
                flag=True
                name = employee_names[matchIndex].upper()
                #print(name)
                y1,x2,y2,x1 = faceLoc
                y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4
                cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
                cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
                cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
                print("Hi",name)
               
                counter+=1
                if counter==4:
                    # cap.stop()
                    sleep_time=drowsiness_detection(cap,name)
                    counter_sending+=1
                    if counter_sending>1:
                        img_name = "forsending.jpg"
                        cv2.imwrite(img_name, img)  
                        send_email("forsending.jpg",f"{name} status is drowsy")
                        counter_sending=0
                    counter=0
            elif flag:
                flag=False
                # print(results[matchIndex])

                img_name = "forsending.jpg"
                cv2.imwrite(img_name, img)    
                send_email("forsending.jpg",'There is Unauthorised access!')
                os.remove("forsending.jpg")
                # counter_sending=0    
        # To show the images            
        
        # The time lag 
        cv2.waitKey(1) 
        # if success == True:
        #     time.sleep(0)
    cap.release()

if __name__== '__main__':
   detection_real_time()