import customtkinter as ctk
import hashlib

from colorama import Fore
from gui.LoginPage import LoginPage
from gui.RegisterPage import RegisterPage

def hash256(string: str) -> str:
	try:
		return hashlib.sha256(string.encode("utf-8")).hexdigest()
	except:
		print(Fore.RED + "Failed hashing" + Fore.RESET)
		exit(1)


def clear_entry(entry: ctk.CTkEntry) -> None:
	entry.delete(0, len(entry.get()))


def show_error(page: LoginPage | RegisterPage, error_msg: str) -> None:
	hide_error(page)

	page.has_error = True
	print(Fore.RED + error_msg + Fore.RESET)

	page.error = ctk.CTkLabel(master=page.frame, text=error_msg, text_color="red3")
	page.error.pack(pady=0, padx=10)


def hide_error(page: LoginPage | RegisterPage) -> None:
	if page.has_error:
		page.error.destroy()
	page.has_error = False


def show_success(page: LoginPage | RegisterPage, success_msg: str) -> None:
	print(Fore.GREEN + success_msg + Fore.RESET)

	page.success_text = ctk.CTkLabel(master=page.frame, text=success_msg, text_color="green")
	page.success_text.pack(pady=0, padx=10)
