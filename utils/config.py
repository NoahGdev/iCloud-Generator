import json
import os
import sys
from colorama import Fore, init
import csv
init()

def line_prepender(filename, header):
    header = header.split(",")
    with open(filename, "r") as csvfile:
        csvreader = csv.reader(csvfile)
        rows = []
        next(csvreader)
        for row in csvreader:
            rows.append(row)
        rows.insert(0, header)
    with open(filename,"w", encoding='UTF8', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(rows)

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
    with open("config.json", "r+") as f:
        data = json.load(f)
        
        if data['webhook'] == "":
            print(Fore.LIGHTRED_EX + f'Notice: Webhook is empty -> Not sending webhooks' + Fore.WHITE)
            
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
    
def makeCSV():
    filenameiCloud = "Accounts/Generated.csv"
    os.makedirs(os.path.dirname(filenameiCloud), exist_ok=True)
    try:
        columnNamesiCloud = ['APPLE ID', 'EMAIL', 'ANONYMOUS ID', 'PROXY', 'DATE']
        with open(filenameiCloud, encoding="utf8") as einhalbFile:
            einhalbReader = csv.reader(einhalbFile, delimiter=',')
            line_count = 0
            for row in einhalbReader:
                if line_count == 0:
                    columnNamesiCloudUser = row
                    line_count += 1
                else:
                    line_count += 1

        if columnNamesiCloud != columnNamesiCloudUser:
            mystring = ",".join(columnNamesiCloud)
            line_prepender(filenameiCloud, mystring)
            print(Fore.LIGHTRED_EX + 'Repaired Invalid iCloud Accounts CSV File' + Fore.WHITE)
    except Exception as e:
        try:
            with open(filenameiCloud, 'w', encoding='UTF8') as f:
                writer = csv.writer(f)
                writer.writerow(columnNamesiCloud)
        except Exception as e:
            pass
