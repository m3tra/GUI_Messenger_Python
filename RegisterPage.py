import customtkinter as ctk

from utils import hash256

class RegisterPage:
	def __init__(self, app):
		self.app = app

		self.has_error = False

		self.frame = ctk.CTkFrame(master=app.root)
		self.frame.pack(pady=20, padx=60, fill="both", expand=True)

		self.label = ctk.CTkLabel(master=self.frame, text="Register")
		self.label.pack(pady=12, padx=10)

		self.user_entry = ctk.CTkEntry(master=self.frame, placeholder_text="Username")
		self.user_entry.pack(pady=12, padx=10)

		self.pw_entry = ctk.CTkEntry(master=self.frame, placeholder_text="Password", show="*")
		self.pw_entry.pack(pady=12, padx=10)
		self.pw_entry_2 = ctk.CTkEntry(master=self.frame, placeholder_text="Confirm Password", show="*")
		self.pw_entry_2.pack(pady=12, padx=10)
		self.pw_entry.option_get

		self.register_btn = ctk.CTkButton(master=self.frame, text="Register", fg_color="purple3", hover_color="purple4", command=lambda: self.register())
		self.register_btn.pack(pady=12, padx=10)

		self.login_label = ctk.CTkLabel(master=self.frame, text="Already registered?")
		self.login_label.pack(pady=0, padx=10)

		self.login_page_btn = ctk.CTkButton(master=self.frame, text="Login", command=lambda: self.goto_login_page())
		self.login_page_btn.pack(pady=0, padx=10)

	def hide(self):
		self.frame.destroy()

	def goto_login_page(self):
		from LoginPage import LoginPage

		self.app.login_page = LoginPage(self.app)
		self.hide()
		# self.app.register_page.frame.pack_forget()
		# self.app.login_page.frame.pack(pady=20, padx=60, fill="both", expand=True)

	def hide_error(self):
		if self.has_error:
			self.error_text.destroy()

	def show_error(self, error_msg):
		self.hide_error()

		self.has_error = True
		print(error_msg)
		self.error_text = ctk.CTkLabel(master=self.frame, text=error_msg, text_color="red3")
		self.error_text.pack(pady=0, padx=10)

	def register(self):
		user = self.user_entry.get()
		pw1 = self.pw_entry.get()
		pw2 = self.pw_entry_2.get()

		if user == "":
			self.show_error("Username required")
			return
		if pw1 != pw2:
			self.show_error("Passwords don't match")
			return
		if not pw1:
			self.show_error("Password required")
			return

		# Check for existing user
		self.app.cur.execute("SELECT * FROM userdata WHERE username = ?", (user,))
		found = self.app.cur.fetchone()
		if found:
			self.show_error("User already exists")
			return

		self.hide_error()

		hashed_pw = hash256(pw1)
		self.app.cur.execute("INSERT INTO userdata (username, password) VALUES (?, ?)", (user, hashed_pw))
		self.app.db_conn.commit()

		self.success_text = ctk.CTkLabel(master=self.frame, text="Registered", text_color="green")
		self.success_text.pack(pady=0, padx=10)
