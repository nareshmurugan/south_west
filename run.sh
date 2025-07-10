
while true; do 
# clear
sudo pkill -f browser
sudo rm -rf profile_data
sudo pkill -f openvpn
sudo rm -rf brave
unzip brave.zip
sudo chown -R root:root brave/chrome-sandbox
sudo chmod 4755 brave/chrome-sandbox
python3 run.py;
done
