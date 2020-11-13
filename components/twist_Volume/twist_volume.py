from __future__ import print_function
import qwiic_twist
import time
import sys
import mpd
import serial
import subprocess
from math import floor
from subprocess import call

global muted
global volume
global orig_volume

def runExample():

	def toggle_mute():
		global muted 
		global orig_volume 
		global volume
		if muted == False:
			orig_volume=volume
			client.volume(-volume)
			muted=True
		elif muted:
			client.volume(orig_volume)
			muted = False

	mute=0
        global muted
        global orig_volume
        global volume
        muted = False
        reboot=False
        shutdown=False

	client = mpd.MPDClient()
	client.connect("localhost", 6600)

	myTwist = qwiic_twist.QwiicTwist()
	#print ( dir(myTwist) )
	#print ( dir(client))
	if myTwist.connected == False:
		print("The Qwiic twist device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return
	myTwist.begin()
	myTwist.set_color(112, 70, 0) #Set Red and Blue LED brightnesses to half of max.

	myTwist.connect_red = 5  # Red LED will go down 10 in brightness with each encoder tick
	myTwist.connect_green = -5 #Blue LED will go up 10 in brightness with each encoder tick
	myTwist.connect_blue = 2 #Blue LED will go up 10 in brightness with each encoder tick

	while True:
		mpdstatus = client.status()
		# Fetch volume
		volume = int(mpdstatus["volume"])
		if myTwist.moved:
			diff  = myTwist.get_diff()
			if diff  >  1000 :
				diff = (-65536 + diff)
				#print("Diff :" + str(diff))
			client.volume(2*diff)
			myTwist.clear_interrupts()
			myTwist.get_diff(clear_value=True)

		if myTwist.clicked:
			toggle_mute()
			myTwist.clear_interrupts()
		if myTwist.pressed:
			start_time = time.time()
			while myTwist.pressed:
				buttonTime = time.time() - start_time
				#print("Button pressed : " + str(buttonTime) + " sec" )
				if .01 <= buttonTime < 2:        # short push mute
					mute=1
				elif 3 <= buttonTime < 5:
					print('long Press! REBOOT!')    #longer push reboot
					reboot=True
				elif buttonTime >= 5:
					print('Looong Press!   Shutdown') # really long push shutdwon
					reboot=False
					#shutdown=True
		 	myTwist.clear_interrupts()
		if mute == 1:
			toggle_mute()
			mute = 0
		if shutdown:
			call(["sudo", "shutdown","-h", "now"])
		if reboot:
			call(["sudo", "reboot"])
		#time.sleep(0.5)

if __name__ == '__main__':
	try:
		runExample()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example 3")
		sys.exit(0)


