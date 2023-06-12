import socket
import time
import rsa
import signal
import threading

from colorama import Fore

from secure import SERVER_PLACEHOLDER, CLIENT_PLACEHOLDER
from secure import ASYM_KEYS_LEN, DEFAULT_PORT, MSG_BUF_SIZE
from secure import key_gen


class Server():
	def __init__(self) -> None:
		self.clients: list[tuple[socket.socket, socket._RetAddress]] = []
		# self.connected: bool = False
		(self.pub_key, self.priv_key) = key_gen(ASYM_KEYS_LEN)

		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		self.socket_bound = False
		self.bind_socket()

		self.listen_for_client()

		self.exchange_keys()

		print(" | Session " + Fore.GREEN + "ESTABLISHED" + Fore.RESET)
		print("###########################################################")

		threading.Thread(target=self.sending_messages, args=(self.client_conn,)).start()
		threading.Thread(target=self.receiving_message, args=(self.client_conn,)).start()


	def listen_for_client(self) -> None:
		self.socket.listen()
		print(Fore.GREEN + "Listening " + Fore.RESET + "for " + Fore.BLUE + "clients" + Fore.RESET, end="", flush=True)

		(self.client_conn, (client_addr, client_port)) = self.socket.accept()

		self.clients.append((self.client_conn, (client_addr, client_port)))
		print(" | " + Fore.BLUE + "Client " + Fore.GREEN + "CONNECTED" + Fore.RESET)


	def bind_socket(self) -> None:
		print("Binding port " + Fore.YELLOW + str(DEFAULT_PORT) + Fore.RESET, end="", flush=True)

		self.tries = 0
		while not self.socket_bound:
			try:
				self.socket.bind(("localhost", DEFAULT_PORT))
				self.tries = 1

				self.socket_bound = True
			except socket.error as msg:
				# if self.tries == 3:
				# 	DEFAULT_PORT -= 1
				# 	print("\nPort switched to " + Fore.YELLOW + str(DEFAULT_PORT), end="", flush=True)
				# 	return

				print(Fore.RED + "\nSocket binding error: " + str(msg) + "\n" + Fore.RESET + "Retrying in 5", end="", flush=True)
				waiting_time: int = 4
				for i in range(waiting_time):
					time.sleep(1)
					print(", " + str(waiting_time - i), end="", flush=True)
				time.sleep(1)
				self.tries += 1


	def exchange_keys(self) -> None:
		print("Exchanging Keys ", end="", flush=True)

		# Send Pub Key: Server --> Client
		self.client_conn.send(self.pub_key.save_pkcs1("PEM"))

		# Receive Pub Key: Client --> Server
		self.peer_pub_key = rsa.PublicKey.load_pkcs1(self.client_conn.recv(MSG_BUF_SIZE))

		print(Fore.GREEN + "DONE" + Fore.RESET, end="", flush=True)


	def receiving_message(self, client: socket.socket) -> None:
		while True:
			received_enc_message = client.recv(MSG_BUF_SIZE)

			try:
				clear_message = rsa.decrypt(received_enc_message, self.priv_key).decode("utf-8")
			except:
				self.client_conn.close()
				self.listen_for_client()
				return

			if (clear_message == "!disconnect"):
				self.client_conn.close()
				self.listen_for_client()
				return

			print(Fore.CYAN + "Peer[" + CLIENT_PLACEHOLDER + Fore.CYAN + "]: " + Fore.RESET + clear_message)


	def sending_messages(self, client: socket.socket) -> None:
		while True:
			clear_message = input("")

			self.send_message(client, clear_message)

			print(Fore.GREEN + "Self[" + SERVER_PLACEHOLDER + Fore.GREEN + "]: " + Fore.RESET + clear_message)


	def send_message(self, client: socket.socket, clear_message: str) -> None:
		encrypted_message = rsa.encrypt(clear_message.encode("utf-8"), self.peer_pub_key)
		client.send(encrypted_message)


if __name__ == "__main__":
	server = Server()

	def signal_handler(sig, frame):
		for c in server.clients:
			client_socket = c[0]
			server.send_message(client_socket, "!disconnect")
			client_socket.close()

		if server.socket:
			# server.socket.shutdown(socket.SHUT_RDWR)
			server.socket.close()

		print(Fore.RED + "\nExit" + Fore.RESET)
		exit(0)

	signal.signal(signal.SIGINT, signal_handler)
