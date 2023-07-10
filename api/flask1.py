from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route("/login", methods=["POST", "GET"])
def login(self):
	return render_template("login.html")



@app.route("/<usr>")
def user(usr):
	return f"<h1>{usr}</h1>", 200



@app.route("/get-user/<user_id>", methods=["GET"])
def get_user(user_id):
	user_data = {
		"user_id": user_id,
		"name": "Swagger",
		"email": "swag@test.com"
	}

	extra = request.args.get("extra")
	if extra:
		user_data["extra"] = extra

	return jsonify(user_data), 200



@app.route("/create-user", methods=["POST"])
def create_user():
	data = request.get_json()

	return jsonify(data), 201



@app.route("/")
def home():
	return "Home"

# if __name__ == "__main__":
app.run(debug=True)



# GET		Request
# POST		Create
# PUT		Update
# DELETE	Delete
