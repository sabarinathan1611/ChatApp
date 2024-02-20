from flask import Blueprint, render_template, request, flash, redirect, url_for,jsonify
from flask_login import login_required, login_user, logout_user, current_user
from .models import User
from .functions import send_verification_email
from .config import Config 
from flask_cors import cross_origin
from .models import get_user,save_user
from .config import Config  as con
 
auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST','GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))

    if request.method == 'POST':
        data = request.json  # Retrieve JSON data from AJAX request
        username = data.get('username')
        password = data.get('password')
        user = get_user(username)

        if user is not None:  # Check if user exists
            if user.check_password(password):
                login_user(user, remember=True)
                return jsonify({'success': True, 'message': 'Login successful'})  
            else:
                return jsonify({'success': False, 'message': 'Invalid password'})  
        else:
            return jsonify({'success': False, 'message': 'User not found'})

    return render_template('login.html')



@auth.route('/signup', methods=['POST', 'GET'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))

    if request.method == 'POST':
        data = request.json  
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        
        save_user(username=username, password=password, email=email)
        try:
            user = get_user(username)
            send_verification_email(user)
        except Exception as error:
            flash(error)
        return jsonify({'success': True, 'message': 'Signup successful'}) 
    return render_template('signup.html')


@auth.route('/verify_email/<string:verification_token>')
def verify_email(verification_token):
    user_data = con.users_db.find_one({'verification_token': verification_token})

    if user_data:
        # Mark the user as verified
        con.users_db.update_one({'verification_token': verification_token}, {'$set': {'is_verified': True}})
        
        # Create a User object from the retrieved data
        user = User(
            username=user_data['_id'],
            email=user_data['email'],
            password=user_data['password'],
            is_verified=True  
        )

       
        login_user(user)

        flash('Email verification successful! You can now access your account.')
        return redirect(url_for('views.home'))
    else:
        flash('Invalid verification token. Please try again.')
        return redirect(url_for('signup'))


@auth.route('logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('auth.login'))