# Bruin Formula Racing Dashboard
 
### How to set up on Raspberry Pi
1. Connect Raspberry Pi and a screen with resolution around 1280x720 pixels to power supply.
2. Configure the Raspberry Pi according to [this manual](https://www.waveshare.com/w/upload/2/29/RS485-CAN-HAT-user-manuakl-en.pdf), test the can0 channel with can-utils
3. Package resource files (if you made any changes to them) with command: `pyrcc5 resources.qrc -o resources.py`
4. Upload non-resource files (excluding gui/resources, gui/main.ui and resources.qrc) to Raspberry Pi
5. Configure the resolution of Raspberry Pi to be 1280x720
6. Cd to main.py's directory, and run command: python main.py. The dashboard should display.
7. You may have to update constant scalers in globalfonts.py since fonts in Raspberry Pi's OS look different.
8. To hide the menu bar, enter in the terminal: `sudo nano /home/[name of your pi]/config/lxsession/LXDE-pi/autostart` and comment out by adding a '#' the line: `@lxpanel --profile LXDE` After hiding the menu bar, press Ctrl+Alt+T to open a terminal
9. To launch on boot, follow [these instructions](https://learn.sparkfun.com/tutorials/how-to-run-a-raspberry-pi-program-on-startup#method-2-autostart)
10. To make updating versions from git easier, move gitpull.sh to the directory one level up. Run `chmod a+rx gitpull.sh` to allow the shell script to make modifications, and then run `~/gitpull.sh` to update from this repo
