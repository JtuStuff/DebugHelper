#!/bin/bash
# Auto Installer Python Helper

# COLORS
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

# Clear screen
clear

# Pause Function
pause(){
 read -r -s -n 1 -p "Press any key to continue . . ." </dev/tty
 echo ""
}

printf "${BLUE}This script is auto install all the required package ...${NC}\n"
pause()

# Git clone function
git_clone() {
    git clone https://github.com/JtuStuff/DebugHelper
}

# Do termux things
termux_setup(){
    # Update Termux
    printf "${GREEN}Updating Termux ...${NC}\n"
    apt-get update -y -q > /dev/null

    # Upgrade Termux
    printf "${GREEN}Upgrading Termux ...${NC}\n"
    printf "${BLUE}This May Take A While ...${NC}\n"
    apt-get upgrade -y -q -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" > /dev/null
    
    # Installing packages
    printf "${GREEN}Installing Nmap ...${NC}\n"
    apt-get install nmap -y > /dev/null

    printf "${GREEN}Installing Git ...${NC}\n"
    apt-get install git -y > /dev/null

    printf "${GREEN}Installing Python ...${NC}\n"
    apt-get install python -y > /dev/null

    printf "${GREEN}Installing Python Pip ...${NC}\n"
    apt-get install python-pip -y > /dev/null

    printf "${GREEN}Installing Python Numpy ...${NC}\n"
    apt-get install python-numpy -y > /dev/null

    # Cloning repo
    git_clone()
    
    # Change dir
    cd DebugHelper

    export CFLAGS="-Wno-deprecated-declarations -Wno-unreachable-code" pip install pandas
    

}

if echo $PREFIX | grep -q "com.termux"; then
    printf "${GREEN}Running On Termux ...${NC}\n"
