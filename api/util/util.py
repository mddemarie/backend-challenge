from flask_mail import Message

def send_email(email, subject, html):
    msg = Message(email, subject, html)
    return msg