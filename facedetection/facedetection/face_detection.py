import cv2
import numpy as np
import scipy
import dlib
import face_recognition
import os

# Face detection using image as input
# First Step: Loading the known images files 

path = 'fd_database'
employee_images = []
employee_names = []
images_list = os.listdir(path)

for image_path in images_list:
    current_image=  cv2.imread(f'{path}/{image_path}')
    employee_images.append(current_image)
    employee_names.append(os.path.splitext(image_path)[0])


# tom_image = face_recognition.load_image_file('fd_database/Tom-Cruise-1.jpg')
# tom_test = face_recognition.load_image_file('fd_database/leonardo-dicaprio11.jpg')

def face_recog(image):

    # The detection works only on grayscale images
    image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)

    # The Second Step: Get the face location fpr each face in each image. 


    faceLoc = face_recognition.face_locations(image)[0]
    # index zero because we can have multiple faces in one image but we want only the face location for the first one
    # (top,right,bottom,left)

    # The Third step: Get the face encodings,for each face in each image file . 
    encod_image = face_recognition.face_encodings(image)[0]
    cv2.rectangle(image,(faceLoc[3],faceLoc[0]),(faceLoc[1],faceLoc[2]),(255,0,255),2)
    


    return [encod_image,image]
    


# Getting the encodings for the known faces
def encoded_known_list(images):
    encoded_known_employees = []
    for image in images:

        result = face_recog(image)[0] 
        encoded_known_employees.append(result)
    return encoded_known_employees

encodeListKnown = encoded_known_list(employee_images)


# Getting the encodings for the unknown faces
cap = cv2.VideoCapture(0)
# test_encoded = face_recog(tom_test)[0] 
# while cap.isOpened():
#     success, img = cap.read()
#     imgS = cv2.resize(img,(0,0),None,0.25,0.25) 
#     if cv2.waitKey(10) & 0xFF == ord('q'):
#         break
# cap.release()
# cv2.destroyAllWindows()

def face_comparison(train_encode,test_encode):
    # Fourth step: Comaring between the the test image and train image measurements
    results = face_recognition.compare_faces([train_encode],test_encode)
    return results

# Comparing the faces
results = face_comparison(train_encoded,test_encoded)


# Getting the face distance
faceDis = face_recognition.face_distance([train_encoded],test_encoded)

# The results can be True or False , matched or mismatched 
print(results,faceDis)

cv2.putText(tom_test,f'{results} {round(faceDis[0],2)}',(50,50),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),2)


# To show the images

cv2.imshow('Tom Test',face_recog(tom_test)[1])

# The time lag 
cv2.waitKey(0)
