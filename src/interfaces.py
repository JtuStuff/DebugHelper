import netifaces
import pandas as pd
import json

def get_interfaces(interfaces_list):
    interfaces = netifaces.interfaces()
    interfaces = [i for i in interfaces if i in interfaces_list]
    if interfaces == []:
        return None
    else:
        return interfaces[0]

def get_netmask_ip(last_interface):
    ip = netifaces.ifaddresses(last_interface)[netifaces.AF_INET][0]['addr']
    netmask = netifaces.ifaddresses(last_interface)[netifaces.AF_INET][0]['netmask']
    return ip, netmask

def get_network_address(last_interface):
    ip, netmask = get_netmask_ip(last_interface)
    ip = ip.split('.')
    netmask = netmask.split('.')
    network_address = []
    for i in range(len(ip)):
        network_address.append( str( int(ip[i]) & int(netmask[i]) ) )
    return '.'.join(network_address)

def get_cidr(last_interface):
    ip, netmask = get_netmask_ip(last_interface)
    netmask = netmask.split('.')
    cidr = 0
    for i in netmask:
        cidr += bin(int(i)).count('1')
    return cidr

def interfaces_table():
    interfaces = netifaces.interfaces()
    if interfaces == []:
        return None
    else:
        ip = []
        netmask = []
        interfaces_list = []
        for i in interfaces:
            try:
                interface = netifaces.ifaddresses(i)[netifaces.AF_INET][0]
                if interface['addr'] and interface['netmask']:
                    ip.append(interface['addr'])
                    netmask.append(interface['netmask'])
                    interfaces_list.append(i)
            except KeyError:
                interfaces.remove(i)
        df = pd.DataFrame({'Interface': interfaces_list, 'IP': ip, 'Netmask': netmask})
        return df
