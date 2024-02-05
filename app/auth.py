from flask import Blueprint, render_template, request, flash, redirect, url_for,jsonify
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from . import db, mail
from .models import User

from .functions import send_verification_email
from .config import Config 
from flask_cors import cross_origin

 
auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
  
    if request.method=='POST':

        email = request.form.get('email')
        password = request.form.get('Password')

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user, remember=True)
            return redirect(url_for('views.home'))
            
        else:
            flash("Login unsuccessful. Please check your email and password.")

    return render_template('login.html')


@auth.route('/sign-up', methods=['POST', 'GET'])
def sign_up():
    

    if request.method == 'POST' :
        email = request.form.get('email')
        password = request.form.get('Password')
        name = request.form.get('name')
        hashed_password = generate_password_hash(password)

        already_in = User.query.filter_by(email=email).first()
        if already_in:
            flash('Email address is already in use.', 'danger')
            return redirect(url_for('auth.sign_up'))
        else:
            if email == Config.AdminMail:
                print("Admin Email:",Config.AdminMail)
                user = User(email=email, password=hashed_password, username=name,is_verified=True,role='admin')
                db.session.add(user)
                db.session.commit()


                flash('Admin Account created successfully', 'success')
                return redirect(url_for('views.home'))
            else:
                print("Admin Email:",Config.AdminMail)
                user = User(email=email, password=hashed_password, username=name)
                db.session.add(user)
                db.session.commit()

                # Send verification email to the user
                send_verification_email(user)

                flash('Account created successfully. Check your email for verification.', 'success')
                return redirect(url_for('views.home'))

    return render_template('Signup.html')

@auth.route('/verify_email/<string:verification_token>')
def verify_email(verification_token):
    user = User.query.filter_by(verification_token=verification_token).first()

    if user:
        # Mark the user as verified
        user.is_verified = True
        db.session.commit()

        # Log in the user after successful verification
        login_user(user)

        flash('Email verification successful! You can now access your account.')
        return redirect(url_for('views.home'))
    else:
        flash('Invalid verification token. Please try again.')
        return redirect(url_for('signup'))

@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))