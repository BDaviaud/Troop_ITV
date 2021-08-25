# TroopRasp

Based on [Troop](https://github.com/Qirky/Troop) (v 0.10.3), TroopRasp is an extended tool for Raspberry Pi that enables interaction with sensors in a live coding performance. To use TroopRasp, you need [SuperCollider](https://supercollider.github.io/) and [FoxDot](https://github.com/Qirky/FoxDot) installed on the Raspberry Pi.

In a collaborative live coding performance with Troop, you can add a TroopRasp client installed on a Raspberry Pi (you can add several TroopRasp Client to the session). Through the TroopRasp client, you can link a sensor at a FoxDot player or composed a virtual orchestration that revolves around sensor measurements. 
The orchestration is composed like finite-states automata, where each transition is a event triggered by a sensor and each state is associated to one or more FoxDot player.

## Getting started

### Installing SuperCollider on Raspberry Pi
Update:

	$ sudo apt-get update
	$ sudo apt-get upgrade
	$ sudo apt-get dist-upgrade

Install the required packages:
	
	$ sudo apt-get install git libjack-jackd2-dev libsndfile1-dev libasound2-dev libavahi-client-dev libreadline6-dev libfftw3-dev libxt-dev libudev-dev libcwiid-dev cmake qttools5-dev-tools libqt5webkit5-dev qtpositioning5-dev libqt5sensors5-dev

	
SETUP JACK : Compile and install jackd (no d-bus).

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

Compile and install supercollider:

	$ git clone --recursive git://github.com/supercollider/supercollider

	$ cd supercollider

Use latest version 3.9.x on branch 3.9:


	$ git checkout 3.9 

Then:

	$ git submodule init && git submodule update
	$ mkdir build && cd build
	$ cmake -L -DCMAKE_BUILD_TYPE="Release" -DBUILD_TESTING=OFF -DSUPERNOVA=OFF -DNATIVE=ON -DSC_WII=ON -DSC_IDE=OFF -DSC_QT=OFF -DSC_ED=OFF -DSC_EL=OFF -DSC_VIM=ON ..
	$ make -j 4 #use -j4 flag only for rpi3 (quadcore)
	$ sudo make install
	$ sudo ldconfig

Only needed for SuperCollider < 3.9.3:

	$ mkdir -p ~/.config/SuperCollider 

Set up jack file

	$ echo /usr/bin/jackd -P75 -dalsa -dhw:0 -r44100 -p1024 -n3 > ~/.jackdrc


The -dhw:0 above is the internal soundcard. Change this to -dhw:1 for usb soundcards. Aplay -l will list available devices. Another way to set up and start jack is to open a terminal and type qjackctl. Click “setup” to select soundcard and set periods to 3 (recommended). Then start jack before scide by clicking the play icon.

Start it up. Reboot and then start it up by typing sclang


	$ sudo reboot

To launch the IDE by a terminal :

	$ scide

If you have sound issue on your Raspberry with SuperCollider, change the driver to a Dummy Driver. The music from the live-coding will be executed on the Troop Client, so don't worry !

### Installing FoxDot
[FoxDot installation](https://foxdot.org/installation/) on a Raspberry Pi is the same on Linux:

	$ git clone https://github.com/Qirky/FoxDot.git
	$ cd FoxDot
	$ python setup.py install

Then, open SuperCollider and run (ctrl+entr):

	Quarks.install("FoxDot")
	
If there is no error, go to the SuperCollider menu Language/Recompile Class Library.

Now you can use FoxDot and SuperCollider for a solo session of live-coding.

### Installing TroopRasp
As Troop, you can download the files from this repository as a .zip file and extract the contents to a suitable folder, or, you can clone the repository yourself using:

	$ git clone https://github.com/BDaviaud/TroopRasp.git


To run the client you'll need to make sure you're in correct directory: use the 'cd' command followed by the path to where you've extracted TroopRasp. Then execute:

	$ python3 run-client.py

## Features

The TroopRasp client interface offers two new features compared to the original Troop interface. The first one, called Sensor Interaction, allows to link a GPIO input of the Raspberry Pi to a parameter of a FoxDot player. The second, called Orchestration, offers the possibility to create and play a virtual orchestration, based on the model of a discrete event system. Each of these features is accessible from the menu in the main window via the "Interactive Features" tab.

### Sensor Interaction Example
To Do

### Orchestration Example
The implementation of virtual orchestration results in the creation of finite automata, whose states are reached as the sensors are activated.
To Do

