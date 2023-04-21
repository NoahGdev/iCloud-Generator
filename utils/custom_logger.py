import threading
from colorama import Fore, Style, init
import sys
from datetime import datetime

init(autoreset=True)

class CustomLogger:
    _lock = threading.Lock()

    @staticmethod
    def _print(color, tag, message):
        with CustomLogger._lock:
            sys.stdout.write("[" + tag + "] " + color + message + Style.RESET_ALL + "\n")

    @staticmethod
    def error(message):
        CustomLogger._print(Fore.RED, str(datetime.now()).split(" ")[1][:-4], message)

    @staticmethod
    def success(message):
        CustomLogger._print(Fore.GREEN, str(datetime.now()).split(" ")[1][:-4], message)

    @staticmethod
    def debug(message):
        CustomLogger._print(Fore.CYAN, str(datetime.now()).split(" ")[1][:-4], message)

    @staticmethod
    def critical(message):
        CustomLogger._print(Fore.MAGENTA, str(datetime.now()).split(" ")[1][:-4], message)

    @staticmethod
    def warning(message):
        CustomLogger._print(Fore.LIGHTYELLOW_EX, str(datetime.now()).split(" ")[1][:-4], message)
