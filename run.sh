
# while true; do 
# # clear
# rm -r __pycache__
# sudo pkill -f browser
# sudo rm -rf profile_data
# sudo pkill -f openvpn
# sudo rm -rf brave
# unzip brave.zip
# sudo chown -R root:root brave/chrome-sandbox
# sudo chmod 4755 brave/chrome-sandbox
# python3 run.py;
# done

while true; do 
# clear
rm -r __pycache__
sudo pkill -f chrome
sudo rm -rf profile_data
sudo pkill -f openvpn
sudo rm -rf .ownbrowser
unzip .ownbrowser.zip
sudo chown -R root:root .ownbrowser/browser/orbita-browser-118/chrome-sandbox
sudo chmod 4755 .ownbrowser/browser/orbita-browser-118/chrome-sandbox
python3 run.py;
done
