from app import socketapp
from utility.middleware import socket_authentication
from flask import request
from flask_socketio import send

user_pool = dict()

@socketapp.on('connect')
@socket_authentication
def connect():
    send("###", room=request.sid)
    user_pool[request.identity] = request.sid
    print(request.identity)
    print("\n"*8)
    print(f"\t\t\t{request.identity} CONNECTED")
    print(", ".join(user_pool.keys()))
    print("\n"*8)
    
@socketapp.on('disconnect')
@socket_authentication
def disconnect():
    user_pool.pop(request.identity)
    print("\n"*8)
    print(f"\t\t\t{request.identity} DISCONNECTED")
    print(", ".join(user_pool.keys()))
    print("\n"*8)