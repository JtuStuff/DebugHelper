# DebugHelper
this script supposedly to scan the network and connect trough ssh and dmesg things 

# Based On [This Tutorial](https://github.com/JtuStuff/DebugHelper/blob/main/tutors.md)
## MAKE SURE TO INSTALL NMAP !!! 
### FROM YOUR OS ex "pkg install nmap" for termux / brew install nmap

# USAGE ON TERMUX
```sh
curl -o- https://raw.githubusercontent.com/JtuStuff/DebugHelper/main/autoinstall.sh | bash
```

# Linux Based System
```sh
git clone https://github.com/JtuStuff/DebugHelper
cd DebugHelper
pip install -r requirements.txt -r requirements_unix.txt

# Setup first configuration
python3 debug.py

# Normal Scan Without Os Scan
python3 debug.py

# Root Scan That HOPEFULLY Pick the right IP From OS Detection
sudo python3 debug.py
```
