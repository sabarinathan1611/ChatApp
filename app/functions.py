# functions.py
from flask_mail import Message
from flask import url_for,render_template
from . import mail
import os
def send_verification_email(user):
    try:
        verification_link = url_for('auth.verify_email', verification_token=user.verification_token, _external=True)
        print("verification_link",type(verification_link))
        subject = 'Verify Your Email for Web App'
        body = render_template('email.html', verification_link=verification_link)
        print("body:", body)
        
        send_email(user.email, subject, body)
    except Exception as error:
        print(error)

def send_email(to, subject, body):
    sender=os.environ.get('GMAIL_USERNAME')
    print("SENDER MAIL: ",sender)
    msg = Message(subject, sender=sender, recipients=[to])
    msg.html = body
    mail.send(msg)
