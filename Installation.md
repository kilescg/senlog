# Raspberry Pi Setup Guide for Senlog

## 1. Install Raspbian OS Lite 
Ensure `ssh` is enabled and set up a secure password for convenience. 
## 2. Update RPI 
```bash
sudo apt update
sudo apt upgrade
```

## 3. Install Python and it's dependency
```bash
sudo apt install python3 python3-pip python3-venv git
```

## 4. Create Virtual Environment 
A virtual environment in Python is a self-contained directory that encapsulates a specific Python interpreter and its installed modules
```bash
python3 -m venv incoming_env
```

## 5. Add this command to ~/.bashrc
We do this for auto activate virtual environment every time we open a new terminal.
```bash
sudo nano ~/.bashrc

# put this in the last line of .bashrc
source incoming_env/bin/activate
# then ctrl + s to save
# ctrl + x to exit
```

## Refresh our terminal
```bash
source ~/.bashrc
```

## 6. Clone our repository to RPI
```bash
git clone https://github.com/kilescg/senlog.git

cd senlog
pip3 install -r requirements.txt

# Use this command to start the program
python3 main.py 
```

## Enjoy!
