import pytest
from facedetection.send_emails import send_email

# test image path
def test_image_path():
    img = "facedetection/images/projectposter.png"
    with open (img , "rb") as f:
        assert f.read()

# test if email is sent
def test_send_email():
    img = "facedetection/images/projectposter.png"
    msg = "Hello, this is a test email"
    assert send_email(img , msg)
    