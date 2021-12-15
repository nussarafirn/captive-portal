from flask import Flask, jsonify, request, session, redirect
from passlib.hash import pbkdf2_sha256
import uuid


from enum import Enum
from app import auth_writer
import json



class Message(Enum):
    DISCONNECT_MSG = 1
    AUTHENTICATE_CLIENT = 2
    INFORM_CONTROLLER = 3
    CONTROLLER_NOTIFICATION = 4
    USER_AUTHENTICATED = 5
    USER_NOT_AUTHENTICATED = 6
    LOCAL_TEST = 9999




class User:

  def start_session(self, user):
    del user['password']
    session['logged_in'] = True
    session['user'] = user
    return jsonify(user), 200

  def signup(self):
    print(request.form)

    # Create the user object
    user = {
      "_id": uuid.uuid4().hex,
      "name": request.form.get('name'),
      "email": request.form.get('email'),
      "password": request.form.get('password')
    }

    # Encrypt the password
    user['password'] = pbkdf2_sha256.encrypt(user['password'])

    # # Check for existing email address
    # if db.users.find_one({ "email": user['email'] }):
    #   return jsonify({ "error": "Email address already in use" }), 400

    # if db.users.insert_one(user):
    #   return self.start_session(user)

    # return jsonify({ "error": "Signup failed" }), 400
    return jsonify(user), 200
  
  def signout(self):
    session.clear()
    return redirect('/')
  
  def login(self):

    print("***************entered login func**********")


    
    '''user = {
          "type": "",
          "data": {
              "ipv4_adr": "",
              "status": ""
          }
      }
      '''


    #retrive info from UI to create a user object
    user = {
        "type": Message.AUTHENTICATE_CLIENT.value,
        "data": {
          'user_ip': request.environ['REMOTE_ADDR'],
          "email": request.form.get('email'),
          "password": request.form.get('password'),
          "status": "not authenticated"
        }
    }

    print("***************user**********")
    print(user)

    if (len(user) != 0 and user['type'] == 2):
        auth_writer.write(json.dumps(user))
        auth_writer.write('\n')
        auth_writer.flush()
        
        return jsonify(user), 200

    return jsonify({ "error": "Invalid login credentials" }), 401
