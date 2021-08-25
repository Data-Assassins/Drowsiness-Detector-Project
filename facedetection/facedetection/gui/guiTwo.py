# from facedetection.drowsiness import ALARAM
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt , QThread, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QPalette, QPixmap 
from PyQt5.QtWidgets import QApplication, QWidget ,QDialog,QTableWidgetItem,QMessageBox
from PyQt5 import QtWidgets ,QtGui
from PyQt5.uic import loadUi
import cv2
import numpy as np
from enum import auto
from re import U
from typing import Counter
from facedetection.send_emails import send_email
import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import time
from scipy.spatial import distance as dist
from imutils.video import VideoStream
from imutils import face_utils
from threading import Thread as audio_thread
import pyglet
import argparse
import imutils
import dlib
from facedetection.save_reprot import *
import csv


database={'admin': '1234','saadoun':'1234', 'haya': '1234', 'ali': '1234'}
path = 'fd_database'
employee_images = []
employee_names = []
def images_data():
    images_list = os.listdir(path)
    for cl in images_list:
        curImg = cv2.imread(f'{path}/{cl}')
        employee_images.append(curImg)
        employee_names.append(os.path.splitext(cl)[0])
    print("from images data")

EYE_THRESHOLD = 0.25
EYE_CONSEC_FRAMES = 30
print("[INFO] loading facial landmark predictor...")
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("facedetection/68_face_landmarks.dat")
(left_Start, left_End) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(right_Start, right_End) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

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
# print(face_comparison([findEncodings(employee_images)[0]],findEncodings(employee_images)[0]))


def eye_aspect_ratio(eye):
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    # print (ear)
    return ear

# intro page
class IntroPage(QDialog):
    def __init__(self):
        super().__init__()
        loadUi('facedetection/gui/guiIntro.ui', self)
        self.setWindowTitle('Face Detection')
        self.label.setFixedWidth(700)
        self.label.setFixedHeight(800)
        self.setFixedWidth(700)
        self.setFixedHeight(800)
        self.label.setStyleSheet("border-image: url(facedetection/gui/images/projectposter.png)")
        self.start.clicked.connect(self.start_clicked)

    def start_clicked(self):
        start = homeWindow()
        widget.addWidget(start)
        # to flip the screen to the login
        widget.setCurrentIndex(widget.currentIndex() + 1)



# Home page 
class homeWindow(QDialog):
    def __init__(self):
        super(homeWindow, self).__init__()
        loadUi('facedetection/gui/guiHome.ui', self)
        self.login.clicked.connect(self.login_clicked)
        self.signup.clicked.connect(self.signup_clicked)
        self.label.setFixedWidth(700)
        self.label.setFixedHeight(800)
        self.setFixedWidth(700)
        self.setFixedHeight(800)
        self.label.setStyleSheet("border-image: url(facedetection/gui/images/background.jpg)")
    # login function will link to the login class then we show the login screen
    def login_clicked(self):
        # make object from login class
        login = loginWindow()
        # add it to the widget stack
        widget.addWidget(login)
        # to flip the screen to the login
        widget.setCurrentIndex(widget.currentIndex() + 1)
    # sign up function will link to the sign up class then we show the signup screen

    def signup_clicked(self):
        # make object from signup class
        signup = signupWindow()
        # add it to the widget stack
        widget.addWidget(signup)
        # to flip the screen to the signup
        widget.setCurrentIndex(widget.currentIndex() + 1)
# Login page
class loginWindow(QDialog):
    def __init__(self):
        super(loginWindow, self).__init__()
        loadUi('facedetection/gui/guiLogin.ui', self)
        self.setWindowTitle("Login")
        # self.login.clicked.connect(self.login_clicked)
        self.passwordfield.setEchoMode(QtWidgets.QLineEdit.Password)
        self.login.clicked.connect(self.login_function)
        self.backbutton.clicked.connect(self.back_button_function)
        self.label.setFixedWidth(700)
        self.label.setFixedHeight(800)
        self.setFixedWidth(700)
        self.setFixedHeight(800)
        self.label.setStyleSheet("border-image: url(facedetection/gui/images/background.jpg)")
    # to handle the login button inside the login window
    def login_function(self):
        # get the username and password
        username = self.usernamefield.text()
        password = self.passwordfield.text()

        # check if the username and password are correct and they are inside the database
        if username in database and database[username] == password:
            # if correct then show the main window
            print("Login Successful")
            user = mainWindow()
            widget.addWidget(user)
            widget.setCurrentIndex(widget.currentIndex() + 1)

        elif len(username) == 0 and len(password) == 0:
            # if username and password are empty show error message
            self.errorfield.setText("* Please enter your username and password")

        else:
            # if not correct then show the error message
            self.errorfield.setText("* Username or Password is incorrect")

    # to handle the back button inside the login window
    def back_button_function(self):
        # to flip the screen to the main window
        widget.removeWidget(widget.currentWidget())
        widget.setCurrentIndex(widget.currentIndex() )


