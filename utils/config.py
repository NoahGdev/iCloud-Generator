import json
import os
import sys
from colorama import Fore, init
init()

def makeConfig():
    jsonFileData = {
        "webhook": "",
        "delay": "",
        "retryDelay": ""
    }
    try:
        t = os.path.exists("config.json")
        if t == False:
            with open("config.json", "w+") as f:
                json.dump(jsonFileData, f, indent=4)
    except Exception as e:
        t = os.path.exists("config.json")
        if t == False:
            print(Fore.LIGHTRED_EX + f'Error Generating Config File: {e}' + Fore.WHITE)
            input()
            sys.exit()

def getConfig():
    with open("config.json", "r") as f:
        data = json.load(f)
        return data
    

def updateConfig(pref, data1):
    pref.seek(0)
    try:
        pref.truncate(0)
    except Exception as e:
        pass
    pref.write(json.dumps(data1, indent=4))
    
def checkConfig():
    with open("config.json", "r") as f:
        data = json.load(f)
        
        if data['webhook'] == "":
            print(Fore.LIGHTRED_EX + f'Notice: Webhook is empty -> Not sending wedbhooks' + Fore.WHITE)
            
        if data['delay'] == "":
            print(Fore.LIGHTRED_EX + f'Notice: Delay is empty -> defaulting to 10' + Fore.WHITE)
            data['delay'] = "10"
            updateConfig(f, data)
            
        if data['retryDelay'] == "":
            print(Fore.LIGHTRED_EX + f'Notice: retryDelay is empty -> defaulting to 10' + Fore.WHITE)
            data['retryDelay'] = "10"
            updateConfig(f, data)
        
def makeProxies():
    open("proxies.txt", 'a').close()