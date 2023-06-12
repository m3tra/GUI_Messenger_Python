import socket
import time
import rsa
import signal
import threading

from colorama import Fore

from secure import ASYM_KEYS_LEN, DEFAULT_PORT, MSG_BUF_SIZE
from secure import SERVER_PLACEHOLDER, CLIENT_PLACEHOLDER
from secure import key_gen

# import keyboard


# def key_handler():
# 	while True:
# 		if keyboard.read_key() == "p":
# 			print("You pressed p")
# 			break


# def signal_handler(sig, frame):
# 	if connected:
# 		send_message(client, "!disconnect")
# 	client.close()
# 	print(Fore.RED + "\nExit" + Fore.RESET)
# 	exit(0)


# signal.signal(signal.SIGINT, signal_handler)


class Client:
	def __init__(self) -> None:
		self.connected: bool = False
		(self.pub_key, self.priv_key) = key_gen(ASYM_KEYS_LEN)

		# Create a TCP/IP socket
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		self.find_server()

		self.exchange_keys()

		print(" | Connection " + Fore.GREEN + "ESTABLISHED" + Fore.RESET)
		print("###########################################################")

		threading.Thread(target=self.sending_messages).start()
		threading.Thread(target=self.receiving_message).start()


	def exchange_keys(self) -> None:
		print("Exchanging Keys ", end="", flush=True)

		# Receive Pub Key: Server --> Client
		self.server_pub_key = rsa.PublicKey.load_pkcs1(self.socket.recv(MSG_BUF_SIZE))

		# Send Pub Key: Client --> Server
		self.socket.send(self.pub_key.save_pkcs1("PEM"))

		print(Fore.GREEN + "DONE" + Fore.RESET, end="", flush=True)


	def find_server(self) -> None:
		print("Waiting for server on port " + Fore.YELLOW + str(DEFAULT_PORT) + Fore.RESET)
		self.connect_to_server()

		self.tries = 1

		while not self.connected:
			print(".", end="", flush=True)
			self.tries += 1
			time.sleep(1)
			self.connect_to_server()


	def connect_to_server(self) -> None:
		if self.connected:
			return

		try:
			self.socket.connect(("localhost", DEFAULT_PORT))
			if self.tries == 1:
				print(" | ", end="", flush=True)
			print(Fore.MAGENTA + "Server " + Fore.GREEN + "FOUND" + Fore.RESET)

			self.connected = True
		except:
			pass


	def receiving_message(self) -> None:
		if not self.connected:
			return

		while True:
			encrypted_message = self.socket.recv(MSG_BUF_SIZE)

			try:
				clear_message = rsa.decrypt(encrypted_message, self.priv_key).decode("utf-8")

				if (clear_message == "!disconnect"):
					self.connected = False
					self.socket.close()
					self.find_server()
					continue

				print(Fore.CYAN + "Peer[" + SERVER_PLACEHOLDER + Fore.CYAN + "]: " + Fore.RESET + clear_message)
			except:
				print(Fore.RED + "Failed to decrypt message" + Fore.RESET)


	def sending_messages(self) -> None:
		if not self.connected:
			return

		while True:
			clear_message = input("")
			encrypted_message = rsa.encrypt(clear_message.encode("utf-8"), self.server_pub_key)
			self.socket.send(encrypted_message)

			print(Fore.GREEN + "Self[" + CLIENT_PLACEHOLDER + Fore.GREEN + "]: " + Fore.RESET + clear_message)



if __name__ == "__main__":
	client = Client()

	def signal_handler(sig, frame) -> None:
		# client.socket.shutdown(socket.SHUT_RDWR)
		client.socket.close()

		print(Fore.RED + "\nExit" + Fore.RESET)
		exit(0)


	signal.signal(signal.SIGINT, signal_handler)