# signup page 
class signupWindow(QDialog):
    def __init__(self):
        super(signupWindow, self).__init__()
        loadUi('facedetection/gui/guiSignup.ui', self)
        self.setWindowTitle("Signup")
        self.signup.clicked.connect(self.signup_function)
        self.backbutton.clicked.connect(self.back_button_function)
        self.label.setFixedWidth(700)
        self.label.setFixedHeight(800)
        self.setFixedWidth(700)
        self.setFixedHeight(800)
        self.label.setStyleSheet("border-image: url(facedetection/gui/images/background.jpg)")
    # to handle the signup button inside the signup window
    def signup_function(self):
        # get the username and password
        username = self.usernamefield.text()
        password = self.passwordfield.text()
        passwordconfirm = self.passwordconfirmfield.text()

        # check if the username and password are correct and they are inside the database
        if password != passwordconfirm:
            # if not correct then show the error message
            self.errorfield.setText("* Password does not match") 

        elif username not in database and password == passwordconfirm:
            # if correct then show the main window
            print("Sign up Successful")
            # add the username and password to the database
            database[username] = password
            main = mainWindow()
            widget.addWidget(main)
            widget.setCurrentIndex(widget.currentIndex() + 1)

        elif len(username) == 0 or len(password)==0 or len(passwordconfirm)== 0:
            # if username and password are empty show error message
            self.errorfield.setText("* Please enter your username and password")

        elif username in database:
            # if user name is found in the database
            self.errorfield.setText("* Username is Taken")

        else:
            # if not correct then show the error message
            self.errorfield.setText("* Something went Wrong")

    # to handle the back button inside the signup window
    def back_button_function(self):
        # to flip the screen to the main window
        widget.removeWidget(widget.currentWidget())
        widget.setCurrentIndex(widget.currentIndex() )

