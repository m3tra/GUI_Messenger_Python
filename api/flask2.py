from flask import Flask, render_template
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

class Message(Resource):
	sender_id: int
	receiver_id: int
	timestamp: int
	length: int
	text: str

	def get(self):
		return {"data": "Hello World"}

	def get_messages_before(self, timestamp: int):
		pass

api.add_resource(Message, "/message")

if __name__ == "__main__":
	app.run(debug=True)
