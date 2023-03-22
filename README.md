# DebugHelper
this script supposedly to scan the network and connect trough ssh and dmesg things 


# USAGE ON TERMUX
```sh
curl -o- https://raw.githubusercontent.com/FlyingThaCat/IPscan/main/runs.sh | bash
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