import cv2
import numpy as np
import scipy
import dlib
import face_recognition

# Face detection using images as input
# First step: Loading the images as numpy array using face_recognition load_image method.
# The tarining image and testing from our database(fd_database) directory

# The train image
# imgElon = face_recognition.load_image_file('fd_database/Tom-Cruise-1.jpg')
tom_image = face_recognition.load_image_file('fd_database/Tom-Cruise-1.jpg')

# The detection works only on grayscale images
# imgElon = cv2.cvtColor(imgElon,cv2.COLOR_BGR2RGB)
tom_image = cv2.cvtColor(tom_image, cv2.COLOR_BGR2GRAY)

# The test image
tom_test = face_recognition.load_image_file('fd_database/tom_test.jpeg')
tom_test = cv2.cvtColor(tom_test, cv2.COLOR_BGR2GRAY)

# # The Second Step: Get the face location fpr each face in each image.


faceLoc = face_recognition.face_locations(tom_image)[0] 
# print(faceLoc)
point_one = (faceLoc[3],faceLoc[0])
point_two = (faceLoc[1],faceLoc[2])

# index zero because we can have multiple faces in one image but we want only the face location for the first one
# (top,right,bottom,left)


# The Third step: Get the face encodings,for each face in each image file . 

encod_tom = face_recognition.face_encodings(tom_image)[0]
cv2.rectangle(tom_image,point_one,point_two,(255,0,255),2)

# Test image
face_loc_test= face_recognition.face_locations(tom_test)[0]
encod_tom_test = face_recognition.face_encodings(tom_test)[0]
cv2.rectangle(tom_test,(face_loc_test[3],face_loc_test[0]),(face_loc_test[1],face_loc_test[2]),(255,0,255),2)


# Fourth step : Compare between the two images face measurements
cv2.imshow('Tom Train',tom_image)
cv2.imshow('Tom Test',tom_test)
cv2.waitKey(0)



 

