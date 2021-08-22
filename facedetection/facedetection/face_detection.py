import cv2
import numpy as np
import scipy
import dlib
import face_recognition


# The train image

tom_image = face_recognition.load_image_file('fd_database/Tom-Cruise-1.jpg')
# The detection works only on grayscale images
tom_image = cv2.cvtColor(tom_image,cv2.COLOR_BGR2RGB)

# The test image

tom_test = face_recognition.load_image_file('fd_database/leonardo-dicaprio11.jpg')
tom_test = cv2.cvtColor(tom_test,cv2.COLOR_BGR2RGB)

# The Second Step: Get the face location fpr each face in each image. 
faceLoc = face_recognition.face_locations(tom_image)[0]
# The Third step: Get the face encodings,for each face in each image file . 

encod_tom = face_recognition.face_encodings(tom_image)[0]
cv2.rectangle(tom_image,(faceLoc[3],faceLoc[0]),(faceLoc[1],faceLoc[2]),(255,0,255),2)

# index zero because we can have multiple faces in one image but we want only the face location for the first one

faceLocTest = face_recognition.face_locations(tom_test)[0]

# # Test image
# (top,right,bottom,left)
encodeTest = face_recognition.face_encodings(tom_test)[0]
cv2.rectangle(tom_test,(faceLocTest[3],faceLocTest[0]),(faceLocTest[1],faceLocTest[2]),(255,0,255),2)
 
results = face_recognition.compare_faces([encod_tom],encodeTest)
faceDis = face_recognition.face_distance([encod_tom],encodeTest)
print(results,faceDis)
cv2.putText(tom_test,f'{results} {round(faceDis[0],2)}',(50,50),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),2)
 
cv2.imshow('Tom Image',tom_image)
cv2.imshow('Tom Test',tom_test)
cv2.waitKey(0)
