#!/usr/bin/bash

#->add user (as root)
#sudo adduser tracker

#->add user to sudo group (as root)
#sudo usermod -aG sudo tracker

echo "You must be logged in as the user you will run this bot as, and that user must have SUDO rights"
echo "to successfully use this sctipt to install the AnyFlightTracker bot. This script will pause at "
echo "each step. SUDO is not to be used to run the bot."
echo ""
echo ""Use CTRL-C to break out of the script at any time."

read -p "Press ENTER to begin....."

echo ""
echo "creating symbolic link for python to python3 (sudo access needed)"
sudo ln -s /usr/bin/python3 /usr/bin/python
echo ""
python --version

echo ""
read -p "Verify PYTHON version is => 3.9 then press ENTER for next step"
echo ""
echo " ---------------------------------------------------------------- "
echo ""

echo "installing python/pip pip3 (sudo access needed)"
echo ""
sudo apt update && sudo apt install python3-pip

echo ""
read -p "Press ENTER for next step"
echo ""
echo " ---------------------------------------------------------------- "
echo ""

echo "installing python/pip tracker dependencies"
echo ""

cd  /home/$USER/AnyFlightTracker

echo "installing MySQL database connection components..."

sudo apt install python3-dev default-libmysqlclient-dev build-essential

sudo pip3 install mysql-connector-python

echo "installing user level python/pip modules from requirements.txt"

python3 -m pip install --user -r requirements.txt

echo ""
read -p "Press ENTER for next step"
echo ""
echo " ---------------------------------------------------------------- "
echo ""

echo "installing chromium-browser (sudo access needed)"
sudo apt update && sudo apt install chromium-browser -y
echo ""
echo "check and note chromium version"
chromium --version

echo ""
read -p "Press ENTER for next step"
echo ""
echo " ---------------------------------------------------------------- "
echo ""

echo "installing chromedriver  (sudo access needed)"
sudo apt install chromium-chromedriver
echo ""
chromedriver --version
echo ""
read -p "Press ENTER for next step"
echo ""
echo " ---------------------------------------------------------------- "
echo ""

echo "creating chromium cache dir  (sudo access needed)"
sudo mkdir /home/$USER/AnyFlightTracker/chromium
echo ""
echo "changing ownership of chromium cache dir to $USER:$USER  (sudo access needed)"
sudo chown $USER:$USER /home/$USER/AnyFlightTracker/chromium
echo ""
echo "changing permissions of chromium cache dir (sudo access needed)"
chmod +777 /home/$USER/AnyFlightTracker/chromium
chmod 777 /home/$USER/AnyFlightTracker/chromium
echo ""
echo " ---------------------------------------------------------------- "
echo ""

echo ""
echo "Time to modify some files manually...."
echo ""

read -p "Press ENTER to modify the screenshot.py file. Change the CACHE parameter to reflect /home/$USER/AnyFlightTracker/chromium"
/usr/bin/nano screenshot.py

echo ""
echo " ---------------------------------------------------------------- "
echo ""

echo ""
echo "Time to modify the *.sh files manually - ensure all directories reflect the absolute path to the bot (/home/$USER/AnyFlightTracker/)"
echo ""

read -p "Press ENTER to modify the .sh files now"

/usr/bin/nano kill-chrome.sh
/usr/bin/nano runbot.sh
/usr/bin/nano autorunbot.sh
/usr/bin/nano run_tracker.sh
/usr/bin/nano stopbot.sh
/usr/bin/nano sys_boot.sh
/usr/bin/nano taillog.sh

chmod u+x *.sh

echo ""
echo " ---------------------------------------------------------------- "
echo ""

echo ""
read -p "follow INSTALL.txt for how to configure config.ini - press ENTER to exit the install script. Manually edit config.ini at this point"
echo ""


