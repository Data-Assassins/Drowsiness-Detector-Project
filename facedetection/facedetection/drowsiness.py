from re import S
from scipy.spatial import distance as dist
from imutils.video import VideoStream
from imutils import face_utils
from threading import Thread
import numpy as np
import pyglet
import argparse
import imutils
import time
import dlib
import cv2

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
def drowsiness_detection(vs,name):
    
    ap = argparse.ArgumentParser()

    ap.add_argument("-w", "--webcam", type=int, default=0,
    	help="index of webcam on system")
    ap.add_argument("-a", "--alarm", type=int, default=0,
     	help="path alarm .WAV file")               
    args = vars(ap.parse_args())

    EYE_THRESHOLD = 0.3
    EYE_CONSEC_FRAMES = 48


EYE_THRESHOLD = 0.3
EYE_CONSEC_FRAMES = 20


    print("[INFO] loading facial landmark predictor...")
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("facedetection/68_face_landmarks.dat")

    (left_Start, left_End) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
    (right_Start, right_End) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

    print( "[INFO] starting video thread ..")

    # vs = VideoStream(src=args["webcam"]).start()
    # time.sleep(1.0)

    sleep_times=0

    while True:
        frame = vs.read()
        frame = imutils.resize(frame, width=450)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
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
                COUNTER += 1
                if COUNTER >= EYE_CONSEC_FRAMES:
                    if not ALARAM:
                        ALARAM = True
                        # t = Thread(target=sound_alarm,args=(args["alarm"],))
                        # t.deamon = True
                        # t.start()
                        sleep_times+=1
                        print(sleep_times)
                    # cv2.putText(frame, "DROWSINESS ALERT!", (10, 30),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    # cv2.putText(frame, f"sleep times={sleep_times}", (100,70),cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                    if sleep_times>4:
                       return sleep_times
            else:
                            COUNTER = 0
                            ALARAM = False  

        cv2.putText(frame, "EAR: {:.2f}".format(ear), (300, 30),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        # cv2.putText(frame,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
        cv2.imshow('Face Recognition',frame)
        cv2.waitKey(1)
    # cv2.imshow("Frame", frame)
    # key = cv2.waitKey(1) & 0xFF    
    
    # if key == ord("q"):  
    #     break     

# cv2.destroyAllWindows()
# vs.stop()                 
# if __name__ == "__main__":
#     drowsiness_detection()
#     vs = VideoStream(src=args["webcam"]).start()
#     cv2.destroyAllWindows()
#     vs.stop()
    # sound_alarm("alarm.wav")
