import smtplib
import imghdr
from email.message import EmailMessage
def send_email(img):
    Sender_Email = "saaddhirat@gmail.com"
    Reciever_Email = "arahal81@gmail.com"
    Password = 'saad2441993'
    newMessage = EmailMessage()                         
    newMessage['Subject'] = "Check out the new logo" 
    newMessage['From'] = Sender_Email                   
    newMessage['To'] = Reciever_Email                   
    newMessage.set_content('There is Unauthorised access!') 
    with open(img, 'rb') as f:
        image_data = f.read()
        image_type = imghdr.what(f.name)
        image_name = f.name
    newMessage.add_attachment(image_data, maintype='image', subtype=image_type, filename=image_name)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        
        smtp.login(Sender_Email, Password)              
        smtp.send_message(newMessage)

        
# if __name__ == '__main__':
#     # sendmail("Arahal81@gmail.com", "This is a test email from python script")
#     # send_mail_test()
