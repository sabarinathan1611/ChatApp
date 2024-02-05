from flask import Blueprint, render_template, request, flash, redirect, url_for,jsonify
from . import db
from .models import User
from flask_login import login_required,current_user
from . import socketio
from flask_socketio import join_room
views = Blueprint('views', __name__)


@views.route('/')
@login_required
def home():	return render_template('chat.html')

@socketio.on('connect')
def handle_connect():
    print('Client Connected')
    
@socketio.on('join_room')
def handle_joinroom(data):
    print("Received 'join_room' event from user:", data['user'],data['roomid'])
    join_room(data['roomid'])


    socketio.emit('room_joined', data)

@socketio.on('send_message')
def send_message(data):
    print("User :",data['username'])
    print("room:",data['room']),
    print("Message :",data['message'])
    return socketio.emit('recived_message',data)
    

