from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///userdata.db'
db = SQLAlchemy(app)

class Message(db.Model):
	sender_id: int
	receiver_id: int
	timestamp: int
	length: int
	text: str

	def get_messages_before(self, timestamp: int):
		pass
