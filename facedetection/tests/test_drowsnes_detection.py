import pytest 
from facedetection.drowsiness import *
from facedetection import *

def test_open_cam():
  assert VideoStream(src=args["webcam"]).start()
  
    
def test_close_cam():
    vs = VideoStream(src=args["webcam"]).start()
    assert vs 
    cv2.destroyAllWindows()
    vs.stop()   

def test_ear():
            leftEAR = eye_aspect_ratio(leftEye)
            rightEAR = eye_aspect_ratio(rightEye)
            assert (leftEAR + rightEAR) / 2.0
            

# def test_check_alarm():

#     eye_ear = eye_aspect_ratio(eye)
#     EYE_THRESHOLD=0.3
#     if eye_ear < EYE_THRESHOLD:
#         assert ALARAM            

