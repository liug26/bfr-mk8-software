# BFR Mk8 Dashboard
PyQt5-based GUI with and endlessly looping thread reading CAN messages that reflect on the screen

### Required Libraries
To install Python 3.7 on a Ubuntu Linux Machine:
```
sudo apt-get update
sudo apt-get install python3.7
```
Then, install PyQt5 by `pip install PyQt5`

### Code Structure

 
### Deployment on Raspberry Pi
#### Setting up the Raspberry Pi
1. Connect Raspberry Pi and a screen with a resolution of around 1280x720 pixels to the power supply.
2. [Configure the resolution](https://raspberrytips.com/change-resolution-raspberry-pi/) of the Raspberry Pi to be 1280x720
3. Configure the Raspberry Pi according to [this manual](https://www.waveshare.com/w/upload/2/29/RS485-CAN-HAT-user-manuakl-en.pdf)
4. Test if the can0 channel can receive messages with can-utils or by running the Python script in the manual
#### Deploying Code
1. Clone this git repository
2. Package resource files (if you made changes to them) by command: `pyrcc5 resources.qrc -o resources.py`, then you can essentially delete gui/resources, gui/main.ui, and resources.qrc
3. In globalfonts.py, tune SCALE and DIAL_SCALE to make the font size look pleasant. This may be necessary since fonts look slightly different on Raspberry Pi's own OS
4. In terminal, run `python main.py`. The dashboard should display.
#### Post-deployment
1. To hide Raspberry Pi's menu bar, enter in terminal `sudo nano /home/[name of your pi]/config/lxsession/LXDE-pi/autostart`  
   and comment out the line: `@lxpanel --profile LXDE` by adding a '#' at front  
   After the menu bar is hidden, to open a terminal press Ctrl+Alt+T
10. To launch on boot, follow [these instructions](https://learn.sparkfun.com/tutorials/how-to-run-a-raspberry-pi-program-on-startup#method-2-autostart)
11. To make updating versions from git easier, move gitpull.sh to the directory one level up. Run `chmod a+rx gitpull.sh` to allow the shell script to make modifications, and then run `~/gitpull.sh` to update from this repo
