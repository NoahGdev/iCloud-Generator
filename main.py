from colorama import Fore, Style, init
from pyfiglet import figlet_format
import os
from termcolor import colored
import six
from utils.custom_logger import CustomLogger as log
from utils.config import getConfig, makeConfig, makeProxies, checkConfig, makeCSV
import itertools

from src.iCloud import iCloud

## INIT

makeConfig()
userConfig = getConfig()
makeProxies()
checkConfig()
makeCSV()

successfulEntries = itertools.count()
failedEntries = itertools.count()

# Menu

def menu_log(string, color, font="slant", figlet=False):
    if colored:
        if not figlet:
            six.print_(colored(string, color))
        else:
            six.print_(colored(figlet_format(string, font=font), color))
    else:
        six.print_(string)

init()

def start():
    while True:
        os.system("cls")
        word = 'iCloud Generator'
        print(Fore.CYAN + figlet_format(word, font='slant', width=115) + Fore.WHITE)

        term_size = os.get_terminal_size()
        print(Fore.CYAN + '\u2500' * ((term_size.columns // 2) + 3) + Fore.WHITE )

        menu_log(" " * 28 + "Menu" , "cyan")
        print(Fore.CYAN + '\u2500' * ((term_size.columns // 2) + 3) + Fore.WHITE )


        print("\n")
        menu_log("1) Start Gen", "cyan")
        menu_log("2) Start Exporter", "cyan")

        option = int(input("\n> "))

        if option == 1:
            os.system("cls")
            taskCount = "ꝏ"

            generator = iCloud(userConfig, log, successfulEntries, failedEntries)

            clientBuildNumber, number, dsid, cookies, session, theId, pNumber, primaryEmail, driver = generator.openIcloudBrowser()
            generator.generate(clientBuildNumber, number, dsid, cookies, session, theId, pNumber, primaryEmail, taskCount, driver)
            
            input("Press Any Key To Continue")
            continue
            
            
        elif option == 2:
            print(Fore.LIGHTRED_EX + f'I will add this soon, busy right now :)' + Fore.WHITE)
            input("Press Any Key To Continue")
            continue
    
if __name__ == "__main__":
    start()
    
