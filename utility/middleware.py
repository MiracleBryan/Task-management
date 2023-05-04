from flask import request
from flask_jwt_extended import decode_token

def socket_authentication(f):
    def wrapper():
        try:
            access_token = request.headers["Authentication"][len("Bearer "):].encode("ascii")
            identity = decode_token(access_token)["sub"]
            request.identity = identity # This is just the email
            f()
        except:
            pass
    return wrapper