import time, paramiko, netifaces, re
from termcolor import colored
from paramiko import SSHClient


HOSTS=[]
COUNTER = 0

while True:
    nm = nmap.PortScanner()
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