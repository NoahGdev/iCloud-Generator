# iCloud HideMyEmail Generator

![iCloud Generator](https://cdn.mos.cms.futurecdn.net/Cdpw6TMsvTS3tPWmYuVXz6.png)

## Introduction

This Python script automates the generation process of iCloud emails. HideMyEmail is a feature of iCloud that allows users to create temporary email addresses for online use, which helps protect their privacy and avoid spam emails. However, generating multiple HideMyEmail addresses manually can be a time-consuming and tedious process. This script simplifies the process by generating multiple HideMyEmail addresses in one go.

## Requirements

You can install these packages using the following command:
```bash
pip install -r requirements.txt
```

## Usage

To use the script, simply run the `main.py` file using the following command:
```bash
python main.py
```

This will generate a config.json that you will be required to fill out (if you want to recieve embeds of the emails you generate to discord)

This tool will use a browser to login then save the cookies and use the in python requests to make it much more efficient. The browser is kept alive minimised to keep the session alive.

## Issues

If you find a bug or have a feature request, please create an issue on GitHub.

## To Do

- Add exporter (this allows user to login and extract all emails to a CSV file
- Add deleter

## Disclaimer

Please note that this script is intended for educational purposes only. The use of this script for any illegal activity or for any purpose other than its intended use is strictly prohibited. The author of this script is not responsible for any misuse of the script.
