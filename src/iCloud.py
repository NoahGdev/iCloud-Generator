import ctypes
import requests
from discord_webhook import DiscordWebhook, DiscordEmbed
from bs4 import BeautifulSoup
import time
import random
import json
import csv
import platform
import datetime
import uuid

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

from multiprocessing import freeze_support
freeze_support()

successColor = '2284d6'
failColor = 'E24D41'

class iCloud:
    def __init__(self, config, log, succesfulEntries, failedEntries):
        self.config = config
        self.log = log
        self.successfulEntries = succesfulEntries
        self.failedEntries = failedEntries
        self.icloudThread = 1
    
    def getDelay(self, delay):
        if "-" in str(delay):
            delay1 = delay.split("-")[0]
            delay2 = delay.split("-")[1]
            if int(delay2) < int(delay1):
                return delay1
            delaySend = random.randrange(int(delay1), int(delay2))
            return int(delaySend)
        else:
            return int(delay)
        
    def openIcloudBrowser(self):

        def proxies():
            with open("proxies.txt") as f:
                lines = f.read().splitlines()
                if len(lines) > 0:
                    proxies = random.choice(lines)
                    proxySplit = proxies.split(":")
                    proxyDict = {
                        "http": "http://"
                                + proxySplit[2]
                                + ":"
                                + proxySplit[3]
                                + "@"
                                + proxySplit[0]
                                + ":"
                                + proxySplit[1]
                                + "/",
                        "https": "http://"
                                + proxySplit[2]
                                + ":"
                                + proxySplit[3]
                                + "@"
                                + proxySplit[0]
                                + ":"
                                + proxySplit[1]
                                + "/",
                    }
                    return proxyDict
                else:
                    proxyDict = []
                    return proxyDict

        def proxies2():
            with open("proxies.txt") as f:
                lines = f.read().splitlines()
                if len(lines) > 0:
                    proxies = random.choice(lines)
                    proxySplit = proxies.split(":")
                    proxyDict = {
                        "http": "http://"
                                + proxySplit[0]
                                + ":"
                                + proxySplit[1]
                                + "/",
                        "https": "http://"
                                + proxySplit[0]
                                + ":"
                                + proxySplit[1]
                                + "/",
                    }
                    return proxyDict
                else:
                    proxyDict = []
                    return proxyDict

        try:
            proxyDict = proxies()
        except:
            proxyDict = proxies2()

        s = requests.Session()
        if len(proxyDict) > 0:
            s.proxies = proxyDict

        theId = uuid.uuid4()

        store = 'ICLOUD'
        threadnumber = 'LOADING'

        self.log.warning(f"[{threadnumber}] [{store}] Loading Browser..")

        USERAGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
        SECHUA = '".Not/A)Brand";v="99", "Google Chrome";v="111", "Chromium";v="111"'

        delay = self.getDelay(self.config['delay'])

        try:
            chrome_options = uc.ChromeOptions()
            chrome_options.add_argument("--window-size=550,800")
            chrome_options.add_argument(f"--user-agent={USERAGENT}")
            driver = uc.Chrome(use_subprocess=True, options=chrome_options)
        except Exception as e:
            self.log.error(f"[{threadnumber}] [{store}] Error Loading Browser -> {str(e)} -> Sleeping for {str(delay)} seconds")
            time.sleep(int(delay))
            return

        try:
            driver.get("https://www.icloud.com/")

            while True:
                if 'https://www.icloud.com/' in driver.current_url:
                    self.log.warning(f"[{threadnumber}] [{store}] Enter Login Details")
                    break
                else:
                    time.sleep(1)
                    continue

            while True:
                try:
                    getSettings = driver.find_element(By.XPATH, '/html/body/div[1]/ui-main-pane/div/div[2]/div[1]/div[3]/div/main/div/div/div[1]/div[1]/div/div/div/div/div[3]').click()
                    break
                except Exception as e:
                    time.sleep(2)
                    continue

            driver.minimize_window()

            self.log.debug(f"[{threadnumber}] [{store}] Successfully Logged In (do not close window)")

            rr = s.get('https://www.icloud.com/')

            soup = BeautifulSoup(rr.text, 'lxml')
            try:
                clientBuildNumber = soup.find('html')['data-cw-private-build-number']
                number = soup.find('html')['data-cw-private-mastering-number']
            except Exception as e:
                return

            def get_cookies2():
                cookies = {}
                selenium_cookies = driver.get_cookies()
                try:
                    for cookie in selenium_cookies:
                        cookies[cookie['name']] = cookie['value']
                except Exception as e:
                    print("test " + e + " test")
                return cookies

            cookies = get_cookies2()

            headers = {
                'Accept': '*/*',
                'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive',
                'Content-Type': 'text/plain;charset=UTF-8',
                'Origin': 'https://www.icloud.com',
                'Pragma': 'no-cache',
                'Referer': 'https://www.icloud.com/',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-site',
                'User-Agent': USERAGENT,
                'sec-ch-ua': SECHUA,
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
            }

            params = {
                'clientBuildNumber': clientBuildNumber,
                'clientMasteringNumber': number,
                'clientId': str(theId),
            }

            data = 'null'

            response = s.post('https://setup.icloud.com/setup/ws/1/validate', params=params, cookies=cookies, headers=headers, data=data)

            data = json.loads(response.text)

            dsid = data['dsInfo']['dsid']
            notificationId = data['dsInfo']['notificationId']
            aDsID = data['dsInfo']['aDsID']
            primaryEmail = data['dsInfo']['primaryEmail']

            pNumber = data['webservices']['reminders']['url'].split("//")[1].split("-")[0]
            return clientBuildNumber, number, dsid, get_cookies2(), s, theId, pNumber, primaryEmail, driver

        except Exception as e:
            self.log.debug(f"[{threadnumber}] [{store}] Error Logging In -> {e}")
            return False
        
    def generate(self, clientBuildNumber, number, dsid, cookies, session, theId, pNumber, primaryEmail, row_count, driver):
        store = 'ICLOUD'

        USERAGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
        SECHUA = '".Not/A)Brand";v="99", "Google Chrome";v="111", "Chromium";v="111"'

        threadnumber = self.icloudThread
        if int(threadnumber) <= 9:
            threadnumber = '00' + str(threadnumber)
        elif int(threadnumber) <= 99:
            threadnumber = '0' + str(threadnumber)

        def send_embed(primaryEmail, email, proxyToPrintOut):
            if self.config['webhook'] != "":
                webhook = DiscordWebhook(
                    url = self.config['webhook'],
                    username = f"iCloud Generator",
                    rate_limit_retry = True
                )
                embed = DiscordEmbed(
                    title = f'Successfully Created iCloud Email!',
                    url = '',
                    color =successColor,
                    description = f""
                )

                embed.add_embed_field(name='**Site**',value= f'iCloud', inline=False)
                embed.add_embed_field(name='**Task Number**',value= f'||{threadnumber}||', inline=True)
                embed.add_embed_field(name='**Apple ID Email**',value=f'||{primaryEmail}||', inline=True)
                embed.add_embed_field(name='**Email**',value= f'||{email}||', inline=True)
                embed.add_embed_field(name='**Proxy Used**',value= f'||{proxyToPrintOut}||', inline=False)
                embed.set_footer(text=f"iCloud Generator")
                embed.set_timestamp()
                webhook.add_embed(embed)
                response = webhook.execute()
                if response.status_code != 200:
                    self.log.error(f'[{threadnumber}] [{store}] Error Seding Webhook -> {str(response.status_code)}')

        delay = self.getDelay(self.config['delay'])
        retryDelay = self.getDelay(self.config['retryDelay'])

        retry_limit = 10
        tryCount = 0

        self.log.warning(f"[{threadnumber}] [{store}] Generating Email..")

        while True:
            threadnumber = self.icloudThread

            if int(threadnumber) <= 9:
                threadnumber = '00' + str(threadnumber)
            elif int(threadnumber) <= 99:
                threadnumber = '0' + str(threadnumber)

            if tryCount == retry_limit:
                self.log.error(f"[{threadnumber}] [{store}] Error Generating Email -> Max Retries Reached [{str(retry_limit)}] | Ending Task In {str(delay)} Seconds")
                next(self.failedEntries)
                cmdTitle = f"iCloud Generator | Successful Generations: {str(self.successfulEntries).replace('count(', '').replace(')', '')}/{str(row_count)} | Failed Generations: {str(self.failedEntries).replace('count(', '').replace(')', '')}"
                if platform == 'darwin':
                    pass
                else:
                    ctypes.windll.kernel32.SetConsoleTitleW(cmdTitle)
                time.sleep(int(delay))
                
                
                return

            try:
                headers = {
                    'Accept': '*/*',
                    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
                    'Cache-Control': 'no-cache',
                    'Connection': 'keep-alive',
                    'Content-Type': 'text/plain',
                    'Origin': 'https://www.icloud.com',
                    'Pragma': 'no-cache',
                    'Referer': 'https://www.icloud.com/',
                    'Sec-Fetch-Dest': 'empty',
                    'Sec-Fetch-Mode': 'cors',
                    'Sec-Fetch-Site': 'same-site',
                    'User-Agent': USERAGENT,
                    'sec-ch-ua': SECHUA,
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                }

                params = {
                    'clientBuildNumber': clientBuildNumber,
                    'clientMasteringNumber': number,
                    'clientId': theId,
                    'dsid': dsid,
                }

                data = '{}'

                response = session.post(f'https://{pNumber}-maildomainws.icloud.com/v1/hme/generate', params=params, cookies=cookies, headers=headers, data=data)

                if 'success":false' in str(response.text):
                    self.log.error(f"[{threadnumber}] [{store}] Hourly Limit Reached -> Restarting Tasks in 1 hour")
                    time.sleep(300)
                    driver.refresh()
                    time.sleep(300)
                    driver.refresh()
                    time.sleep(300)
                    rr = session.get('https://www.icloud.com/')

                    soup = BeautifulSoup(rr.text, 'lxml')
                    try:
                        clientBuildNumber = soup.find('html')['data-cw-private-build-number']
                        number = soup.find('html')['data-cw-private-mastering-number']
                    except Exception as e:
                        return

                    def get_cookies2():
                        cookies = {}
                        selenium_cookies = driver.get_cookies()
                        try:
                            for cookie in selenium_cookies:
                                cookies[cookie['name']] = cookie['value']
                        except Exception as e:
                            print("test " + e + " test")
                        return cookies

                    cookies = get_cookies2()

                    headers = {
                        'Accept': '*/*',
                        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
                        'Cache-Control': 'no-cache',
                        'Connection': 'keep-alive',
                        'Content-Type': 'text/plain;charset=UTF-8',
                        'Origin': 'https://www.icloud.com',
                        'Pragma': 'no-cache',
                        'Referer': 'https://www.icloud.com/',
                        'Sec-Fetch-Dest': 'empty',
                        'Sec-Fetch-Mode': 'cors',
                        'Sec-Fetch-Site': 'same-site',
                        'User-Agent': USERAGENT,
                        'sec-ch-ua': SECHUA,
                        'sec-ch-ua-mobile': '?0',
                        'sec-ch-ua-platform': '"Windows"',
                    }

                    params = {
                        'clientBuildNumber': clientBuildNumber,
                        'clientMasteringNumber': number,
                        'clientId': str(theId),
                    }

                    data = 'null'

                    response = session.post('https://setup.icloud.com/setup/ws/1/validate', params=params, cookies=cookies, headers=headers, data=data)

                    data = json.loads(response.text)

                    dsid = data['dsInfo']['dsid']
                    notificationId = data['dsInfo']['notificationId']
                    aDsID = data['dsInfo']['aDsID']
                    primaryEmail = data['dsInfo']['primaryEmail']
                    pNumber = data['webservices']['reminders']['url'].split("//")[1].split("-")[0]
                    time.sleep(300)
                    driver.refresh()
                    time.sleep(300)
                    driver.refresh()
                    time.sleep(300)
                    rr = session.get('https://www.icloud.com/')

                    soup = BeautifulSoup(rr.text, 'lxml')
                    try:
                        clientBuildNumber = soup.find('html')['data-cw-private-build-number']
                        number = soup.find('html')['data-cw-private-mastering-number']
                    except Exception as e:
                        return

                    def get_cookies2():
                        cookies = {}
                        selenium_cookies = driver.get_cookies()
                        try:
                            for cookie in selenium_cookies:
                                cookies[cookie['name']] = cookie['value']
                        except Exception as e:
                            print("test " + e + " test")
                        return cookies

                    cookies = get_cookies2()

                    headers = {
                        'Accept': '*/*',
                        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
                        'Cache-Control': 'no-cache',
                        'Connection': 'keep-alive',
                        'Content-Type': 'text/plain;charset=UTF-8',
                        'Origin': 'https://www.icloud.com',
                        'Pragma': 'no-cache',
                        'Referer': 'https://www.icloud.com/',
                        'Sec-Fetch-Dest': 'empty',
                        'Sec-Fetch-Mode': 'cors',
                        'Sec-Fetch-Site': 'same-site',
                        'User-Agent': USERAGENT,
                        'sec-ch-ua': SECHUA,
                        'sec-ch-ua-mobile': '?0',
                        'sec-ch-ua-platform': '"Windows"',
                    }

                    params = {
                        'clientBuildNumber': clientBuildNumber,
                        'clientMasteringNumber': number,
                        'clientId': str(theId),
                    }

                    data = 'null'

                    response = session.post('https://setup.icloud.com/setup/ws/1/validate', params=params, cookies=cookies, headers=headers, data=data)

                    data = json.loads(response.text)

                    dsid = data['dsInfo']['dsid']
                    notificationId = data['dsInfo']['notificationId']
                    aDsID = data['dsInfo']['aDsID']
                    primaryEmail = data['dsInfo']['primaryEmail']
                    pNumber = data['webservices']['reminders']['url'].split("//")[1].split("-")[0]
                    time.sleep(300)
                    driver.refresh()
                    time.sleep(300)
                    driver.refresh()
                    time.sleep(300)
                    rr = session.get('https://www.icloud.com/')

                    soup = BeautifulSoup(rr.text, 'lxml')
                    try:
                        clientBuildNumber = soup.find('html')['data-cw-private-build-number']
                        number = soup.find('html')['data-cw-private-mastering-number']
                    except Exception as e:
                        return

                    def get_cookies2():
                        cookies = {}
                        selenium_cookies = driver.get_cookies()
                        try:
                            for cookie in selenium_cookies:
                                cookies[cookie['name']] = cookie['value']
                        except Exception as e:
                            print("test " + e + " test")
                        return cookies

                    cookies = get_cookies2()

                    headers = {
                        'Accept': '*/*',
                        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
                        'Cache-Control': 'no-cache',
                        'Connection': 'keep-alive',
                        'Content-Type': 'text/plain;charset=UTF-8',
                        'Origin': 'https://www.icloud.com',
                        'Pragma': 'no-cache',
                        'Referer': 'https://www.icloud.com/',
                        'Sec-Fetch-Dest': 'empty',
                        'Sec-Fetch-Mode': 'cors',
                        'Sec-Fetch-Site': 'same-site',
                        'User-Agent': USERAGENT,
                        'sec-ch-ua': SECHUA,
                        'sec-ch-ua-mobile': '?0',
                        'sec-ch-ua-platform': '"Windows"',
                    }

                    params = {
                        'clientBuildNumber': clientBuildNumber,
                        'clientMasteringNumber': number,
                        'clientId': str(theId),
                    }

                    data = 'null'

                    response = session.post('https://setup.icloud.com/setup/ws/1/validate', params=params, cookies=cookies, headers=headers, data=data)

                    data = json.loads(response.text)

                    dsid = data['dsInfo']['dsid']
                    notificationId = data['dsInfo']['notificationId']
                    aDsID = data['dsInfo']['aDsID']
                    primaryEmail = data['dsInfo']['primaryEmail']
                    pNumber = data['webservices']['reminders']['url'].split("//")[1].split("-")[0]
                    time.sleep(300)
                    driver.refresh()
                    time.sleep(300)
                    driver.refresh()
                    time.sleep(300)
                    rr = session.get('https://www.icloud.com/')

                    soup = BeautifulSoup(rr.text, 'lxml')
                    try:
                        clientBuildNumber = soup.find('html')['data-cw-private-build-number']
                        number = soup.find('html')['data-cw-private-mastering-number']
                    except Exception as e:
                        return

                    def get_cookies2():
                        cookies = {}
                        selenium_cookies = driver.get_cookies()
                        try:
                            for cookie in selenium_cookies:
                                cookies[cookie['name']] = cookie['value']
                        except Exception as e:
                            print("test " + e + " test")
                        return cookies

                    cookies = get_cookies2()

                    headers = {
                        'Accept': '*/*',
                        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
                        'Cache-Control': 'no-cache',
                        'Connection': 'keep-alive',
                        'Content-Type': 'text/plain;charset=UTF-8',
                        'Origin': 'https://www.icloud.com',
                        'Pragma': 'no-cache',
                        'Referer': 'https://www.icloud.com/',
                        'Sec-Fetch-Dest': 'empty',
                        'Sec-Fetch-Mode': 'cors',
                        'Sec-Fetch-Site': 'same-site',
                        'User-Agent': USERAGENT,
                        'sec-ch-ua': SECHUA,
                        'sec-ch-ua-mobile': '?0',
                        'sec-ch-ua-platform': '"Windows"',
                    }

                    params = {
                        'clientBuildNumber': clientBuildNumber,
                        'clientMasteringNumber': number,
                        'clientId': str(theId),
                    }

                    data = 'null'

                    response = session.post('https://setup.icloud.com/setup/ws/1/validate', params=params, cookies=cookies, headers=headers, data=data)

                    data = json.loads(response.text)

                    dsid = data['dsInfo']['dsid']
                    notificationId = data['dsInfo']['notificationId']
                    aDsID = data['dsInfo']['aDsID']
                    primaryEmail = data['dsInfo']['primaryEmail']
                    pNumber = data['webservices']['reminders']['url'].split("//")[1].split("-")[0]
                    self.log.critical(f"[{threadnumber}] [{store}] 1 Hour Completed, restarting tasks..")
                    continue

                try:
                    data = json.loads(response.text)

                    email = data['result']['hme']

                    headers = {
                        'Accept': '*/*',
                        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
                        'Connection': 'keep-alive',
                        'Content-Type': 'text/plain',
                        'Origin': 'https://www.icloud.com',
                        'Referer': 'https://www.icloud.com/',
                        'Sec-Fetch-Dest': 'empty',
                        'Sec-Fetch-Mode': 'cors',
                        'Sec-Fetch-Site': 'same-site',
                        'User-Agent': USERAGENT,
                        'sec-ch-ua': SECHUA,
                        'sec-ch-ua-mobile': '?0',
                        'sec-ch-ua-platform': '"Windows"',
                    }

                    params = {
                        'clientBuildNumber': clientBuildNumber,
                        'clientMasteringNumber': number,
                        'clientId': theId,
                        'dsid': dsid,
                    }

                    label = primaryEmail.split("@")[0] + "_" + str(random.randint(100, 999))

                    data = '{"hme":"' + email + '","label":"' + label + '","note":""}'

                    time.sleep(random.randint(2,3))

                    response = session.post(f'https://{pNumber}-maildomainws.icloud.com/v1/hme/reserve', params=params, cookies=cookies, headers=headers, data=data)

                    if 'success":false' in str(response.text):
                        self.log.error(f"[{threadnumber}] [{store}] Hourly Limit Reached -> Restarting Tasks in 1 hour")
                        time.sleep(300)
                        driver.refresh()
                        time.sleep(300)
                        driver.refresh()
                        time.sleep(300)
                        rr = session.get('https://www.icloud.com/')

                        soup = BeautifulSoup(rr.text, 'lxml')
                        try:
                            clientBuildNumber = soup.find('html')['data-cw-private-build-number']
                            number = soup.find('html')['data-cw-private-mastering-number']
                        except Exception as e:
                            return

                        def get_cookies2():
                            cookies = {}
                            selenium_cookies = driver.get_cookies()
                            try:
                                for cookie in selenium_cookies:
                                    cookies[cookie['name']] = cookie['value']
                            except Exception as e:
                                print("test " + e + " test")
                            return cookies

                        cookies = get_cookies2()

                        headers = {
                            'Accept': '*/*',
                            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
                            'Cache-Control': 'no-cache',
                            'Connection': 'keep-alive',
                            'Content-Type': 'text/plain;charset=UTF-8',
                            'Origin': 'https://www.icloud.com',
                            'Pragma': 'no-cache',
                            'Referer': 'https://www.icloud.com/',
                            'Sec-Fetch-Dest': 'empty',
                            'Sec-Fetch-Mode': 'cors',
                            'Sec-Fetch-Site': 'same-site',
                            'User-Agent': USERAGENT,
                            'sec-ch-ua': SECHUA,
                            'sec-ch-ua-mobile': '?0',
                            'sec-ch-ua-platform': '"Windows"',
                        }

                        params = {
                            'clientBuildNumber': clientBuildNumber,
                            'clientMasteringNumber': number,
                            'clientId': str(theId),
                        }

                        data = 'null'

                        response = session.post('https://setup.icloud.com/setup/ws/1/validate', params=params, cookies=cookies, headers=headers, data=data)

                        data = json.loads(response.text)

                        dsid = data['dsInfo']['dsid']
                        notificationId = data['dsInfo']['notificationId']
                        aDsID = data['dsInfo']['aDsID']
                        primaryEmail = data['dsInfo']['primaryEmail']
                        pNumber = data['webservices']['reminders']['url'].split("//")[1].split("-")[0]
                        time.sleep(300)
                        driver.refresh()
                        time.sleep(300)
                        driver.refresh()
                        time.sleep(300)
                        rr = session.get('https://www.icloud.com/')

                        soup = BeautifulSoup(rr.text, 'lxml')
                        try:
                            clientBuildNumber = soup.find('html')['data-cw-private-build-number']
                            number = soup.find('html')['data-cw-private-mastering-number']
                        except Exception as e:
                            return

                        def get_cookies2():
                            cookies = {}
                            selenium_cookies = driver.get_cookies()
                            try:
                                for cookie in selenium_cookies:
                                    cookies[cookie['name']] = cookie['value']
                            except Exception as e:
                                print("test " + e + " test")
                            return cookies

                        cookies = get_cookies2()

                        headers = {
                            'Accept': '*/*',
                            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
                            'Cache-Control': 'no-cache',
                            'Connection': 'keep-alive',
                            'Content-Type': 'text/plain;charset=UTF-8',
                            'Origin': 'https://www.icloud.com',
                            'Pragma': 'no-cache',
                            'Referer': 'https://www.icloud.com/',
                            'Sec-Fetch-Dest': 'empty',
                            'Sec-Fetch-Mode': 'cors',
                            'Sec-Fetch-Site': 'same-site',
                            'User-Agent': USERAGENT,
                            'sec-ch-ua': SECHUA,
                            'sec-ch-ua-mobile': '?0',
                            'sec-ch-ua-platform': '"Windows"',
                        }

                        params = {
                            'clientBuildNumber': clientBuildNumber,
                            'clientMasteringNumber': number,
                            'clientId': str(theId),
                        }

                        data = 'null'

                        response = session.post('https://setup.icloud.com/setup/ws/1/validate', params=params, cookies=cookies, headers=headers, data=data)

                        data = json.loads(response.text)

                        dsid = data['dsInfo']['dsid']
                        notificationId = data['dsInfo']['notificationId']
                        aDsID = data['dsInfo']['aDsID']
                        primaryEmail = data['dsInfo']['primaryEmail']
                        pNumber = data['webservices']['reminders']['url'].split("//")[1].split("-")[0]
                        time.sleep(300)
                        driver.refresh()
                        time.sleep(300)
                        driver.refresh()
                        time.sleep(300)
                        rr = session.get('https://www.icloud.com/')

                        soup = BeautifulSoup(rr.text, 'lxml')
                        try:
                            clientBuildNumber = soup.find('html')['data-cw-private-build-number']
                            number = soup.find('html')['data-cw-private-mastering-number']
                        except Exception as e:
                            return

                        def get_cookies2():
                            cookies = {}
                            selenium_cookies = driver.get_cookies()
                            try:
                                for cookie in selenium_cookies:
                                    cookies[cookie['name']] = cookie['value']
                            except Exception as e:
                                print("test " + e + " test")
                            return cookies

                        cookies = get_cookies2()

                        headers = {
                            'Accept': '*/*',
                            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
                            'Cache-Control': 'no-cache',
                            'Connection': 'keep-alive',
                            'Content-Type': 'text/plain;charset=UTF-8',
                            'Origin': 'https://www.icloud.com',
                            'Pragma': 'no-cache',
                            'Referer': 'https://www.icloud.com/',
                            'Sec-Fetch-Dest': 'empty',
                            'Sec-Fetch-Mode': 'cors',
                            'Sec-Fetch-Site': 'same-site',
                            'User-Agent': USERAGENT,
                            'sec-ch-ua': SECHUA,
                            'sec-ch-ua-mobile': '?0',
                            'sec-ch-ua-platform': '"Windows"',
                        }

                        params = {
                            'clientBuildNumber': clientBuildNumber,
                            'clientMasteringNumber': number,
                            'clientId': str(theId),
                        }

                        data = 'null'

                        response = session.post('https://setup.icloud.com/setup/ws/1/validate', params=params, cookies=cookies, headers=headers, data=data)

                        data = json.loads(response.text)

                        dsid = data['dsInfo']['dsid']
                        notificationId = data['dsInfo']['notificationId']
                        aDsID = data['dsInfo']['aDsID']
                        primaryEmail = data['dsInfo']['primaryEmail']
                        pNumber = data['webservices']['reminders']['url'].split("//")[1].split("-")[0]
                        time.sleep(300)
                        driver.refresh()
                        time.sleep(300)
                        driver.refresh()
                        time.sleep(300)
                        rr = session.get('https://www.icloud.com/')

                        soup = BeautifulSoup(rr.text, 'lxml')
                        try:
                            clientBuildNumber = soup.find('html')['data-cw-private-build-number']
                            number = soup.find('html')['data-cw-private-mastering-number']
                        except Exception as e:
                            return

                        def get_cookies2():
                            cookies = {}
                            selenium_cookies = driver.get_cookies()
                            try:
                                for cookie in selenium_cookies:
                                    cookies[cookie['name']] = cookie['value']
                            except Exception as e:
                                print("test " + e + " test")
                            return cookies

                        cookies = get_cookies2()

                        headers = {
                            'Accept': '*/*',
                            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
                            'Cache-Control': 'no-cache',
                            'Connection': 'keep-alive',
                            'Content-Type': 'text/plain;charset=UTF-8',
                            'Origin': 'https://www.icloud.com',
                            'Pragma': 'no-cache',
                            'Referer': 'https://www.icloud.com/',
                            'Sec-Fetch-Dest': 'empty',
                            'Sec-Fetch-Mode': 'cors',
                            'Sec-Fetch-Site': 'same-site',
                            'User-Agent': USERAGENT,
                            'sec-ch-ua': SECHUA,
                            'sec-ch-ua-mobile': '?0',
                            'sec-ch-ua-platform': '"Windows"',
                        }

                        params = {
                            'clientBuildNumber': clientBuildNumber,
                            'clientMasteringNumber': number,
                            'clientId': str(theId),
                        }

                        data = 'null'

                        response = session.post('https://setup.icloud.com/setup/ws/1/validate', params=params, cookies=cookies, headers=headers, data=data)

                        data = json.loads(response.text)

                        dsid = data['dsInfo']['dsid']
                        notificationId = data['dsInfo']['notificationId']
                        aDsID = data['dsInfo']['aDsID']
                        primaryEmail = data['dsInfo']['primaryEmail']
                        pNumber = data['webservices']['reminders']['url'].split("//")[1].split("-")[0]
                        self.log.critical(f"[{threadnumber}] [{store}] 1 Hour Completed, restarting tasks..")
                        continue

                    anonymousId = response.json()['result']['hme']['anonymousId']

                    self.log.success(f"[{threadnumber}] [{store}] Successfully Generated iCloud Email -> {email} -> sleeping {str(delay)} seconds")

                    next(self.successfulEntries)

                    cmdTitle = f"iCloud Generator | Successful Generations: {str(self.successfulEntries).replace('count(', '').replace(')', '')}/{str(row_count)} | Failed Generations: {str(self.failedEntries).replace('count(', '').replace(')', '')}"
                    if platform == 'darwin':
                        pass
                    else:
                        ctypes.windll.kernel32.SetConsoleTitleW(cmdTitle)

                    try:
                        proxyToPrintOut = str(session.proxies['https']).replace('https://', '').replace('/', '')
                    except:
                        proxyToPrintOut = 'localhost'

                    rows = [primaryEmail, email, anonymousId, proxyToPrintOut, datetime.datetime.now()]

                    def append_list_as_row(file_name, list_of_elem):
                        with open(file_name, 'a', newline='') as write_obj:
                            csv_writer = csv.writer(write_obj)
                            csv_writer.writerow(list_of_elem)

                    append_list_as_row('Accounts/Generated.csv', rows)

                    send_embed(primaryEmail, email, proxyToPrintOut)
                    time.sleep(int(delay))
                    self.icloudThread += 1
                    continue
                except Exception as e:
                    try:
                        self.log.error(f"[{threadnumber}] [{store}] Error Generating Email #122d7s -> {response.text}")
                    except Exception as e:
                        self.log.error(f"[{threadnumber}] [{store}] Error Generating Email [referenceId: #s27s9] -> {str(e)}")
                    next(self.failedEntries)
                    cmdTitle = f"iCloud Generator | Successful Generations: {str(self.successfulEntries).replace('count(', '').replace(')', '')}/{str(row_count)} | Failed Generations: {str(self.failedEntries).replace('count(', '').replace(')', '')}"
                    if platform == 'darwin':
                        pass
                    else:
                        ctypes.windll.kernel32.SetConsoleTitleW(cmdTitle)
                    time.sleep(int(delay))
                    self.icloudThread += 1
                    continue
            except requests.exceptions.ConnectionError:
                self.log.error(f"[{threadnumber}] [{store}] Error Generating Email -> Proxy Error -> Retrying in {str(retryDelay)} seconds")
                time.sleep(int(delay))
                tryCount += 1
                continue
            except requests.exceptions.Timeout:
                self.log.error(f"[{threadnumber}] [{store}] Error Generating Email -> Proxy Timeout -> Retrying in {str(retryDelay)} seconds")
                time.sleep(int(delay))
                tryCount += 1
                continue
            except Exception as e:
                self.log.error(f"[{threadnumber}] [{store}] Error Generating Email -> {e}")
                next(self.failedEntries)
                cmdTitle = f"iCloud Generator | Successful Generations: {str(self.successfulEntries).replace('count(', '').replace(')', '')}/{str(row_count)} | Failed Generations: {str(self.failedEntries).replace('count(', '').replace(')', '')}"
                if platform == 'darwin':
                    pass
                else:
                    ctypes.windll.kernel32.SetConsoleTitleW(cmdTitle)
                time.sleep(int(delay))
                return
