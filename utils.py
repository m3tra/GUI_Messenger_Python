import hashlib, sqlite3

def hash256(str):
	try:
		return hashlib.sha256(str.encode()).hexdigest()
	except:
		print("Failed hashing")
		exit()

def init_database(app):
		try:
			app.db_conn = sqlite3.connect("userdata.db")
			app.cur = app.db_conn.cursor()
			app.cur.execute("""
			CREATE TABLE IF NOT EXISTS userdata (
				id INTEGER PRIMARY KEY,
				username VARCHAR(255) NOT NULL,
				password VARCHAR(255) NOT NULL
			)
			""")
			print("Database initialized")
		except:
			print("Failed to connect to database")
			exit()
