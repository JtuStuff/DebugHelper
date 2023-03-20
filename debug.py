import os, nmapHandler, time, json, paramiko, netifaces, re
from termcolor import colored
from paramiko import SSHClient

# Default interfaces
KNOWN_INTERFACES = ['rndis0', 'usb0']



# Check if run in Termux from prefix
prefix = os.environ.get('PREFIX')
if re.search('com.termux', prefix):
    print( colored('[+] Running in Termux', 'green') )
    exit()

# If user not ever run this script before make a config file
if not os.path.isfile('config.json'):
    username = input( colored('[+] Enter your username: ', 'green') )
    password = input( colored('[+] Enter your password: ', 'green') )
    config = {
        'username': username,
        'password': password,
        'hosting': 'http://0x0.local',
        'last_interface': '',
        'delay': 3
    }
    with open('config.json', 'w') as f:
        json.dump(config, f)

    # restart script
    os.system('python3 debug.py')
    exit()

# read config file
print( colored('[+] config file found', 'green') )
with open('config.json', 'r') as f:
    config = json.load(f)

# get interfaces
interfaces = netifaces.interfaces()

# if interface is contain in KNOWN_INTERFACES
interfaces = [i for i in interfaces if i in KNOWN_INTERFACES]
config['last_interface'] = interfaces[0]

# get ip address and netmask of interface
ip = netifaces.ifaddresses(config['last_interface'])[netifaces.AF_INET][0]['addr']
netmask = netifaces.ifaddresses(config['last_interface'])[netifaces.AF_INET][0]['netmask']

# make function that calculate network address and cidr
def get_network_address(ip, netmask):
    ip = ip.split('.')
    netmask = netmask.split('.')
    network_address = []
    for i in range(len(ip)):
        network_address.append( str( int(ip[i]) & int(netmask[i]) ) )
    return '.'.join(network_address)

def get_cidr(netmask):
    netmask = netmask.split('.')
    cidr = 0
    for i in netmask:
        cidr += bin(int(i)).count('1')
    return cidr

# get network address and cidr
network_address = get_network_address(ip, netmask)
cidr = get_cidr(netmask)

print( colored('[+] Network address: ', 'green') + network_address+'/'+str(cidr) )

# do nmap scan
print( colored('[+] Scanning...', 'green') )

HOSTS=[]
COUNTER = 0

while True:
    nm = nmapHandler.PortScanner()
    nm.scan(hosts=network_address+'/'+str(cidr), ports='22', arguments='-T5 -n -Pn --open --max-retries 0 --max-scan-delay 0 --min-rate 10000 --max-rate 10000')
    hosts = nm.all_hosts()

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
stdout = client.exec_command('echo "HELLO WORLD" | curl -F file=@- 0x0.local')

# get output
output = stdout[1].read().decode('utf-8')
print( colored('[+] Output: ', 'green') + output )

# make enter to continue
input( colored('[!] Press enter when the screen goes black with the backlight on for 30+ seconds', 'green') )

stdout = client.exec_command('ioreg -flxw0 | curl -F file=@- 0x0.local')
output = stdout[1].read().decode('utf-8')
print( colored('[+] Output: ', 'green') + output )

stdout = client.exec_command('/System/Library/Extensions/AppleGraphicsControl.kext/Contents/MacOS/AGDCDiagnose | curl -F file=@- 0x0.local')
output = stdout[1].read().decode('utf-8')
print( colored('[+] Output: ', 'green') + output )


# close connection
client.close()