# report page       
class reportWindow(QDialog):
    def __init__(self):
        super(reportWindow, self).__init__()
        loadUi('facedetection/gui/guiReport.ui', self)
        self.setWindowTitle("Report")
        self.backbutton.clicked.connect(self.back_button_function)
        self.Reporttable.setColumnWidth(0,200)
        self.Reporttable.setColumnWidth(1,200)
        self.Reporttable.setColumnWidth(2,240)
        self.label.setFixedWidth(700)
        self.label.setFixedHeight(800)
        self.setFixedWidth(700)
        self.setFixedHeight(800)
        self.label.setStyleSheet("border-image: url(facedetection/gui/images/background.jpg)")
        #Row count
        #Column count
        # self.Reporttable.setColumnCount(3)  
        self.read_report()

    def read_report(self):
        """read from csv file"""
        with open('report.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            # self.Reporttable.setRowCount(len(list(reader))-1)
            self.Reporttable.setRowCount(13)
            
            for row in reader:
                print("this is row", row)
                for i in range(len(row)):
                    # self.Reporttable.setItem(read each line in the reader,row_num, each value to the table column count)
                    self.Reporttable.setItem(reader.line_num-2,i,QTableWidgetItem(row[i]))

    # to handle the back button inside the signup window
    def back_button_function(self):
        # to flip the screen to the main window
        widget.removeWidget(widget.currentWidget())
        widget.setCurrentIndex(widget.currentIndex() )

############################################################################################
###########################################  guitwo ########################################
############################################################################################
# Home page 
class mainWindow(QDialog):
    def __init__(self):
        super(mainWindow, self).__init__()
        loadUi('facedetection/gui/mainWindow.ui', self)
        self.start.clicked.connect(self.start_clicked)
        self.report.clicked.connect(self.report_function) 
        self.backbutton.clicked.connect(self.back_button_function)
        self.label.setFixedWidth(700)
        self.label.setFixedHeight(800)
        self.setFixedWidth(700)
        self.setFixedHeight(800)
        self.label.setStyleSheet("border-image: url(facedetection/gui/images/background.jpg)")
    def start_clicked(self):
        videoScreen = videoWindow()
        widget.addWidget(videoScreen)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    # to handle the report button inside the user window
    def report_function(self):
        report = reportWindow()
        widget.addWidget(report)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    # to handle the back button inside the signup window
    def back_button_function(self):
        # to flip the screen to the main window
        widget.removeWidget(widget.currentWidget())
        widget.setCurrentIndex(widget.currentIndex() )

# Cam page
class videoWindow(QDialog):
    def __init__(self):
        super(videoWindow, self).__init__()
        loadUi('facedetection/gui/videoWindow.ui', self)
        self.backbutton.clicked.connect(self.back_button_function)
        self.video = videoLable(self.videoLabel)
        self.video.run_thread(self.edited)
        self.label.setFixedWidth(700)
        self.label.setFixedHeight(800)
        self.setFixedWidth(700)
        self.setFixedHeight(800)
        self.label.setStyleSheet("border-image: url(facedetection/gui/images/background.jpg)")

    @pyqtSlot(np.ndarray,name="edited")
    def edited(self,image):
        self.video.update_image(image)
    def back_button_function(self):
        # to flip the screen to the main window
        self.video.camera.release()
        widget.removeWidget(widget.currentWidget())
        widget.setCurrentIndex(widget.currentIndex())
# to play the cam inside the label
class videoLable(QWidget):
    def __init__(self , lable):
        self.videoLabel = QLabel()
        self.camera = cv2.VideoCapture(0)
        self.shape = self.get_resolution(self.camera)
        self.videoLabel = lable
        self.videoLabel.resize(self.shape[0], self.shape[1])

    def run_thread(self,edited):
        self.thread = videoThread(self.camera)
        self.thread.pixmap.connect(edited)
        self.thread.start()
    def get_resolution(self , camera):
        ret , frame = camera.read()
        return frame.shape
    # @pyqtSlot(np.ndarray)
    def update_image(self, image):
        # print("image updated")
        qtFrame = self.convert_cv2_to_qt(image)
        self.videoLabel.setPixmap(qtFrame)

    def convert_cv2_to_qt(self, image):
        rgbFrame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        h, w, ch = rgbFrame.shape
        bytesPerLine = ch * w
        convertToQtFormat = QtGui.QImage(rgbFrame.data, w, h, bytesPerLine, QtGui.QImage.Format_RGB888)
        p = convertToQtFormat.scaled(self.videoLabel.width(), self.videoLabel.height(), Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)

    def closeThread(self):
        self.thread.stop()


class videoThread(QThread):
    pixmap = pyqtSignal(np.ndarray)
    def __init__(self , camera):
        super(videoThread, self).__init__()
      
        # self.backbutton.clicked.connect(self.back_button_function)
        # self.video = self.videoLabel(self.videoLabel)
        # self.video.run_thread(self.edited)
        # self.backbutton.clicked.connect(self.back_button_function)
        # self._flag = True
        self.camera = camera
        self.counter=0
        self.sleep_times=0
        self.unauthorize_flag=True
        self.counter_sending=0
        self.alarm=False
        self.ap = argparse.ArgumentParser()
        self.ap.add_argument("-w", "--webcam", type=int, default=0,help="index of webcam on system")
        self.ap.add_argument("-a", "--alarm", type=int, default=0,help="path alarm .mp3 file")               
        self.args = vars(self.ap.parse_args())
    def  run(self):

        while self.camera.isOpened():
            print("Thread is runing")
            # ret , self.frame = self.camera.read()
            self.detection_real_time()
            # self.pixmap.emit(self.frame)
        
    def back_button_function(self):
        # to flip the screen to the main window
        widget.removeWidget(widget.currentWidget())
        widget.setCurrentIndex(widget.currentIndex() )
        self.camera.release()
    def stop(self):
        self._flag = False
        self.wait()
    # Drowsy Detection:
    def sound_alarm(self,path):
        music = pyglet.resource.media("alarm.mp3")
        if not self.alarm:
            music.play()
        pyglet.app.run()

    def drwosy(self,name):
        
        if self.camera.isOpened():    
            ret, self.frame=self.camera.read()or None
            cv2.rectangle(self.frame,(self.x1,self.y1),(self.x2,self.y2),(0,255,0),2)
            cv2.rectangle(self.frame,(self.x1,self.y2-35),(self.x2,self.y2),(0,255,0),cv2.FILLED)
            cv2.putText(self.frame,name,(self.x1+6,self.y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
            self.pixmap.emit(self.frame)
            self.frame = imutils.resize(self.frame, width=700,height=700)
            gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
            rects = detector(gray, 0)
            for rect in rects:
                shape = predictor(gray, rect)
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
                    self.counter += 1
                    print(self.counter)
                    if self.counter >= EYE_CONSEC_FRAMES:
                        if self.counter==30:
                            self.alarm=False
                        if not self.alarm:
                            self.alarm = True
                            # t = audio_thread(target=self.sound_alarm,args=(self.args["alarm"],))
                            # t.deamon = True
                            # t.start()
                            duration = 1  # seconds
                            freq = 700  # Hz
                            os.system('play -nq -t alsa synth {} sine {}'.format(duration, freq))
                            print('alarm')
                            self.counter = 0
                            self.sleep_times+=1
                            if self.sleep_times == 4:
                                                
                                img_name = "forsending.jpg"
                                cv2.imwrite(img_name, self.frame)  
                                send_email("forsending.jpg",f"{name} status is drowsy")
                                os.remove("forsending.jpg")
                                save_report(name)
                                # authorize_flag=False
                                # counter_sending=0
                                print("done from sending email")
                                self.sleep_times =0 
                        cv2.putText(gray, "DROWSINESS ALERT!", (10, 30),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                        cv2.putText(gray, f"sleep times={self.sleep_times}", (100,70),cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                        
                else:
                                self.counter = 0
                                self.alarm=False
                                
                                
                cv2.putText(gray, "EAR: {:.2f}".format(ear), (300, 30),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            # return (counter,self.sleep_times)

    def detection_real_time(self):
        Keyboard=KeyboardInterrupt()
        images_data()
        encodeListKnown = findEncodings(employee_images)
        print('Encoding Complete')

        # COUNTER = 0
        # counter=0
        # sleep_times=0
        # unauthorize_flag=True
        # counter_sending=0
        # authorize_flag=True
        while self.camera.isOpened():
            # images_data()
            # encodeListKnown = findEncodings(employee_images)
            success, self.frame = self.camera.read()
            imgS = cv2.resize(self.frame,(0,0),None,0.25,0.25)
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
                    flag=True
                    name = employee_names[matchIndex].upper()
                    
                    self.y1,self.x2,self.y2,self.x1 = faceLoc
                    self.y1, self.x2, self.y2, self.x1 = self.y1*4,self.x2*4,self.y2*4,self.x1*4
                    cv2.rectangle(self.frame,(self.x1,self.y1),(self.x2,self.y2),(0,255,0),2)
                    cv2.rectangle(self.frame,(self.x1,self.y2-35),(self.x2,self.y2),(0,255,0),cv2.FILLED)
                    cv2.putText(self.frame,name,(self.x1+6,self.y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)

                    # print("Hi",name)
                    self.drwosy(name)
                    
                    # if counter_sending>2 and authorize_flag:
                    #         img_name = "forsending.jpg"
                    #         cv2.imwrite(img_name, img)  
                    #         send_email("forsending.jpg",f"{name} status is drowsy")
                    #         os.remove("forsending.jpg")
                    #         authorize_flag=False
                    #         counter_sending=0
                    #         print("done from sending email")
                else:
                    self.pixmap.emit(self.frame)
                    self.counter_sending+=1
                    if self.unauthorize_flag and self.counter_sending>25:
                        print("unauthorize")
                        img_name = "forsending.jpg"
                        cv2.imwrite(img_name,self.frame)    
                        send_email("forsending.jpg",'There is unauthorized access!')
                        os.remove("forsending.jpg")
                        self.unauthorize_flag=False
                        save_report()

                # To show the images            
                # cv2.imshow('Face Recognition',img)
                # To show the images            
                
                # The time lag 

                # cv2.waitKey(1) 
                # key = cv2.waitKey(1) & 0xFF
                # if key == ord("q"):
                #     break 
     


# main
if __name__ == '__main__':
    app = QApplication(sys.argv)
    home = IntroPage()
    widget = QtWidgets.QStackedWidget()
    widget.addWidget(home)
    widget.setWindowTitle("App-Drowsiness-Detector")
    widget.setFixedWidth(700)
    widget.setFixedHeight(800)
    widget.show()
    try:
        sys.exit(app.exec_())
    except:
        print("Exiting From The Application")