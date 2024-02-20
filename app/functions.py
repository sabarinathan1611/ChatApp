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
        html = f"""
 <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Email Verification</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                    margin: 0;
                    padding: 0;
                }}
                .container {{
                    max-width: 600px;
                    margin: 20px auto;
                    background-color: #ffffff;
                    padding: 20px;
                    border-radius: 10px;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                }}
                h1 {{
                    text-align: center;
                    color: #333333;
                }}
                p {{
                    color: #666666;
                }}
                .btn {{
                    display: inline-block;
                    background-color: #007bff;
                    color: #ffffff;
                    text-decoration: none;
                    padding: 10px 20px;
                    border-radius: 5px;
                    transition: background-color 0.3s;
                }}
                .btn:hover {{
                    background-color: #0056b3;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Verify Your Email</h1>
                <p>Click the following link to verify your email:</p>
                <a href="{verification_link}" class="btn">Verify Email</a>
            </div>
        </body>
        </html>
        """
        
        
        send_email(user.email, subject, html)
    except Exception as error:
        print(error)

def send_email(to, subject, html):
    sender=os.environ.get('GMAIL_USERNAME')
    print("SENDER MAIL: ",sender)
    msg = Message(subject, sender=sender, recipients=[to])
    msg.html = html
    mail.send(msg)
