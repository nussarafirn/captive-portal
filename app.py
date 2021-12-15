from flask import Flask, render_template, session, redirect
from functools import wraps

import eventlet


app = Flask(__name__)
app.secret_key = b'\xcc^\x91\xea\x17-\xd0W\x03\xa7\xf8J0\xac8\xc5'




# TODO:NEW set up sockets
#   turns internal socket api to green threads
eventlet.monkey_patch(socket=True)

#   socket to Authenticator
addr_auth = '127.0.0.1'
port = 5050
auth_socket = eventlet.connect((addr_auth, port))

print(f"[AUTH CONNECTED]: A auth socket is connect on {addr_auth}")

#   set up a reader & writer to auth
auth_writer = auth_socket.makefile('w')
auth_reader = auth_socket.makefile('r')

# TODO is this where the listener should be?
# listen_to_auth(reader=auth_reader)
print(app.instance_path)
print(app.root_path)
app.run(debug=True)




from user import routes

# Decorators
def login_required(f):
  @wraps(f)
  def wrap(*args, **kwargs):
    if 'logged_in' in session:
      return f(*args, **kwargs)
    else:
      return redirect('/')
  
  return wrap



@app.route('/')
def home():
  return render_template('home.html')

@app.route('/dashboard/')
@login_required
def dashboard():
  return render_template('dashboard.html')

@app.route('/wait/')
def wait():
  return render_template('wait.html')


