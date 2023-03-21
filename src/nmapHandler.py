import nmap
from termcolor import colored

class NmapHandler:
    def __init__(self, networkAddress, ports='22', admin=False):
        self.networkAddress = networkAddress
        self.ports = ports
        self.nmap = nmap.PortScanner()
        self.admin = admin

    def scan(self):
        if self.admin:
            try:
                result = self.nmap.scan(hosts=self.networkAddress, ports=self.ports, arguments='-T5 -n -Pn --open --max-retries 0 --max-scan-delay 0 --min-rate 10000 --max-rate 10000 -O')
                hosts = self.nmap.all_hosts()
                return result, hosts
            except Exception as e:
                print("[!!]"+colored(str(e), 'red'))
            
        else:
            try:
                result = self.nmap.scan(hosts=self.networkAddress, ports=self.ports, arguments='-T5 -n -Pn --open --max-retries 0 --max-scan-delay 0 --min-rate 10000 --max-rate 10000')
                hosts = self.nmap.all_hosts()
                return result, hosts
            except Exception as e:
                print("[!!]"+colored(str(e), 'red'))
    