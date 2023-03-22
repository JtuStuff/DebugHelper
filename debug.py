import os
import re
import json
import time
import ctypes
import paramiko
from src.nmapHandler import NmapHandler
from paramiko import SSHClient
from termcolor import colored
from src.interfaces import get_interfaces, get_network_address, get_cidr, interfaces_table

# Variables
KNOWN_INTERFACES = ['rndis0', 'usb0']
IS_ADMIN = False
IS_TERMUX = False

# Clear screen
os.system('clear')

def checkAdmin():
    try:
        return os.getuid() == 0
    except AttributeError:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0

# Check os type
if os.name == 'nt':
    IS_ADMIN = checkAdmin()
    print( colored('[X] Running in Windows is not yet supported', 'green') )
    exit()
else:
    if os.environ.get('PREFIX') != None:
        if re.search('com.termux', os.environ.get('PREFIX')):
            print( colored('[*] Running in Termux', 'green') )
            print( colored('[*] Scan result may not be accurate', 'light_yellow') )
            IS_ADMIN = False
            IS_TERMUX = True
    else:
        IS_ADMIN = checkAdmin()
        print( colored('[*] Running in Linux', 'green') )
        if IS_ADMIN:
            print( colored('[*] Running as root', 'green') )
        else:
            print( colored('[*] Running as normal user', 'green') )
            print( colored('[*] Scan result may not be accurate', 'light_yellow') )


# Check config file
if not os.path.isfile('config.json'):
    print( colored('[*] No config found running one time configuration', 'light_yellow') )
    username = input( colored('[?] Enter your username: ', 'green') )
    password = input( colored('[?] Enter your password: ', 'green') )
    config = {
        'username': username,
        'password': password,
        'hosting': 'http://0x0.local',
        'last_interface': '',
        'delay': 3
    }
    with open('config.json', 'w') as f:
        json.dump(config, f)
    
    print( colored('[*] Please restart the app ...', 'light_yellow') )
    print( colored('[*] "python3 debug.py"', 'light_yellow') )
    input("Press Enter to continue...")
    exit()

# Read config file
with open('config.json', 'r') as f:
    config = json.load(f)

# Get interfaces
if config['last_interface'] == '':
    interfaces = get_interfaces(KNOWN_INTERFACES)
    if interfaces == None:
        print( colored('[X] No interface found', 'red') )
        print( colored('[?] Type interface to be using\n', 'green') )
        if IS_TERMUX:
            pass
        else:
            print( colored( interfaces_table().to_string(index=False), 'cyan'))

        config['last_interface'] = input( colored('[?] Enter interface: ', 'green') )
        with open('config.json', 'w') as f:
            json.dump(config, f)

# Using interface
print( colored('[+] Using interface: ', 'green') + config['last_interface'])

# Get network address and cidr
cidr = get_cidr(config['last_interface'])
network_address = get_network_address(config['last_interface']) + '/' + str(cidr)

print( colored('[+] Network address: ', 'green') + network_address )
print( colored('[+] CIDR: ', 'green') + str(cidr) )

COUNTER = 0

while True:
    nm = NmapHandler(networkAddress=network_address, admin=IS_ADMIN)
    hosts = nm.scan()

    if len(hosts) == 0:
        COUNTER += 1
        print( colored('[+] Try: ', 'green') + str(COUNTER) + colored(' - No hosts found', 'red') )
        time.sleep(config['delay'])
    elif len(hosts) >= 1:
        break

print( colored('[+] Found hosts: ', 'green') + str(len(hosts)) )
if len(hosts) == 0:
    print( colored('[-] No hosts found', 'red') )
    exit()
elif len(hosts) > 1:
    print( colored('[-] More than one host found', 'red') )
    exit()
else:
    pass

# do dmesg
print( colored('[+] Getting dmesg...', 'green') )
client = SSHClient()
client.set_missing_host_key_policy(paramiko.MissingHostKeyPolicy()) #BYPASS MITM
client.connect(hostname=hosts[0] ,username=config['username'], password=config['password'])

# execute command
stdout = client.exec_command('echo '+config['password']+' | sudo -S dmesg | curl -F file=@- '+config['hosting'])

# get output
output = stdout[1].read().decode('utf-8')
print( colored('[+] Output: ', 'green') + output )

# make enter to continue
input( colored('[!] Press enter when the screen goes black with the backlight on for 30+ seconds', 'green') )

stdout = client.exec_command('ioreg -flxw0 | curl -F file=@- '+config['hosting'])
output = stdout[1].read().decode('utf-8')
print( colored('[+] Output: ', 'green') + output )

stdout = client.exec_command('/System/Library/Extensions/AppleGraphicsControl.kext/Contents/MacOS/AGDCDiagnose | curl -F file=@- '+config['hosting'])
output = stdout[1].read().decode('utf-8')
print( colored('[+] Output: ', 'green') + output )


# close connection
client.close()