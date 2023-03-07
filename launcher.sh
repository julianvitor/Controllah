yes | sudo apt install unattended-upgrades #security updates
yes | sudo timedatectl set-ntp true         #time synchronization
yes | sudo systemctl restart systemd-timesyncd
yes | sudo apt install pip
yes | sudo pip install --upgrade pip setuptools wheel
yes | sudo pip install -r requirements.txt
yes | sudo pip install -r /home/pi/Controllah/requirements.txt