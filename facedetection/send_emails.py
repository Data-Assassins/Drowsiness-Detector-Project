import smtplib
import imghdr
from email.message import EmailMessage

def send_email(img,msg:str)-> bool:
    Sender_Email = "saaddhirat@gmail.com"
    Reciever_Email = "arahal81@gmail.com"
    Password = 'saad2441993'
    newMessage = EmailMessage()                         
    newMessage['Subject'] = "‪Drowsiness Detector Status" 
    newMessage['From'] = Sender_Email                   
    newMessage['To'] = Reciever_Email                   
    newMessage.set_content(msg) 
    with open(img, 'rb') as f:
        image_data = f.read()
        image_type = imghdr.what(f.name)
        image_name = f.name
    newMessage.add_attachment(image_data, maintype='image', subtype=image_type, filename=image_name)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(Sender_Email, Password)              
        smtp.send_message(newMessage)
    return True
        