# import signal
import rsa

from colorama import Fore

ASYM_KEYS_LEN = 2048
DEFAULT_PORT = 9999
MSG_BUF_SIZE = 1024
# chosen_port: int

# class clr:
# 	LILAC = '\033[95m'
# 	BLUE = '\033[94m'
# 	CYAN = '\033[96m'
# 	GREEN = '\033[92m'
# 	YELLOW = '\033[93m'
# 	RED = '\033[91m'
# 	RST = '\033[0m'
# 	BOLD = '\033[1m'
# 	UNDERLINE = '\033[4m'

SERVER_PLACEHOLDER = Fore.RED + "SERVER" + Fore.RESET
CLIENT_PLACEHOLDER = Fore.RED + "CLIENT" + Fore.RESET


# def signal_handler(sig, frame) -> None:
# 	print(Fore.RED + "\nExit" + Fore.RESET)
# 	exit(0)


# signal.signal(signal.SIGINT, signal_handler)


def key_gen(key_length: int) -> tuple[rsa.PublicKey, rsa.PrivateKey]:
	print(Fore.YELLOW + "GENERATING ENCRYPTION KEYS (RSA-2048) " + Fore.RESET, end="", flush=True)

	(PUBLIC_KEY, PRIVATE_KEY) = rsa.newkeys(key_length)

	print(Fore.GREEN + "DONE" + Fore.RESET)

	return (PUBLIC_KEY, PRIVATE_KEY)


if __name__ == "__main__":
	(PUBLIC_KEY, PRIVATE_KEY) = key_gen(2048)

	print("Init modes: ", end="", flush=True)
	print(Fore.MAGENTA + "host(" + Fore.RESET + "1" + Fore.MAGENTA + ")" + Fore.BLUE + " client(" + Fore.RESET + "2" + Fore.BLUE + ") " + Fore.RESET, end="", flush=True)

	choice = input("Mode: ")

	# chosen_port = int(input("Choose port [" + Fore.YELLOW + "1024" + Fore.RESET + "-" + Fore.YELLOW + "65535" + Fore.RESET + "] (default " + Fore.YELLOW + str(DEFAULT_PORT) + Fore.RESET + "): "))
	# if chosen_port and chosen_port < 1024 or chosen_port >= 65535:
	# 	chosen_port = DEFAULT_PORT
	# else:
	# 	chosen_port = DEFAULT_PORT

	if choice == "1":	# Server Mode
		print(Fore.MAGENTA + "[ SERVER MODE ]" + Fore.RESET)

		from Server import Server
		Server()

	elif choice == "2":	# Client Mode
		print(Fore.BLUE + "[ CLIENT MODE ]" + Fore.RESET)
		from Client import Client
		Client()

	else:
		exit(0)
