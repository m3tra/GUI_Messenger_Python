import customtkinter as ctk

from utils import hash256

class LoginPage:
	def __init__(self, app):
		self.app = app

		self.logged_in = False
		self.has_error = False

		self.frame = ctk.CTkFrame(master=app.root)
		self.frame.pack(pady=20, padx=60, fill="both", expand=True)

		self.label = ctk.CTkLabel(master=self.frame, text="Login")
		self.label.pack(pady=12, padx=10)

		self.username_entry = ctk.CTkEntry(master=self.frame, placeholder_text="Username")
		self.username_entry.pack(pady=12, padx=10)

		self.password_entry = ctk.CTkEntry(master=self.frame, placeholder_text="Password", show="*")
		self.password_entry.pack(pady=12, padx=10)

		self.login_btn = ctk.CTkButton(master=self.frame, text="Login", fg_color="purple3", hover_color="purple4", command=lambda: self.login())
		self.login_btn.pack(pady=12, padx=10)

		# self.checkbox = ctk.CTkCheckBox(master=self.frame, text="Remember Me")
		# self.checkbox.pack(pady=12, padx=10)

		self.register_label = ctk.CTkLabel(master=self.frame, text="Don't have an account?")
		self.register_label.pack(pady=0, padx=10)

		self.register_page_btn = ctk.CTkButton(master=self.frame, text="Register", command=lambda: self.goto_register_page())
		self.register_page_btn.pack(pady=0, padx=10)

	# def show(self, register_page):
	# 	register_page.frame.destroy()
	# 	self.frame.pack(pady=20, padx=60, fill="both", expand=True)

	def hide(self):
		self.frame.destroy()

	def goto_register_page(self):
		from RegisterPage import RegisterPage

		self.app.register_page = RegisterPage(self.app)
		self.hide()
		# self.app.login_page.frame.pack_forget()
		# self.app.register_page.frame.pack(pady=20, padx=60, fill="both", expand=True)

	def hide_error(self):
		if self.has_error:
			self.error_text.destroy()
		self.has_error = False

	def show_error(self, error_msg):
		self.hide_error()

		self.has_error = True
		self.error_text = ctk.CTkLabel(master=self.frame, text=error_msg, text_color="red3")
		self.error_text.pack(pady=0, padx=10)

	def show_success(self, success_msg):
		if not self.logged_in:
			self.success_text = ctk.CTkLabel(master=self.frame, text=success_msg, text_color="green")
			self.success_text.pack(pady=0, padx=10)
			self.logged_in = True

	def login(self):
		username = self.username_entry.get()
		password = self.password_entry.get()

		if not username:
			self.show_error("Username required")
			return
		if not password:
			self.show_error("Password required")
			return

		self.app.cur.execute("SELECT * FROM userdata WHERE username = ? AND password = ?", (username, hash256(password)))
		found = self.app.cur.fetchone()

		if not found:
			self.show_error("Login failed")
			return
		self.hide_error()

		self.show_success("Login successful")
