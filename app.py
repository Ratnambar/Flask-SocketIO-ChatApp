from flask import Flask, render_template, url_for,request,redirect,request
from flask_socketio import SocketIO,leave_room
from flask_login import login_user,LoginManager,login_required,logout_user,current_user
from db import get_user,save_user,get_all_user,save_messages,get_messages,get_all_rooms,save_rooms
from pymongo.errors import DuplicateKeyError
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key-is!'
socketio = SocketIO(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "users.login"


@app.route('/')
@login_required
def home():
	l=[]
	rooms = get_all_rooms()
	for room in rooms:
		room_name = room['room_name']
		l.append(room_name)
	return render_template('index.html',room_name=l)


@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	message = ''
	if request.method == 'POST':
		username = request.form.get('username')
		password_input = request.form.get('password')
		user = get_user(username)

		if user and user.check_password(password_input):
			login_user(user)
			return redirect(url_for('home'))
		else:
			message = 'User is not exist.'
	return render_template('login.html', message=message)



@app.route('/signup',methods=['GET', 'POST'])
def signup():
	if current_user.is_authenticated:
		return redirect(url_for('home'))

	message = ''
	if request.method == 'POST':
		username = request.form.get('username')
		email = request.form.get('email')
		password = request.form.get('password')
		try:
			save_user(username,email,password)
			return redirect(url_for('login'))
		except DuplicateKeyError:
			message = 'User is already exist.'
	return render_template('signup.html',message=message)



@app.route('/<room_name>',methods=['GET','POST'])
def handle_newUser_message(room_name):
	l = []
	if current_user.is_authenticated:
		all_messages = get_messages(room_name)
		rooms = get_all_rooms()
		for room in rooms:
			room_name = room['room_name']
			l.append(room_name)
		for message in all_messages:
			print(message)
		return render_template('chat.html',all_messages=all_messages,room_name=room_name,room_name_list=l)
	return redirect(url_for('home'))


@login_manager.user_loader
def load_user(username):
    return get_user(username)



@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))



@socketio.on('send_message')
def handle_send_message(data):
	save_messages(data['message'],data['sender'],data['room_name'],datetime.now())
	socketio.emit('receive_message',data=data);


if __name__ == '__main__':
    socketio.run(app,debug=True)
