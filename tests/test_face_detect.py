from facedetection.application import*
import cv2
import face_recognition
# import pytest


def converting_image(path):
    # 1- Loading the image file as numpy array
    img_tom = cv2.imread(path)
    # 2- Converting to gray scale
    img_tom = cv2.cvtColor(img_tom, cv2.COLOR_BGR2RGB)
    encoded = face_recognition.face_encodings(img_tom)[0]
    return encoded


# @pytest.fixture
# def one_path():
#     return converting_image('fd_database/tom_test.jpeg')


# @pytest.fixture
# def two_paths():
#     return [converting_image('fd_database/tom_test.jpeg'), converting_image('fd_database/tom_cruise.jpg')]


# @pytest.fixture
# def diff_image(one_path):
#     return [one_path, converting_image('fd_database/leonardo_dicaprio.jpg')]

# Testing if the findencoding function is successfully encoding the face located in the given image:


def test_findencoding():
    # Arrange
    img_tom = [cv2.imread('fd_database/tom_test.jpeg')]
    expected = converting_image('fd_database/tom_test.jpeg')
    # Act
    actual = findEncodings(img_tom)[0]
    # Assert
    assert expected[0] == actual[0]

# Testing if the facecomparison function is successfully compare  the face encodings for the given images:


def test_facecomparison_same_path():
    one_path=converting_image('fd_database/tom_test.jpeg')
    # Arrange
    expected = face_recognition.compare_faces([one_path], one_path)[0]
    # Act
    actual = face_comparison([one_path], one_path)[0]
    # Assert
    assert expected == actual


def test_facecomparison_different_path():
    two_paths=[converting_image('fd_database/tom_test.jpeg'), converting_image('fd_database/tom_cruise.jpg')]
    # Arrange
    expected = face_recognition.compare_faces([two_paths[0]], two_paths[1])[0]
    # Act
    actual = face_comparison([two_paths[0]], two_paths[1])[0]
    # Assert
    assert expected == actual


def test_facecomparison_different_images():
    diff_image=[converting_image('fd_database/tom_test.jpeg'), converting_image('fd_database/leonardo_dicaprio.jpg')]
    # Arrange
    expected = face_recognition.compare_faces(
        [diff_image[0]], diff_image[1])[0]
    # Act
    actual = face_comparison([diff_image[0]], diff_image[1])[0]
    # Assert
    assert expected == actual
