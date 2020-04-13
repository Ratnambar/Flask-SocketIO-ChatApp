from pymongo import MongoClient,DESCENDING
from werkzeug.security import generate_password_hash
from datetime import datetime
from user import User

client = MongoClient("mongodb+srv://ambarkr123:ambarkr123@chatapp-ldmf4.mongodb.net/test?retryWrites=true&w=majority")

db = client.get_database('MyChatApp')
collections = db.get_collection('ChatApp')
messages_collections = db.get_collection('Messages')
room_collections = db.get_collection('Room')



def save_user(username,email,password):
	password_hash = generate_password_hash(password)
	collections.insert_one({'_id':username,'email':email,'password':password_hash})


def get_user(username):
    user_data = collections.find_one({'_id': username})
    return User(user_data['_id'], user_data['email'], user_data['password']) if user_data else None

def get_all_user():
	all_user_data = collections.find()
	return all_user_data


def get_all_rooms():
	room = room_collections.find({})
	return room
	
def save_messages(text,sender,room_name,send_at):
	messages_collections.insert_one({'text':text,'sender':sender,'room_name':room_name,'send_at':datetime.now()})
	# print(room_name)

def get_messages(room_name):
	all_messages = list(messages_collections.find({'room_name':room_name}))
	for message in all_messages:
		message['send_at'] = message['send_at'].strftime("%d %b, %H:%M")
	return all_messages
