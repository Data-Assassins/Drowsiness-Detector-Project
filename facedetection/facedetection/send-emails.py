import smtplib, ssl

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


if __name__ == '__main__':
    sendmail("Arahal81@gmail.com", "This is a test email from python script")