class App:
	def __init__(self, root):
		from utils import init_database
		from LoginPage import LoginPage
		from RegisterPage import RegisterPage

		self.root = root

		init_database(self)

		# self.register_page = RegisterPage(self)
		# self.register_page.frame.pack_forget()
		self.login_page = LoginPage(self)
