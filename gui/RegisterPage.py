import customtkinter as ctk

from App import App
from utils import hash256, show_error, hide_error, show_success, clear_entry

class RegisterPage:
	def __init__(self, app: App) -> None:
		self.app = app

		self.has_error: bool = False
		self.error: ctk.CTkLabel

		self.success_text: ctk.CTkLabel

		self.fill_page()


	def fill_page(self) -> None:
		self.frame = ctk.CTkFrame(master=self.app.root)
		# self.frame.pack(pady=20, padx=60, fill="both", expand=True)

		self.label = ctk.CTkLabel(master=self.frame, text="Register an account")
		self.label.pack(pady=12, padx=10)

		self.username_entry = ctk.CTkEntry(master=self.frame, placeholder_text="Username")
		self.username_entry.pack(pady=12, padx=10)

		self.password_entry = ctk.CTkEntry(master=self.frame, placeholder_text="Password", show="*")
		self.password_entry.pack(pady=12, padx=10)
		self.password_entry_2 = ctk.CTkEntry(master=self.frame, placeholder_text="Confirm Password", show="*")
		self.password_entry_2.pack(pady=12, padx=10)
		self.password_entry.option_get

		self.register_btn = ctk.CTkButton(master=self.frame, text="Register", fg_color="purple3", hover_color="purple4", command=lambda: self.register())
		self.register_btn.pack(pady=12, padx=10)

		self.login_label = ctk.CTkLabel(master=self.frame, text="Already registered?")
		self.login_label.pack(pady=0, padx=10)

		self.login_page_btn = ctk.CTkButton(master=self.frame, text="Login", command=lambda: self.goto_login_page())
		self.login_page_btn.pack(pady=0, padx=10)


	def clear_entries(self) -> None:
		clear_entry(self.username_entry)
		clear_entry(self.password_entry)
		clear_entry(self.password_entry_2)


	def goto_login_page(self) -> None:
		self.clear_entries()
		hide_error(self)
		self.frame.pack_forget()

		# Lose focus of previous clicked entry field
		self.app.root.focus()

		self.app.login_page.frame.pack(pady=20, padx=60, fill="both", expand=True)

		print()
		print("* Switched to login page *")


	def register(self) -> None:
		username = self.username_entry.get()
		password_1 = self.password_entry.get()
		password_2 = self.password_entry_2.get()

		if not username:
			show_error(self, "Username required")
			return
		if password_1 != password_2:
			show_error(self, "Passwords don't match")
			return
		if not password_1:
			show_error(self, "Password required")
			return

		# Check for existing user
		self.app.cursor.execute("SELECT * FROM userdata WHERE username = ?", (username,))
		found: tuple[int, str, str] | None = self.app.cursor.fetchone()
		if found:
			show_error(self, "User already exists")
			return

		hide_error(self)

		hashed_password = hash256(password_1)
		self.app.cursor.execute("INSERT INTO userdata (username, password) VALUES (?, ?)", (username, hashed_password))
		self.app.db_conn.commit()

		show_success(self, "Registration successful")
