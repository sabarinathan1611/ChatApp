from app import create_app,socketio

app = create_app(mode='development')

if __name__ == '__main__':
    socketio.run(app, debug=True)