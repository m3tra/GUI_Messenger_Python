import customtkinter as ctk

def init_window():
	ctk.set_appearance_mode("dark")
	ctk.set_default_color_theme("dark-blue")
	root = ctk.CTk()
	root.geometry("500x450")
	root.minsize(300, 375)
	root.maxsize(500, 450)
	root.title("Secure Messaging App")
	return root

if __name__ == "__main__":
	from App import App

	root = init_window()
	app = App(root)

	# root.bind("<Control-l>", lambda x: hide())
	root.mainloop()
