#!/bin/bash
# IP & PORT SCANNER FOR RNDIS INTERFACE 
# @Flyingthacat (github)

RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

check_termux() {
  echo $PREFIX | grep -q "com.termux"
}

if check_termux; then
    printf "${GREEN}Running On Termux ...${NC}\n"
  else
    printf "${RED}Sorry This Script Only Works On Termux ...${NC}\n"
    exit
fi


printf "${GREEN}Update And Upgrading Termux ...${NC}\n"
pkg update -y -q && pkg upgrade -y -q

printf "${GREEN}Checking Nmap ...${NC}\n"

if ! command -v nmap -V &> /dev/null
then 
  printf "${RED}Nmap Not Installed ...${NC}\n"
  printf "${BLUE}Do You Want To Install Nmap ... (y/n)${NC}\n"
  read answerNmap
  if [ "$answerNmap" != "${answerNmap#[Yy]}" ] ;then
    pkg install nmap -y
  else
    exit
  fi
fi

printf "${GREEN}Checking IPCalc ...${NC}\n"

if ! command -v ipcalc -v &> /dev/null
then 
  printf "${RED}Ipcalc Not Installed ...${NC}\n"
  printf "${BLUE}Do You Want To Install Ipcalc ... (y/n)${NC}\n"
  read answerIpcalc
  if [ "$answerIpcalc" != "${answerIpcalc#[Yy]}" ] ;then
    pkg install ipcalc -y
  else
    exit
  fi
fi

if ! ifconfig 2> /dev/null | grep -q "rndis"
then
  printf "${RED}Usb Tethering Interface Not Found !!!!!${NC}\n"
  exit
fi

printf "${GREEN}Checking Phone IP On Rndis ...${NC}\n"
PHONE_IP_RNDIS=$(ifconfig 2> /dev/null | grep -A 1 "rndis" | awk '/inet /{print $2}')
printf "${BLUE}Phone IP : ${PHONE_IP_RNDIS}${NC}\n"

printf "${GREEN}Checking Phone Netmask On Rndis ...${NC}\n"
PHONE_NETMASK_RNDIS=$(ifconfig 2> /dev/null | grep -A 1 "rndis" | awk '/netmask/{print $4}')
printf "${BLUE}Phone Netmask : ${PHONE_NETMASK_RNDIS}${NC}\n"

NETWORK_ADDRESS=$(ipcalc $PHONE_IP_RNDIS | awk '/Network:/ { print $2 }')
printf "${BLUE}Founded Network Address : ${NETWORK_ADDRESS}${NC}\n"

printf "${GREEN}Do Nmap Scan ... ${NC}\n"
counter=0

nmap_scan(){
  nmap -p 22 --open -oG - $NETWORK_ADDRESS | awk '/Up$/{print $2}'
}

# THX CHATGPT
# Use a for loop to iterate 5 times
for i in {1..5}; do
  # Call the nmap_scan function and capture its output
  result="$(nmap_scan)"
  
  # If the result is not empty, print it and break out of the loop
  if [ ! -z "$result" ]; then
    printf "${GREEN}Possible Ip Address is $result ${NC}\n"
    printf "${GREEN}Try This Command 'ssh username@$result' ${NC}\n"
    break
  fi

  # Increment the counter variable
  counter=$((counter+1))
  printf "${RED}Try $counter: Host not found${NC}\n"
done

# If the counter is equal to 5, exit with an error message
if [ $counter -eq 5 ]; then
  printf "${RED}Could not find host after 5 attempts !!!!!${NC}\n"
  exit 1
fi