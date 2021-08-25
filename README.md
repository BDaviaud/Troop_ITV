# TroopRasp
***

Based on [Troop](https://github.com/Qirky/Troop) (v 0.10.3), TroopRasp is an extended tool for Raspberry Pi that enables interaction with sensors in a live coding performance. 

- Utilise FoxDot et SuperCollider.

## Getting started

### Installing SuperCollider on Raspberry Pi
Do updates :
‘’’
	$ sudo apt-get update
	$ sudo apt-get upgrade
	$ sudo apt-get dist-upgrade
‘’’
Install the required packages:
‘’’
	$ sudo apt-get install git libjack-jackd2-dev libsndfile1-dev libasound2-dev libavahi-client-dev libreadline6-dev libfftw3-dev libxt-dev libudev-dev libcwiid-dev cmake qttools5-dev-tools libqt5webkit5-dev qtpositioning5-dev libqt5sensors5-dev
‘’’
	
SETUP JACK
Compile and install jackd (no d-bus)
‘’’
	$ git clone git://github.com/jackaudio/jack2 --depth 1
	$ cd jack2
	$ ./waf configure --alsa --libdir=/usr/lib/arm-linux-gnueabihf/
	$ ./waf build
	$ sudo ./waf install
	$ sudo ldconfig
	$ cd ..
	$ rm -rf jack2
	$ echo "@audio - memlock 256000" | sudo tee --append /etc/security/limits.conf
	$ echo "@audio - rtprio 75" | sudo tee --append /etc/security/limits.conf
‘’’

Compile and install supercollider
‘’’
	$ git clone --recursive git://github.com/supercollider/supercollider

	$ cd supercollider
‘’’

Use latest version 3.9.x on branch 3.9
‘’’
	$ git checkout 3.9 
‘’’
‘’’
	$ git submodule init && git submodule update
	$ mkdir build && cd build
	$ cmake -L -DCMAKE_BUILD_TYPE="Release" -DBUILD_TESTING=OFF -DSUPERNOVA=OFF -DNATIVE=ON -DSC_WII=ON -DSC_IDE=OFF -DSC_QT=OFF -DSC_ED=OFF -DSC_EL=OFF -DSC_VIM=ON ..
	$ make -j 4 #use -j4 flag only for rpi3 (quadcore)
	$ sudo make install
	$ sudo ldconfig
‘’’
	# mkdir -p ~/.config/SuperCollider # Only needed for sc < 3.9.3

Set up jack file
‘’’
	$ echo /usr/bin/jackd -P75 -dalsa -dhw:0 -r44100 -p1024 -n3 > ~/.jackdrc
‘’’

The -dhw:0 above is the internal soundcard. Change this to -dhw:1 for usb soundcards. Aplay -l will list available devices. Another way to set up and start jack is to open a terminal and type qjackctl. click “setup” to select soundcard and set periods to 3 (recommended). Then start jack before scide by clicking the play icon.

Start it up. Reboot and then start it up by typing sclang
‘’’
$ sudo reboot
‘’’

Démarrage de supercollider
#scsynth -u 4555 &

Lancer l'ide de SC
scide

### Installing FoxDot

### Installing TroopRasp

### Start a session

## Features
The TroopRasp client interface offers two new features compared to the original Troop interface. The first one, called Sensor Interaction, allows to link a GPIO input of the Raspberry Pi to a parameter of a FoxDot player. The second, called Orchestration, offers the possibility to create and play a virtual orchestration, based on the model of a discrete event system. Each of these features is accessible from the menu in the main window via the "Interactive Features" tab.

### Sensor Interaction
#### Example

### Orchestration
L’implémentation d’orchestration virtuelle se traduit par la création d’automates finis, dont les états sont atteints au fil des activations des capteurs.

#### Example
