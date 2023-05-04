from app import socketapp
from api.socket import user_pool


# Emits a connection request refresh to the targetted user.
def emit_conn_request(user):
    if user.email in user_pool:
        socketapp.emit(
            "connection requests", parse_conn_req(user), room=user_pool[user.email]
        )


# Emits a connection refresh to the targetted user.
def emit_conn(user):
    if user.email in user_pool:
        socketapp.emit("connection", parse_conn(user), room=user_pool[user.email])


"""
Socket Event Utilities
"""


# Parses the connection request.
def parse_conn_req(user):
    return {
        "IncomingConnection": [
            conn.user_1.parse_private() for conn in user.incoming_connection_requests
        ],
        "OutgoingConnection": [
            conn.user_2.parse_private() for conn in user.outgoing_connection_requests
        ],
    }


# Parses the connections.
def parse_conn(user):
    return {
        "Connections": [
            c.user_1.parse() if c.user_2.email == user.email else c.user_2.parse()
            for c in user.connected
        ]
    }
