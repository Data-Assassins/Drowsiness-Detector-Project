import smtplib, ssl
import imghdr
from email.message import EmailMessage
def sendmail(receiver_email, message):
    port = 587  # For starttls
    smtp_server = "smtp.gmail.com"
    sender_email = "saaddhirat@gmail.com"
    # receiver_email = "Arahal81@gmail.com"
    receiver_email = receiver_email
    password = "saad2441993"
    message = """\
    Subject: Hi there, email feature works, this is a test email from python script.
    This message is sent from Python.
              """
    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)

def send_mail_test(img):
    Sender_Email = "saaddhirat@gmail.com"
    Reciever_Email = "arahal81@gmail.com"
    Password = 'saad2441993'
    newMessage = EmailMessage()                         
    newMessage['Subject'] = "Check out the new logo" 
    newMessage['From'] = Sender_Email                   
    newMessage['To'] = Reciever_Email                   
    newMessage.set_content('There is unauthorised access!') 
    
    image_data = img
    newMessage.add_attachment(image_data, maintype='image', subtype="jpg", filename="Unauthorised")
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        
        smtp.login(Sender_Email, Password)              
        smtp.send_message(newMessage)

        
# if __name__ == '__main__':
#     # sendmail("Arahal81@gmail.com", "This is a test email from python script")
#     # send_mail_test()
    