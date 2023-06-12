import customtkinter as ctk
import sqlite3

from colorama import Fore
from gui.LoginPage import LoginPage
from gui.RegisterPage import RegisterPage

class App:
	def __init__(self) -> None:
		self.root = self.init_window()

		(self.db_conn, self.cursor) = self.init_database("userdata.db")

		self.register_page = RegisterPage(self)
		# self.register_page.frame.pack_forget()

		self.login_page = LoginPage(self)
		# self.login_page.frame.tkraise(aboveThis=self.register_page.frame)

		self.root.mainloop()


	def init_window(self) -> ctk.CTk:
		ctk.set_appearance_mode("dark")
		ctk.set_default_color_theme("dark-blue")

		root = ctk.CTk()

		root.geometry("500x450")
		root.minsize(300, 375)
		root.maxsize(500, 450)

		root.title("Secure Messaging App")

		return root

	def init_database(self, db_filename: str) -> tuple[sqlite3.Connection, sqlite3.Cursor]:
		try:
			db_conn = sqlite3.connect(db_filename)
			cursor = db_conn.cursor()
			cursor.execute("""
				CREATE TABLE IF NOT EXISTS userdata (
					id INTEGER PRIMARY KEY,
					username VARCHAR(255) NOT NULL,
					password VARCHAR(255) NOT NULL
				)
			""")

			print("####################")
			print("Database initialized")
			print("####################")
			print()

			return (db_conn, cursor)
		except:
			print(Fore.RED + "Failed to connect to database" + Fore.RESET)
			exit(1)
