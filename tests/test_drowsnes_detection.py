# import pytest 
from facedetection.application import *

def converting_image(path):
      # 1- Loading the image file as numpy array 
    img_tom = cv2.imread(path)
       # 2- Converting to gray scale
    img_tom = cv2.cvtColor(img_tom,cv2.COLOR_BGR2RGB)
    encoded = face_recognition.face_encodings(img_tom)[0]
    return encoded


# @pytest.fixture
# def one_path():
#    return  converting_image('fd_database/tom_test.jpeg')



def test_findencoding2():
    # Arrange 
    one_path = converting_image('fd_database/tom_test.jpeg')

    img_tom = [cv2.imread('fd_database/tom_test.jpeg')]
    expected = one_path
    # Act 
    actual = findEncodings(img_tom)[0]
    assert expected[0] == actual[0]
    
# def test_left_eye_recognetion():
#     detector = dlib.get_frontal_face_detector()
#     predictor = dlib.shape_predictor("facedetection/68_face_landmarks.dat")
#     (left_Start, left_End) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
#     assert  [left_Start, left_End]


# def test_right_eye_recognetion():
#     detector = dlib.get_frontal_face_detector()
#     predictor = dlib.shape_predictor("facedetection/68_face_landmarks.dat")
#     (right_Start, right_End) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
#     assert  [right_Start, right_End]
    
    
    
