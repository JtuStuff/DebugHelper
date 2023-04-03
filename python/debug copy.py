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