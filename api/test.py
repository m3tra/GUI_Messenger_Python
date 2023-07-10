import requests
from colorama import Fore

BASE = "http://127.0.0.1:5000/"
ENDPOINT = "get-user/"
ID = "1"
EXTRA = "?extra=test"

response = requests.get(BASE + ENDPOINT + ID + EXTRA)
print("Status code:", response.status_code)
if response:
	print(response.json())
else:
	print(Fore.RED + "Endpoint not found, null response" + Fore.RESET)
