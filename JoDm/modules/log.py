import time
import os
from colorama import Fore

class Log:
    def __init__(self):
        pass

    def fatal(self, message):
        print(f"{Fore.RED}[X]{Fore.RESET} --> {message}")
        exit()

    def suc(self, message):
        print(f"{Fore.GREEN}[+]{Fore.RESET} --> {message}")

    def inf(self, message):
        print(f"{Fore.BLUE}[I]{Fore.RESET} --> {message}")

    def error(self, message):
        print(f"{Fore.LIGHTRED_EX}[-]{Fore.RESET} --> {message}")

    def dbg(self, message):
        print(f"{Fore.LIGHTYELLOW_EX}[D]{Fore.RESET} --> {message}")

