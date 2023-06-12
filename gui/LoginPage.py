import customtkinter as ctk

from utils import hash256, show_error, hide_error, show_success

class LoginPage:
	from App import App
	def __init__(self, app: App) -> None:
		self.app = app

		self.logged_in: bool = False

		self.has_error: bool = False
		self.error: ctk.CTkLabel

		self.success_text: ctk.CTkLabel

		self.fill_page()


	def fill_page(self) -> None:
		self.frame = ctk.CTkFrame(master=self.app.root)
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


	def clear_entries(self) -> None:
		from utils import clear_entry

		clear_entry(self.username_entry)
		clear_entry(self.password_entry)


	def goto_register_page(self) -> None:
		self.clear_entries()
		hide_error(self)
		self.frame.pack_forget()

		# Lose focus of previous clicked entry field
		self.app.root.focus()

		self.app.register_page.frame.pack(pady=20, padx=60, fill="both", expand=True)

		print()
		print("* Switched to register page *")


	def login(self) -> None:
		username: str = self.username_entry.get()
		password: str = self.password_entry.get()

		if not username:
			show_error(self, "Username required")
			return
		if not password:
			show_error(self, "Password required")
			return

		self.app.cursor.execute("SELECT * FROM userdata WHERE username = ? AND password = ?", (username, hash256(password)))
		found: tuple[int, str, str] | None = self.app.cursor.fetchone()

		if not found:
			show_error(self, "Login failed")
			return
		hide_error(self)

		if not self.logged_in:
			show_success(self, "Login successful")
			self.logged_in = True
