import requests
from database.models import User, Connection

"""
Purpose is to test connection API.
"""

auth_header = ''
base_url = 'http://localhost:5000'

def post(path, data):
    return requests.post(f'{base_url}{path}', headers={'Authorization':auth_header}, data=data)
def put(path, data):
    return requests.put(f'{base_url}{path}', headers={'Authorization':auth_header}, data=data)

def login(email, password):
    r = post('/user/login', {'email':email, 'password':password})
    global auth_header
    auth_header = f'Bearer {r.json()["access_token"]}'

def create_user(name, email, password):
    post('/user', {'name':name, 'email':email, 'password':password})

def add_connection_request(email):
    return post('/connectionrequest', {'email':email})

def accept_connection_request(email):
    return put('/connectionrequest', {'email':email})

# Tests #

def test_connected():
    create_user('Apple', 'test@gmail.com', '123')
    create_user('Orange', 'test2@gmail.com', '123')
    
    login('test2@gmail.com', '123')

    r = add_connection_request('test@gmail.com')
    print(r)
    r = accept_connection_request('test@gmail.com')
    print(r.json())
    r = accept_connection_request('test2@gmail.com')
    print(r.json())
    
    login('test@gmail.com', '123')
    r = accept_connection_request('test@gmail.com')
    print(r.json())
    r = accept_connection_request('test2@gmail.com')
    print(r.json())

test_connected()