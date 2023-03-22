# DebugHelper
This script supposedly help you to find the ip and do the debug for you 
The script based on [This Tutorial](https://github.com/JtuStuff/DebugHelper/blob/main/tutors.md)

## Requirements
- Python
- Pip
- Nmap that installed to the system (**Mandatory**)
- - Do (**nmap -v**) to check it

## Library that use
- netifaces
- python-nmap
- paramiko
- termcolor
- pandas (**ONLY WORKS ON UNIX**)

## Warning
The scripts maybe a little bit buggy and please make an issue that will really help me
Update maybe not that fast since im really busy

- **Do first setup !!!**
- **Termux user maybe feel a bug that seems painfull to fix -_ because of the pip library** 
- Sudo method : using nmap os & port detection but only match "Apple" so it maybe get random device
- Non sudo method : using nmap port detection and hopefully find the only one device that has it
- Disconnect any wifi & other connection if you using a usb tethering i'm already being dumb

# USAGE
## Termux
1. Run this code
```sh
curl -o- https://raw.githubusercontent.com/JtuStuff/DebugHelper/main/autoinstall.sh | bash
```
2. Cd to DebugHelper
```sh
cd DebugHelper
```
3. Run the first setup 
```sh 
python3 debug.py
```
4. Run again
```
python3 debug.py
```

## Linux Based System
1. Clone the repository
```sh
git clone https://github.com/JtuStuff/DebugHelper
```
2. Cd to DebugHelper
```sh
cd DebugHelper
```
3. Install the pip requirements
```sh
pip install -r requirements.txt -r requirements_unix.txt
```
4. Run the first setup 
```sh 
python3 debug.py
```
5. -  Normal Scan Without OS Detection
	```sh
	python3 debug.py
	```
	- Root Scan with OS Detection
	```sh
	python3 debug.py
	```
### Helping or Collaboration to fixing the bug will be really appreciated :)
