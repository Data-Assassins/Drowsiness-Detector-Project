# import pytest 
# from facedetection.gui.guiTwo import *
# from facedetection import *
# import cv2
# from imutils.video import VideoStream
# # def test_open_cam():
# #   assert VideoStream(src=args["webcam"]).start()
  
    
# def test_open_close_cam():
#     vs = VideoStream(src=args["webcam"]).start()
#     assert vs
#     cv2.destroyAllWindows()
#     vs.stop()   

# # def test_ear():
# #             leftEAR = eye_aspect_ratio(leftEye)
# #             rightEAR = eye_aspect_ratio(rightEye)
# #             assert (leftEAR + rightEAR) / 2.0
            

# # def test_check_alarm():

# #     eye_ear = eye_aspect_ratio(eye)
# #     EYE_THRESHOLD=0.3
# #     if eye_ear < EYE_THRESHOLD:
# #         assert ALARAM            

# def test_detect_left_eye():
#  
#         for rect in rects:
#             shape = predictor(gray, rect)
#             shape = face_utils.shape_to_np(shape)
#             leftEye = shape[left_Start:left_End]
#         assert  leftEye.any()

# def test_detect_right_eye():
#     rects = detector(gray, 0)
#     for rect in rects:
#         shape = predictor(gray, rect)
#         shape = face_utils.shape_to_np(shape)
#         rightEye = shape[right_Start:right_End]
#     assert rightEye.any()