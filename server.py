from myapp import create_app
from myapp.database import db, Message
from flask import request
from flask_socketio import SocketIO

app, socketio = create_app()

host="0.0.0.0"
port=5000

# Initialize SocketIO with your Flask app
socketio.init_app(app)

# COMMUNICATION ARCHITECTURE
@socketio.on('disconnect')
def handle_disconnect():
    """
    handles disconnection event
    :return: None
    """
    print(f'{request.sid} disconnected')
    socketio.emit('disconnect', {'sid': request.sid})

@socketio.on('event')
def custom_event(json):
    """
    handles saving messages and sending messages to other clients
    :param json: json
    :return: None
    """
    data = dict(json)
    if 'name' in data:
        message = Message(name=data['name'], message=data['message'], time=data['date'])
        db.session.add(message)
        db.session.commit()

    socketio.emit('message response', json, room=None)

if __name__ == "__main__":
    socketio.run(app, host, port)
    print(host,port)
