#!/bin/bash
# Auto Debug Collector
# @Flyingthacat (github)

# COLORS
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

# EMPTY VARIABLES
PHONE_IP=""
PHONE_NETMASK=""
NETWORK_ADDRESS=""
INTERFACE=""
USERNAME=""
COUNTER=0

# Clear Screen
clear

# CHECK IF RUNNING ON TERMUX
if echo $PREFIX | grep -q "com.termux"; then
    printf "${GREEN}Running On Termux ...${NC}\n"
else
    printf "${RED}Sorry This Script Only Works On Termux ...${NC}\n"
    exit
fi

# Update Termux
printf "${GREEN}Updating Termux ...${NC}\n"
apt-get update -y -q > /dev/null

# Upgrade Termux
printf "${GREEN}Upgrading Termux ...${NC}\n"
printf "${BLUE}This May Take A While ...${NC}\n"
apt-get upgrade -y -q -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" > /dev/null

# Function To Check If Package Is Installed
check_package(){
  if ! command -v $1 &> /dev/null
  then 
    printf "${RED}$1 Not Installed ...${NC}\n"
    read -r -p "$(printf "${BLUE}Do You Want To Install $1 ... (y/n)\n${NC}")" answer </dev/tty
    if [ "$answer" != "${answer#[Yy]}" ] ;then
      apt-get install $1 -y > /dev/null
    else
      exit
    fi
  fi
}

# Check If Nmap Is Installed
printf "${GREEN}Checking Nmap ...${NC}\n"
check_package nmap

# Check If Ipcalc Is Installed
printf "${GREEN}Checking IPCalc ...${NC}\n"
check_package ipcalc

# Ask user the username
read -r -p "$(printf "${BLUE}Enter Your Username ... OR leave it empty to default\n${NC}")" USERNAME </dev/tty

# Make Function To Check Interface
check_interface(){
  if ! ifconfig 2> /dev/null | grep -q "$1"
  then
    printf "${RED}$1 Interface Not Found !!!!!${NC}\n"

    # return failed
    return 1
  fi
}

# Make Function To Get Ip Address From Interface
get_ip(){
  # ifconfig 2> /dev/null | grep -A 1 "$1" | awk '/inet /{print $2}'
  ip a | grep -A 2 "$1" | awk '/inet /{print $2}' | cut -d '/' -f 1
}

# Make Function To Get Netmask From Interface
get_netmask(){
  # ifconfig 2> /dev/null | grep -A 1 "$1" | awk '/netmask/{print $4}'
  ip a | grep -A 2 "$1" | awk '/inet /{print $2}' | cut -d '/' -f 2
}

# Make function to set interface
set_interface(){
  # if interface empty exit
  if [ -z "$INTERFACE" ]
  then
    printf "${RED}Interface Variable Is Empty !!!!!${NC}\n"
    exit
  fi

  # Get Phone Ip Address
  printf "${GREEN}Checking Phone IP On $INTERFACE ...${NC}\n"
  PHONE_IP=$(get_ip $INTERFACE)
  printf "${BLUE}Phone IP : ${PHONE_IP}${NC}\n"

  # Get Phone Netmask
  printf "${GREEN}Checking Phone Netmask On $INTERFACE ...${NC}\n"
  PHONE_NETMASK=$(get_netmask $INTERFACE)
  printf "${BLUE}Phone Netmask : ${PHONE_NETMASK}${NC}\n"

  # Get Network Address
  printf "${GREEN}Checking Network Address ...${NC}\n"
  NETWORK_ADDRESS=$(ipcalc $PHONE_IP $PHONE_NETMASK | awk '/Network:/ { print $2 }')

  # if network address empty exit
  if [ -z "$NETWORK_ADDRESS" ]
  then
    printf "${RED}Network Address Variable Is Empty !!!!!${NC}\n"
    exit
  fi
  printf "${BLUE}Network Address : ${NETWORK_ADDRESS}${NC}\n"
}

# Make Function To Do Nmap Scan
nmap_scan(){
  # Do Nmap Scan
  printf "${GREEN}Do Nmap Scan ... ${NC}\n"



  # THX CHATGPT
  # Use a for loop to iterate 5 times
  for i in {1..5}; do
    # Call the nmap_scan function and capture its output
    result="$(nmap -T5 -n -Pn -p 22 --open -oG - $NETWORK_ADDRESS | awk '/Up$/{print $2}')"

    # If the result is not empty, print it and break out of the loop
    if [ ! -z "$result" ]; then
      # if result more than 1 ip address
      if echo $result | grep -q " "; then
        printf "${RED}More Than 1 Ip Address Found !!!!!${NC}\n"
        printf "${RED}Something Must Be Wrong${NC}\n"
        exit
      fi
      printf "${GREEN}Possible Ip Address is $result ${NC}\n"
      # if username empty
      if [ -z "$USERNAME" ]
      then
        printf "${BLUE}Try This Command 'ssh username@$result' ${NC}\n"
        break
      fi
      printf "${BLUE}Try This Command 'ssh $USERNAME@$result' ${NC}\n"
      break
    fi

    # Increment the counter variable
    COUNTER=$((COUNTER+1))
    printf "${RED}Try $COUNTER: Host not found${NC}\n"
  done

  # If the counter is equal to 5, exit with an error message
  if [ $COUNTER -eq 5 ]; then
    printf "${RED}Could not find host after 5 attempts !!!!!${NC}\n"
    exit 1
  fi
}

# Check If Rndis Interface Is Found
printf "${GREEN}Checking Rndis Interface ...${NC}\n"
if check_interface rndis
then
  INTERFACE="rndis"
  set_interface
  nmap_scan
  exit
fi

# Check If Usb0 Interface Is Found
printf "${GREEN}Checking Usb0 Interface ...${NC}\n"
if check_interface usb0
then
  INTERFACE="usb0"
  set_interface
  nmap_scan
  exit
fi

# if not match rndis or usb0 do something
if ! ifconfig 2> /dev/null | grep -q "rndis\|usb0"
then
  printf "${RED}No Interface Found !!!!!${NC}\n"
  printf "${RED}It Seems Your Interface Is Not Rndis Or Usb0 ... Trying The Manual Method${NC}\n"
  
  # printf debug from ifconfig
  # ifconfig 2> /dev/null

  # Use ip a
  ip a 2> /dev/null

  read -r -p "$(printf "${BLUE}Enter Your Interface Name For Usb Tethering : \n${NC}")" interface </dev/tty

  # Check If Interface Is Found
  printf "${GREEN}Checking Interface ...${NC}\n"
  # if ! ifconfig 2> /dev/null | grep -q "$interface"
  if ! ip a 2> /dev/null | grep -q "$interface"
  then
    printf "${RED}$interface Interface Not Found !!, You must be Entering A Wrong Interface Name${NC}\n"
    exit
  fi  

  # set interface to variable
  INTERFACE=$interface
  set_interface
  nmap_scan
  exit
fi
