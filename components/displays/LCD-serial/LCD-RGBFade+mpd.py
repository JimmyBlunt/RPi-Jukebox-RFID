"""
Test python sketch for Adafruit USB+Serial LCD backpack
---> http://www.adafruit.com/category/63_96

Adafruit invests time and resources providing this open source code,
please support Adafruit and open-source hardware by purchasing
products from Adafruit!

Written by Limor Fried/Ladyada  for Adafruit Industries.
BSD license, check license.txt for more information
All text above must be included in any redistribution
"""

import mpd
import serial
import sys
import time
import subprocess
from time import sleep
from datetime import datetime
from math import floor

# 16x2 LCD:
ROWS = 2
COLS = 16


def matrixwritecommand(commandlist):
    commandlist.insert(0, 0xFE)
    # time.sleep(0.1);
    for i in range(0, len(commandlist)):
        ser.write(chr(commandlist[i]))
    # ser.write(bytearray(commandlist))


class TextScroller:
    """Class for scrolling text"""
    text = ''
    position = 0
    textLength = 0

    def __init__(self, initialText, textLength):
        self.text = initialText
        self.textLength = textLength

    def scroll(self):
        doubleText = self.text + '     ' + self.text
        scrolledText = doubleText[self.position:len(doubleText)]
        self.position = self.position + 1

        # We add five extra spaces between each complete text scroll.
        if self.position > len(self.text) + 4:
            self.position = 0

        return scrolledText

    def setNewText(self, newText):
        self.text = newText
        self.position = 0



# Set default serialport to USB
serialport = "/dev/ttyACM0"
# 1. get serial port
if len(sys.argv) != 2:
    print("Use default <serialport> /dev/ttyACM0  ")
    ser = serial.Serial(serialport, 9600, timeout=1)
  # exit(0)

if len(sys.argv) == 2:
    ser = serial.Serial(sys.argv[1], 9600, timeout=1)

lastArtistSong = ''
scroller = TextScroller('', 16)
# turn on display
matrixwritecommand([0x42, 0])
sleep(0.3)
# set size
matrixwritecommand([0xD1, COLS, ROWS])
# set & save brightness -
matrixwritecommand([0x98, 200])
# Set & Save Contrast 180-220 value is what works well.
matrixwritecommand([0x91, 180])
print('Contrast was set to 180')

# Clear display
matrixwritecommand([0x58])  # Clear screen - 0
# Autoscroll OFF
matrixwritecommand([0x52])
##Cursor OFF##
matrixwritecommand([0x4B]) #turn off the underline cursor
matrixwritecommand([0x54]) #turn off the blinking block cursor
'''
print ("Set custom Character 0x4E and send it" )
matrixwritecommand([0x4E, 0, 0, 0xA, 0x15, 0x11, 0x11, 0xA, 0x4, 0])
matrixwritecommand([0xC0, 1])  # load bank 1
print ("print all 8 loaded custom charectres from Buffer")
matrixwritecommand([0x58])  # Clear screen
for i in range(0, 7):
    print (chr(i))
    ser.write(chr(i))
    sleep(1)
print("Print themn single ser.write(chr(0)")
print("char0")
sleep(1)
ser.write(chr(0))
print("char1")
sleep(1)
ser.write(chr(1))
print("char2")
sleep(1)
ser.write(chr(2))
print("char3")
sleep(1)
ser.write(chr(3))
print("char4")
sleep(1)
ser.write(chr(4))
sleep(5)
#ser.write(chr(0))
print ("Set own custom Character 0xc1 on 2 and 3" )
matrixwritecommand([0xC1, 0, 2, 0x2,0x3,0x2,0x2,0xe,0x1e,0xc,0x0])
matrixwritecommand([0xC1, 0, 3, 0x7,0x19,0x1,0x1,0x7,0xf,0x6,0x0])
print ("print all 8 loaded custom charectres from Buffer")
matrixwritecommand([0x58])  # Clear screen
matrixwritecommand([0x47, 1, 1])  # 1
for i in range(0, 7):
    print (chr(i))
    ser.write(chr(i))
    sleep(1)
sleep(4);
print("Print themn single ser.write(chr(0)")
ser.write(chr(2))
print("char3")
sleep(1)
ser.write(chr(3))
sleep(6)
matrixwritecommand([0x58])    # Clear screen - 0
# create horizontal bars in custom chars bank #1
matrixwritecommand([0xC1, 1, 0, 0x10,0x10,0x10,0x10,0x10,0x10,0x10,0x10])
matrixwritecommand([0xC1, 1, 1, 0x18,0x18,0x18,0x18,0x18,0x18,0x18,0x18])
matrixwritecommand([0xC1, 1, 2, 0x1C,0x1C,0x1C,0x1C,0x1C,0x1C,0x1C,0x1C])
matrixwritecommand([0xC1, 1, 3, 0x1E,0x1E,0x1E,0x1E,0x1E,0x1E,0x1E,0x1E])
matrixwritecommand([0xC1, 1, 4, 0xF,0xF,0xF,0xF,0xF,0xF,0xF,0xF])
matrixwritecommand([0xC1, 1, 5, 0x7,0x7,0x7,0x7,0x7,0x7,0x7,0x7])
matrixwritecommand([0xC1, 1, 6, 0x3,0x3,0x3,0x3,0x3,0x3,0x3,0x3])
matrixwritecommand([0xC1, 1, 7, 0x1,0x1,0x1,0x1,0x1,0x1,0x1,0x1])
matrixwritecommand([0xC0, 1])  # load bank 1
ser.write(( chr(0) + chr(1) + chr(2) + chr(3) + chr(4) + chr(5) + chr(6) + chr(7) )[0:16] + '\n' +( chr(0) + chr(1) + chr(2) + chr(3) + chr(4) + chr(5) + chr(6) + chr(7))[0:16])
sleep(3)
for i in range(0, 7):
    print (chr(i))
    ser.write(chr(i))
    sleep(3)
matrixwritecommand([0x58])  # Clear screen
print("Prinr Bannk1 srtareting char0")
sleep(1)
ser.write(chr(0))
print("char1")
sleep(1)
ser.write(chr(1))
print("char2")
sleep(1)
ser.write(chr(2))
print("char3")
sleep(1)
ser.write(chr(3))
print("char4")
sleep(1)
ser.write(chr(4))
print("char5")
sleep(1)
ser.write(chr(5))
print("char6")
sleep(1)
ser.write(chr(6))
sleep(1)
print("char7")
ser.write(chr(7))
sleep(2)
sleep(10)
'''
# create vertical bars in custom chars bank #0
matrixwritecommand([0xC1, 0, 0, 0x0,0x11,0x4,0xe,0x4,0x11,0x0,0x0]) 
matrixwritecommand([0xC1, 0, 1, 0x0,0x4,0x4,0xe,0x1b,0xe,0x4,0x4])
matrixwritecommand([0xC1, 0, 2, 0x2,0x3,0x2,0x2,0xe,0x1e,0xc,0x0])
#matrixwritecommand([0xC1, 0, 3, 0x7,0x19,0x1,0x1,0x7,0xf,0x6,0x0])
matrixwritecommand([0xC1, 0, 3, 0x0,0x4,0xe,0x11,0x11,0x11,0xe,0x4])
matrixwritecommand([0xC1, 0, 4, 0x0,0x0,0x0a,0x15,0x11,0xa,0x4,0x0])
matrixwritecommand([0xC1, 0, 5, 0x0,0x15,0xe,0x1b,0xe,0x15,0x0,0x0])
matrixwritecommand([0xC1, 0, 6, 0x1,0x3,0x5,0x9,0xb,0xb,0x18,0x18])
matrixwritecommand([0xC1, 0, 7, 0x0,0xa,0x1f,0x1f,0x1f,0xe,0x4,0x0])

matrixwritecommand([0xC1, 1, 1, 0x4,0xe,0x11,0x11,0x11,0x11,0xe,0x4]) 



# create vertical bars in custom chars bank #2
matrixwritecommand([0xC1, 2, 0, 0,0,0,0,0,0,0,0x1F])
matrixwritecommand([0xC1, 2, 1, 0,0,0,0,0,0,0x1F,0x1F])
matrixwritecommand([0xC1, 2, 2, 0,0,0,0,0,0x1F,0x1F,0x1F])
matrixwritecommand([0xC1, 2, 3, 0,0,0,0,0x1F,0x1F,0x1F,0x1F])
matrixwritecommand([0xC1, 2, 4, 0,0,0,0x1F,0x1F,0x1F,0x1F,0x1F])
matrixwritecommand([0xC1, 2, 5, 0,0,0x1F,0x1F,0x1F,0x1F,0x1F,0x1F])
matrixwritecommand([0xC1, 2, 6, 0,0x1F,0x1F,0x1F,0x1F,0x1F,0x1F,0x1F])
#matrixwritecommand([0xC1, 2, 7, 0x1F,0x1F,0x1F,0x1F,0x1F,0x1F,0x1F,0x1F])
matrixwritecommand([0xC0, 2]) #  load bank 2
matrixwritecommand([0x58])  # Clear screen
matrixwritecommand([0x47, 1, 1])  # 1
#ser.write(( chr(0) + chr(1) + chr(2) + chr(3) + chr(4) + chr(5) + chr(6) + chr(7) )[0:16] + '\n' +( chr(0) + chr(1) + chr(2) + chr(3) + chr(4) + chr(5) + chr(6) + chr(7))[0:16])
#sleep(5)
#for i in range(0, 7):
#    print ('string(chr(i)):' + str(chr(i)))
#    ser.write(chr(i))
#    sleep(3)
matrixwritecommand([0x58])  # Clear screen

'''
print("Prinr Bannk1 srtareting char0")
sleep(1)
ser.write(chr(0))
print("char1")
sleep(1)
ser.write(chr(1))
print("char2")
sleep(1)
ser.write(chr(2))
print("char3")
sleep(1)
ser.write(chr(3))
print("char4")
sleep(1)
ser.write(chr(4))
print("char5")
sleep(1)
ser.write(chr(5))
print("char6")
sleep(1)
ser.write(chr(6))
sleep(1)
print("char7")
ser.write(chr(7))
sleep(2)
sleep(10)
print ("contrast to 170")
matrixwritecommand([0x91, 170])
sleep(1)
print ("contrast to 180")
matrixwritecommand([0x91, 180])
sleep(4)
print ("contrast to 190")
matrixwritecommand([0x91, 190])
sleep(1)
print ("contrast to 200")
matrixwritecommand([0x91, 200])
sleep(1)
print ("contrast to 210")
matrixwritecommand([0x91, 210])
sleep(1)
print ("contrast to 220")
matrixwritecommand([0x91, 220])
sleep(1)
print ("contrast to 230")
matrixwritecommand([0x91, 230])
sleep(1)
print ("contrast to 240")
matrixwritecommand([0x91, 240])
sleep(1)
print ("contrast to 250")
matrixwritecommand([0x91, 250])
sleep(1)
print ("Reset Contrast back to 150")
matrixwritecommand([0x91, 150])
sleep(4)

# create medium numbers in bank #3
matrixwritecommand([0xC1, 3, 0, 0x1f,0x1f,0x03,0x03,0x03,0x03,0x03,0x03])
matrixwritecommand([0xC1, 3, 1, 0x1f,0x1f,0x18,0x18,0x18,0x18,0x18,0x18])
matrixwritecommand([0xC1, 3, 2, 0x03,0x03,0x03,0x03,0x03,0x03,0x1F,0x1F])
matrixwritecommand([0xC1, 3, 3, 0x18,0x18,0x18,0x18,0x18,0x18,0x1F,0x1F])
matrixwritecommand([0xC1, 3, 4, 0x00,0x00,0x00,0x00,0x00,0x00,0x1F,0x1F])
matrixwritecommand([0xC1, 3, 5, 0x1F,0x1F,0x00,0x00,0x00,0x00,0x00,0x00])
matrixwritecommand([0xC1, 3, 6, 0x1F,0x1F,0x03,0x03,0x03,0x03,0x1F,0x1F])

matrixwritecommand([0xC1, 3, 7, 0x1F,0x1F,0x1F,0x1F,0x1F,0x1F,0x1F,0x1F])
matrixwritecommand([0xC0, 3])
print ("Loaded Bank 3")
sleep(3)

matrixwritecommand([0x58])  # Clear screen
matrixwritecommand([0x47, 1, 1])  # 1
ser.write(( chr(0) + chr(1) + chr(2) + chr(3) + chr(4) + chr(5) + chr(6) + chr(7) )[0:16] + '\n' +( chr(0) + chr(1) + chr(2) + chr(3) + chr(4) + chr(5) + chr(6) + chr(7))[0:16])
sleep(5)
for i in range(0, 7):
    print (chr(i))
    ser.write(chr(i))
    sleep(1)
print("Prinr Bannk3 srtareting char0")
sleep(1)
ser.write(chr(0))
print("char1")
sleep(1)
ser.write(chr(1))
print("char2")
sleep(1)
ser.write(chr(2))
print("char3")
sleep(1)
ser.write(chr(3))
print("char4")
sleep(1)
ser.write(chr(4))
print("char5")
sleep(1)
ser.write(chr(5))
print("char6")
sleep(1)
ser.write(chr(6))
sleep(1)
print("char7")
ser.write(chr(7))
sleep(2)
print("Now on 2 lines1")
ser.write(( chr(0) + chr(0) + chr(5) + chr(6) + chr(3) + chr(5) + chr(5) + chr(6) )[0:16] + '\n' +( chr(2) + chr(3) + chr(1) + chr(4) + chr(3) + chr(6) + chr(4) + chr(2))[0:16])

sleep(3)
matrixwritecommand([0x58])  # Clear screen
matrixwritecommand([0x47, 1, 1])  # 1
ser.write(( chr(1) + chr(5) + chr(1) + chr(6) + chr(1) + chr(6) + chr(1) + chr(0) )[0:16] + '\n' +( chr(4) + chr(6) + chr(1) + chr(6) + chr(4) + chr(2) + chr(3) + chr(2))[0:16])
sleep(3)
print("contrast loop1")
# contrast loop1
for i in range(160,255,4):
    matrixwritecommand([0x50, i])
    ser.write((chr(3) + chr(2) + chr(5) + chr(6)))
    sleep(1.3)
matrixwritecommand([0x91, 190])
matrixwritecommand([0x58])  # Clear screen
matrixwritecommand([0x47, 1, 1])  # 1
# write medium num #0
print ("Create custom caraters with  0x6F 0,1,2,3")
ser.write(( chr(0) + chr(0) + chr(5) + chr(6) + chr(3) + chr(5) + chr(5) + chr(6) + '        ')[0:16] + '\n' +( chr(2) + chr(3) + chr(1) + chr(4) + chr(3) + chr(6) + chr(4) + chr(2))+ '        '[0:16])

sleep(2)
matrixwritecommand([0x58])  # Clear screen
matrixwritecommand([0x47, 1, 1])  # 1
ser.write(( chr(1) + chr(5) + chr(1) + chr(6) + chr(1) + chr(6) + chr(1) + chr(0)  + '        ')[0:16] + '\n' +( chr(4) + chr(6) + chr(1) + chr(6) + chr(4) + chr(2) + chr(3) + chr(2)+ '        ')[0:16])
sleep(2)
print("0x6F, 0, 0, 5")
matrixwritecommand([0x47, 1, 1])  # 1-1
print("0x6F, 0, 0, 5")
matrixwritecommand([0x6F,0, 0, 5])
sleep(4)
matrixwritecommand([0x47, 3, 1])  # 1-3
print("0x6F, 5,6, 1")
matrixwritecommand([0x6F,5, 6, 1])
sleep(4)
matrixwritecommand([0x47,6, 1])  # 1-6
print("0x6F, 5, 1, 6")
matrixwritecommand([0x6F, 5,1, 6])
sleep(4)
matrixwritecommand([0x47, 9, 1])  # 1-9
print("0x6F, 1, 6, 1")
matrixwritecommand([0x6F, 1, 6, 1])
sleep(4)
matrixwritecommand([0x47, 12, 1])  # 1-12
print("0x6F, 0, 7, 7")
matrixwritecommand([0x6F,0, 7, 7])
sleep(4)
matrixwritecommand([0x47, 1, 2])  # 2-1
print("0x6F, 2, 3, 1")
matrixwritecommand([0x6F, 2,3, 1])
sleep(4)
matrixwritecommand([0x47, 4, 2])  # 2-3
print("0x6F,4, 3, 6")
matrixwritecommand([0x6F,4, 3, 6])
sleep(4)
matrixwritecommand([0x47, 8, 2])  # 2-6
print("0x6F, 4, 2, 4")
matrixwritecommand([0x6F, 4, 2, 4])
sleep(4)
matrixwritecommand([0x47, 12, 2])  # 2-9
print("0x6F,6,1, 60")
matrixwritecommand([0x6F, 6, 1, 6])
sleep(4)
matrixwritecommand([0x47, 16, 2])  # 2-12
print("0x6F, 4, 2, 3")
matrixwritecommand([0x6F, 4, 2, 3])
sleep(4)

sleep(1)
print("char0")
sleep(1)
ser.write(chr(0))
print("char1")
sleep(1)
ser.write(chr(1))
print("char2")
sleep(1)
ser.write(chr(2))
print("char3")
sleep(1)
ser.write(chr(3))
print("char4")
sleep(1)
ser.write(chr(4))
print("char5")
sleep(1)
ser.write(chr(5))
print("char6")
sleep(1)
ser.write(chr(6))
sleep(1)
print("char7")
ser.write(chr(7))
sleep(2)
sleep(2)

matrixwritecommand([0x58])  # Clear screen
matrixwritecommand([0x47, 1, 1])  # 1
print("0x6F, 2, 0, 1")
matrixwritecommand([0x6F, 2, 0, 1])
sleep(8)
print("0x6F, 1, 0, 0")
matrixwritecommand([0x47, 4, 1])  # 1
matrixwritecommand([0x6F, 1, 0,0])
sleep(8)
print("0x6F, 1, 0, 1")
matrixwritecommand([0x47, 8, 1])  # 1
matrixwritecommand([0x6F, 1, 0, 1])
sleep(8)
matrixwritecommand([0x47, 12, 1])  # 1
print("0x6F, 2, 0, 2")
matrixwritecommand([0x6F, 2, 0, 2])
sleep(8)
matrixwritecommand([0x47, 1, 2])  # 1
print("0x6F, 3, 0, 2")
matrixwritecommand([0x6F, 3, 0, 2])
sleep(8)
matrixwritecommand([0x47, 4, 2])  # 1
print("0x6F, 4, 0, 2")
matrixwritecommand([0x6F, 4, 0, 2])
sleep(8)
matrixwritecommand([0x47, 8, 2])  # 1
print("0x6F, 4, 0, 3")
matrixwritecommand([0x6F, 4, 0, 3])
sleep(8)
matrixwritecommand([0x47, 12, 2])  # 1
matrixwritecommand([0x58])  # Clear screen
matrixwritecommand([0x47, 1, 1])  # 1
print("0x6F, 5, 0, 4")
matrixwritecommand([0x6F, 5, 0, 4])
sleep(8)
print("0x6F, 6, 0, 4")
matrixwritecommand([0x47, 4, 1])  # 1
matrixwritecommand([0x6F, 6, 0, 4])
sleep(3)
print("0x6F, 6, 0, 5")
matrixwritecommand([0x47, 8, 1])  # 1
matrixwritecommand([0x6F, 6, 0, 5])
sleep(3)
print("0x6F, 6, 0, 1")
matrixwritecommand([0x47, 12, 1])  # 1
matrixwritecommand([0x6F, 6, 0, 1])
sleep(3)
print("0x6F, 2, 0, 6")
matrixwritecommand([0x47, 1, 2])  # 1
matrixwritecommand([0x6F, 2, 0, 6])
matrixwritecommand([0x58])  # Clear screen
matrixwritecommand([0x47, 1, 1])  # 1
print("char0")
sleep(1)
ser.write(chr(0))
print("char1")
sleep(1)
ser.write(chr(1))
print("char2")
sleep(1)
ser.write(chr(2))
print("char3")
sleep(1)
ser.write(chr(3))
print("char4")
sleep(1)
ser.write(chr(4))
print("char5")
sleep(1)
ser.write(chr(5))
print("char6")
sleep(1)
ser.write(chr(6))
sleep(1)
print("char7")
ser.write(chr(7))
sleep(10)
matrixwritecommand([0x58])  # Clear screen
matrixwritecommand([0x47, 1, 1])  # 1
print("0x6F, 4, 0, 2")
matrixwritecommand([0x6F, 4, 0, 2])
print("char0")
sleep(1)
ser.write(chr(0))
print("char1")
sleep(1)
ser.write(chr(1))
print("char2")
sleep(1)
ser.write(chr(2))
print("char3")
sleep(1)
ser.write(chr(3))
print("char4")
sleep(1)
ser.write(chr(4))
print("char5")
sleep(1)
ser.write(chr(5))
print("char6")
sleep(1)
ser.write(chr(6))
sleep(1)
print("char7")
ser.write(chr(7))
sleep(10)
matrixwritecommand([0x58])  # Clear screen
matrixwritecommand([0x47, 1, 1])  # 1
print("0x6F, 6, 0, 3")
matrixwritecommand([0x6F, 6, 0, 3])
print("char0")
sleep(1)
ser.write(chr(0))
print("char1")
sleep(1)
ser.write(chr(1))
print("char2")
sleep(1)
ser.write(chr(2))
print("char3")
sleep(1)
ser.write(chr(3))
print("char4")
sleep(1)
ser.write(chr(4))
print("char5")
sleep(1)
ser.write(chr(5))
print("char6")
sleep(1)
ser.write(chr(6))
sleep(1)
print("char7")
ser.write(chr(7))
sleep(2)
matrixwritecommand([0x58])  # Clear screen
matrixwritecommand([0x47, 1, 1])  # 1
ser.write("255, 0, 0")
matrixwritecommand([0xD0, 255, 0, 0 ])
sleep(1.5)
matrixwritecommand([0x58])  # Clear screen
matrixwritecommand([0x47, 1, 1])  # 1
ser.write("255,120, 0")
matrixwritecommand([0xD0, 255, 120, 0 ])
sleep(1.5)
matrixwritecommand([0x58])  # Clear screen
matrixwritecommand([0x47, 1, 1])  # 1
ser.write("255, 255, 0 ")
matrixwritecommand([0xD0, 255, 255, 0 ])
sleep(1.5)
matrixwritecommand([0x58])  # Clear screen
matrixwritecommand([0x47, 1, 1])  # 1
ser.write("120, 255, 0")
matrixwritecommand([0xD0, 120, 255, 0 ])
sleep(1.5)
matrixwritecommand([0x58])  # Clear screen
matrixwritecommand([0x47, 1, 1])  # 1
ser.write("0, 255, 0")
matrixwritecommand([0xD0,   0, 255, 0 ])
sleep(1.5)
matrixwritecommand([0x58])  # Clear screen
matrixwritecommand([0x47, 1, 1])  # 1
ser.write("0, 255, 120")
matrixwritecommand([0xD0,   0, 255, 120 ])
sleep(1.5)
matrixwritecommand([0x58])  # Clear screen
matrixwritecommand([0x47, 1, 1])  # 1
ser.write("0, 255, 255")
matrixwritecommand([0xD0,   0, 255, 255 ])
sleep(1.5)
matrixwritecommand([0x58])  # Clear screen
matrixwritecommand([0x47, 1, 1])  # 1
ser.write("0, 120, 255")
matrixwritecommand([0xD0,   0, 120, 255 ])
sleep(1.5)
matrixwritecommand([0x58])  # Clear screen
matrixwritecommand([0x47, 1, 1])  # 1
ser.write("0, 0, 255")
matrixwritecommand([0xD0,   0, 0, 255 ])
sleep(1.5)
matrixwritecommand([0x58])  # Clear screen
matrixwritecommand([0x47, 1, 1])  # 1
ser.write("120, 0, 255")
matrixwritecommand([0xD0,  120, 0, 255 ])
sleep(1.5)
matrixwritecommand([0x58])  # Clear screen
matrixwritecommand([0x47, 1, 1])  # 1
ser.write(" 255, 0, 255")
matrixwritecommand([0xD0,  255, 0, 255 ])
sleep(1.5)
matrixwritecommand([0x58])  # Clear screen
matrixwritecommand([0x47, 1, 1])  # 1
ser.write("255, 120, 255")
matrixwritecommand([0xD0,  255, 120, 255 ])
sleep(1.5)
matrixwritecommand([0x58])  # Clear screen
matrixwritecommand([0x47, 1, 1])  # 1
ser.write(" 255, 255, 255")
matrixwritecommand([0xD0,  255, 255, 255 ])
sleep(1.5)
matrixwritecommand([0x58])  # Clear screen
matrixwritecommand([0x47, 1, 1])  # 1
ser.write("255, 255, 120")
matrixwritecommand([0xD0,  255, 255, 120 ])
sleep(1.5)
matrixwritecommand([0x58])  # Clear screen
matrixwritecommand([0x47, 1, 1])  # 1
ser.write(" 255, 120, 120")
matrixwritecommand([0xD0,  255, 120, 120 ])
sleep(1.5)
matrixwritecommand([0x58])  # Clear screen
matrixwritecommand([0x47, 1, 1])  # 1
ser.write("255, 0, 120 ")
matrixwritecommand([0xD0,  255, 0, 120 ])
sleep(1.5)
matrixwritecommand([0x58])  # Clear screen
matrixwritecommand([0x47, 1, 1])  # 1
ser.write("120, 0, 120")
matrixwritecommand([0xD0,  120, 0, 120 ])
sleep(1.5)
matrixwritecommand([0x58])  # Clear screen
matrixwritecommand([0x47, 1, 1])  # 1
ser.write(" 120,120, 0 ")
matrixwritecommand([0xD0,  120,120, 0 ])
sleep(1.5)
matrixwritecommand([0x58])  # Clear screen
matrixwritecommand([0x47, 1, 1])  # 1
ser.write("Done")
matrixwritecommand([0xD0,  255, 0, 0 ])

matrixwritecommand([0x58])  # Clear screen
matrixwritecommand([0x47, 1, 1])  # 1

print ("print all 8 loaded custom charectres from Buffer")
for i in range(0, 7):
    print (chr(i))
    ser.write(chr(i))
    sleep(2)
sleep(10);
time.sleep(1.0)
'''
matrixwritecommand([0x58])  # Clear screen
matrixwritecommand([0x47, 1, 1])  # 1

print("connecting to mpd...")
client = mpd.MPDClient()
client.connect("localhost", 6600)
loop = 1
red = 0
green = 0
blue = 0
t = 0
l = 255
volume = 0
lastvolume = 50
while True:
    # Get current status and playtime
    mpdstatus = client.status()
    #print(repr(mpdstatus))
    # Fetch volume
    try:
        volume = int(mpdstatus["volume"])
    except KeyError:
        mpdstatus ["volume"] = 0
    if  volume != lastvolume:
        print ("Volume changed : " )
        matrixwritecommand([0xC0, 2])  # load bank 2
        if volume in xrange (0, 5):
            matrixwritecommand([0x58])
            matrixwritecommand([0x47, 3, 1])  # 1
            #matrixwritecommand([0x4D])  # move cursor right
            ser.write(('  Volume:  ' + str(mpdstatus["volume"] + '   ' ))[0:16] + '\n' +(chr(0) + '\n' )[0:16])
            sleep(3)
        if volume in xrange (6, 11):
            matrixwritecommand([0x58])
            matrixwritecommand([0x47, 3, 1])  # 1
            ser.write(('  Volume:  ' + str(mpdstatus["volume"] + ' ' ))[0:16] + '\n' + (chr(0) + chr(
                0) + '\n')[0:16])
            sleep(3)
        if volume in xrange(12, 17):
            matrixwritecommand([0x58])
            matrixwritecommand([0x47, 3, 1])  # 1
            ser.write(('  Volume:  ' + str(mpdstatus["volume"] + ' ' ))[0:16] + '\n' + (chr(0) + chr(
                0) + chr(1) +  '\n')[0:16])
            sleep(3)
        if volume in xrange(18, 23):
            matrixwritecommand([0x58])
            matrixwritecommand([0x47, 3, 1])  # 1
            ser.write(('  Volume:  ' + str(mpdstatus["volume"] + ' ' ))[0:16] + '\n' + (chr(0) + chr(
                0) + chr(1) + chr(1) + '\n')[0:16])
            sleep(3)
        if volume in xrange(24, 29):
            matrixwritecommand([0x58])
            matrixwritecommand([0x47, 3, 1])  # 1
            ser.write(('  Volume:  ' + str(mpdstatus["volume"] + ' ' ))[0:16] + '\n' + (chr(0) + chr(
                0) + chr(1) + chr(1) + chr(2) +'\n')[0:16])
            sleep(3)
        if volume in xrange(30, 35):
            matrixwritecommand([0x58])
            matrixwritecommand([0x47, 3, 1])  # 1
            ser.write(('  Volume:  ' + str(mpdstatus["volume"] + ' ' ))[0:16] + '\n' + (chr(0) + chr(
                0) + chr(1) + chr(1) + chr(2) + chr(2)  +'\n')[0:16])
            sleep(3)
        if volume in xrange(36, 41):
            matrixwritecommand([0x58])
            matrixwritecommand([0x47, 3, 1])  # 1
            ser.write(('  Volume:  ' + str(mpdstatus["volume"] + ' ' ))[0:16] + '\n' + (chr(0) + chr(
                0) + chr(1) + chr(1) + chr(2) + chr(2) +  chr(3)  +'\n')[0:16])
            sleep(3.0)
        if volume in xrange(42, 47):
            matrixwritecommand([0x58])
            matrixwritecommand([0x47, 3, 1])  # 1
            ser.write(('  Volume:  ' + str(mpdstatus["volume"] + ' '))[0:16] + '\n' + (chr(0) + chr(
                0) + chr(1) + chr(1) + chr(2) + chr(2) + chr(3) + chr(3)  + '\n')[0:16])
            sleep(2)
        if volume in xrange(48, 53):
            matrixwritecommand([0x58])
            matrixwritecommand([0x47, 3, 1])  # 1
            ser.write(('  Volume:  ' + str(mpdstatus["volume"] + ' '))[0:16] + '\n' + (chr(0) + chr(
                0) + chr(1) + chr(1) + chr(2) + chr(2) + chr(3) + chr(3) + chr(4)  + '\n')[0:16])
            sleep(2)
        if volume in xrange(54, 59):
            matrixwritecommand([0x58])
            matrixwritecommand([0x47, 3, 1])  # 1
            ser.write(('  Volume:  ' + str(mpdstatus["volume"] + ' '))[0:16] + '\n' + (chr(0) + chr(
                0) + chr(1) + chr(1) + chr(2) + chr(2) + chr(3) + chr(3) + chr(4) + chr(4)  + '\n')[0:16])
            sleep(2)
        if volume in xrange(60, 65):
            matrixwritecommand([0x58])
            matrixwritecommand([0x47, 3, 1])  # 1
            ser.write(('  Volume:  ' + str(mpdstatus["volume"] + ' '))[0:16] + '\n' + (chr(0) + chr(
                0) + chr(1) + chr(1) + chr(2) + chr(2) + chr(3) + chr(3) + chr(4) + chr(4) + chr(5) + '\n')[0:16])
            sleep(2)
        if volume in xrange(66, 71):
            matrixwritecommand([0x58])
            matrixwritecommand([0x47, 3, 1])  # 1
            ser.write(('  Volume:  ' + str(mpdstatus["volume"] + ' '))[0:16] + '\n' + (chr(0) + chr(
                0) + chr(1) + chr(1) + chr(2) + chr(2) + chr(3) + chr(3) + chr(4) + chr(4) + chr(5) + chr(5)  + '\n')[0:16])
            sleep(2)
        if volume in xrange(72, 77):
            matrixwritecommand([0x58])
            matrixwritecommand([0x47, 3, 1])  # 1
            ser.write(('  Volume:  ' + str(mpdstatus["volume"] + ' '))[0:16] + '\n' + (chr(0) + chr(
                0) + chr(1) + chr(1) + chr(2) + chr(2) + chr(3) + chr(3) + chr(4) + chr(4) + chr(5) + chr(5) + chr(
                6)  + '\n')[0:16])
            sleep(2)
        if volume in xrange(78, 83):
            matrixwritecommand([0x58])
            matrixwritecommand([0x47, 3, 1])  # 1
            ser.write(('  Volume:  ' + str(mpdstatus["volume"] + ' '))[0:16] + '\n' + (chr(0) + chr(
                0) + chr(1) + chr(1) + chr(2) + chr(2) + chr(3) + chr(3) + chr(4) + chr(4) + chr(5) + chr(5) + chr(
                6) + chr(6) + '\n')[0:16])
            sleep(2)
        if volume in xrange(84, 89):
            matrixwritecommand([0x58])
            matrixwritecommand([0x47, 3, 1])  # 1
            ser.write(('  Volume:  ' + str(mpdstatus["volume"] + ' '))[0:16] + '\n' + (chr(0) + chr(
                0) + chr(1) + chr(1) + chr(2) + chr(2) + chr(3) + chr(3) + chr(4) + chr(4) + chr(5) + chr(5) + chr(
                6) + chr(6) + chr(7) + '\n')[0:16])
            sleep(2)
        if volume in xrange(90, 100):
            matrixwritecommand([0x58])
            matrixwritecommand([0x47, 3, 1])  # 1
            ser.write(('  Volume:  ' + str(mpdstatus["volume"] + ' '))[0:16] + '\n' + (chr(0) + chr(
                0) + chr(1) + chr(1) + chr(2) + chr(2) + chr(3) + chr(3) + chr(4) + chr(4) + chr(5) + chr(5) + chr(
                6) + chr(6) + chr(7) + chr(7) + '\n')[0:16])
            sleep(2)
    lastvolume = volume
    if mpdstatus["state"] == "play":
        song = client.currentsong()
        songName = song["file"]
        #print(repr(song))
        # songName = song["artist"]
        # print ("songName : " + songName )
        # Extract the songName (first line)
        # songName = statusLines[0]
        # Extract play status
        playStatus = "playing"

        elapsed = int(floor(float(mpdstatus["elapsed"])))
        minutes = elapsed // 60
        songtime = "%02d:%02d" % (minutes, elapsed % 60)
        if songName.startswith("http"):  # if it is a http stream!
            time = "%s" % (songtime)
            songName =  "%s-%s" % (song["name"], song["title"])
        else:
            lenght = int(floor(float(song["time"])))
            minutes_lengt = lenght // 60
            # print('Time elapsed (mm:ss) {}'.format(elapsed))
            length_track = "%02d:%02d" % (minutes_lengt, lenght % 60)
            time = "%s/%s" % (songtime, length_track)
            # print ("time:  " + time )
            # print("% %s [%s]" % (song["file"], elapsed))

    else:
        songName = ""
        playStatus = "[stopped]"
        time = "0:00/0:00 (0%)"

    ###lcd.setCursor(0,0)
    # cursor set 1
    ##matrixwritecommand([0x58])    # Clear screen - 0
    matrixwritecommand([0x47,1,1])
    
    # Without scolling of text
    # lcd.message((playStatus + ' ' + songName)[0:16] + '\n' + (time + '     ')[0:16])

    # with scolling text
    artistSong = (playStatus + ' ' + songName)
    if artistSong != lastArtistSong:
        scroller.setNewText(artistSong)
        lastArtistSong = artistSong
        # sleep(2)
    if songName != '':
        ser.write(scroller.scroll()[0:16] + '\n' + (time + '     ')[0:16])
        sleep(0.4)
    else:
        #ser.write((playStatus + '             ')[0:16] + '\n' + (time + '     ')[0:16])
        matrixwritecommand([0xC0, 0])  # load bank 0
        ser.write(" ")
        ser.write(chr(2))
        ser.write(" ")
        ser.write(chr(3))
        ser.write(chr(0))
        ser.write(" Mia's ")
        ser.write(chr(4))
        ser.write(" ")
        ser.write(chr(5))
        ser.write("  ")
        ser.write(chr(6))
        ser.write("  B")
        ser.write(chr(1))
        ser.write(chr(3))
        ser.write(chr(1))
        ser.write("MBoX  ")
        ser.write(chr(7))
     # color loop 
     
    # red+green
    if loop == 1:
        if green < 255:
            matrixwritecommand([0xD0, red, green, blue])
            green = green + 1
        else:
            loop = 2
    # green - red       
    if loop == 2:
        if red > 0:
            matrixwritecommand([0xD0, red, green, blue])
            red = red -1
        else:
            loop = 3
    # green + blue        
    if loop == 3:
        if blue < 255:
            matrixwritecommand([0xD0, red, green, blue])
            blue = blue + 1
        else:
            loop = 4
    # blue - green      
    if loop == 4:
        if green  > 0:
            matrixwritecommand([0xD0,red, green, blue])
            green = green - 1 
        else:
            loop = 5
           
    # blue + red  
    if loop == 5:
        if red < 255:
            matrixwritecommand([0xD0, red, green, blue])
            red = red + 1
        else:
            loop = 6
    # red - blue
    if loop == 6:
        if blue  > 0:
            matrixwritecommand([0xD0,red, green, blue])
            blue = blue - 1 
        else:
            loop = 1


    # Poll the buttons most of the sleep time, to make them responsive the plan is to
    # poll the buttons for 400ms and then update the status on the display
    # If we sleep for 40ms between each poll time and have five buttons that equals to 200 ms
    # Two iterations of this gives us 400 ms.
    # for i in range (0, 10):
    # time.sleep(0.2)

# contrast loop
# for i in range(0, 256):
#    matrixwritecommand([0x50, i]) 
# time.sleep(0.2);
#    matrixwritecommand([0x50, 254])
# ser.write("Turn LCD OFF in 3s")
# time.sleep(3.1);
# turn off display
# ser.write("off");
# matrixwritecommand([0x46])
# time.sleep(3.3);

# turn on display
# ser.write("on");
# matrixwritecommand([0x42, 0])
# time.sleep(3.3);
# ser.write(" LCD is ON ")
'''
# autoscroll onqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq1ww
matrixwritecommand([0x58])
matrixwritecommand([0x51])

# create custom char
matrixwritecommand([0x4E, 0, 0, 0xA, 0x15, 0x11, 0x11, 0xA, 0x4, 0]) 
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            matrixwritecommand([0xC1, 0, 2, 0x2,0x3,0x2,0x2,0xe,0x1e,0xc,0x0])
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            matrixwritecommand([0xC1, 0, 3, 0x7,0x19,0x1,0x1,0x7,0xf,0x6,0x0])
ser.write(" ")
ser.write(chr(0))
ser.write(" ")
ser.write(chr(1))
ser.write(chr(0))
ser.write(" Mia's ")
ser.write(chr(0))
ser.write(" ")
ser.write(chr(0))
ser.write("  ")
ser.write(chr(3))
ser.write(" BooOMBoX  ")
ser.write(chr(0))
time.sleep(0.5)

# color loop
matrixwritecommand([0x99, 255]) 
for r in range(0, 256):
    matrixwritecommand([0xD0, r, 0, 0]) 
    time.sleep(0.05);
for g in range(0, 256):
    matrixwritecommand([0xD0, 255-g, g, 0]) 
    time.sleep(0.05);
for b in range(0, 256):
    matrixwritecommand([0xD0, 0, 255-b, b]) 
    time.sleep(0.05);
for r in range(0, 256):
    matrixwritecommand([0xD0, r, 0, 255-r]) 
    time.sleep(0.05);
for r in range(255, 0):
    matrixwritecommand([0xD0, r, 0, 0]) 
    time.sleep(0.05);

#matrixwritecommand([0x99, 0]) 
#matrixwritecommand([0xD0, 255, 255, 255]) 
ser.write("test brightness loop in 2s");
time.sleep(2.3);
# brightness loop
for i in range(0, 256):
    matrixwritecommand([0x99, i]) 
    time.sleep(0.01);
ser.write("Done");
time.sleep(2.01);
matrixwritecommand([0x99, 255]) 
ser.write("Next");
time.sleep(2.01);
# home
matrixwritecommand([0x48]) 
ser.write("home");
time.sleep(3.5);

#clear
matrixwritecommand([0x58])    # Clear screen - 0
ser.write("clear");
time.sleep(3.5);

matrixwritecommand([0x58])    # Clear screen - 0
matrixwritecommand([0xC0, 1])  # load bank 1
ser.write(chr(0))
ser.write(chr(1))
ser.write(chr(2))
ser.write(chr(3))
ser.write(chr(4))
ser.write(chr(5))
ser.write(chr(6))
ser.write(chr(7))
sleep(10)

matrixwritecommand([0x58])    # Clear screen - 0
# load vertical bars from custom chars bank #2
matrixwritecommand([0xC0, 2])
ser.write(chr(0))
ser.write(chr(1))
ser.write(chr(2))
ser.write(chr(3))
ser.write(chr(4))
ser.write(chr(5))
ser.write(chr(6))
ser.write(chr(7))
sleep(10)

matrixwritecommand([0x58])    # Clear screen - 0
# load vertical bars from custom chars bank #3
matrixwritecommand([0xC0, 3])
ser.write(chr(0))
ser.write(chr(1))
ser.write(chr(2))
ser.write(chr(3))
ser.write(chr(4))
ser.write(chr(5))
ser.write(chr(6))
ser.write(chr(7))
sleep(10)

matrixwritecommand([0x58])    # Clear screen - 0
# create medium numbers in bank #3
matrixwritecommand([0xC1, 3, 0, 0x0,0x1,0x3,0x2,0x2,0xe,0x1e,0xc])
matrixwritecommand([0xC1, 3, 1, 0x7,0x19,0x1,0x1,0x7,0xf,0x6,0x0])
matrixwritecommand([0xC1, 3, 2, 0x6,0x9,0xe,0x8,0x8,0x18,0x18,0x0])
matrixwritecommand([0xC1, 3, 3, 0x2,0x3,0x2,0x2,0xe,0x1e,0xc,0x0])
matrixwritecommand([0xC1, 3, 4, 0x00,0x00,0x00,0x00,0x00,0x00,0x1F,0x1F])
matrixwritecommand([0xC1, 3, 5, 0x1F,0x1F,0x00,0x00,0x00,0x00,0x00,0x00])
matrixwritecommand([0xC1, 3, 6, 0x1F,0x1F,0x03,0x03,0x03,0x03,0x1F,0x1F])
matrixwritecommand([0xC1, 3, 7, 0x1F,0x1F,0x1F,0x1F,0x1F,0x1F,0x1F,0x1F])
ser.write(chr(0))
ser.write(chr(1))
ser.write(chr(2))
ser.write(chr(3))
ser.write(chr(4))
ser.write(chr(5))
ser.write(chr(6))
ser.write(chr(7))
sleep(4)

matrixwritecommand([0x58])
# write medium num #0
matrixwritecommand([0x6F, 0, 0, 0])
matrixwritecommand([0x6F, 2, 0, 1])
matrixwritecommand([0x6F, 4, 0, 2])
matrixwritecommand([0x6F, 6, 0, 3])
sleep(4)





#while True:
# create custom char
matrixwritecommand([0x4E, 0, 0, 0xA, 0x15, 0x11, 0x11, 0xA, 0x4, 0]) 
matrixwritecommand([0xC1, 0, 2, 0x2,0x3,0x2,0x2,0xe,0x1e,0xc,0x0])
matrixwritecommand([0xC1, 0, 3, 0x7,0x19,0x1,0x1,0x7,0xf,0x6,0x0])
ser.write(" ")
ser.write(chr(0))
ser.write(" ")
ser.write(chr(1))
ser.write(chr(0))
ser.write(" Mia's ")
ser.write(chr(0))
ser.write(" ")
ser.write(chr(0))
ser.write("  ")
ser.write(chr(3))
ser.write(" BooOMBoX ")
ser.write(chr(0))
sleep(4.5)

# color loop
  matrixwritecommand([0x99, 255]) 
  for r in range(0, 256):
    matrixwritecommand([0xD0, r, 0, 0]) 
    sleep(0.05);
  for g in range(0, 256):
    matrixwritecommand([0xD0, 255-g, g, 0]) 
    sleep(0.05);
  for b in range(0, 256):
    matrixwritecommand([0xD0, 0, 255-b, b]) 
    sleep(0.05);
  for r in range(0, 256):
    matrixwritecommand([0xD0, r, 0, 255-r]) 
    sleep(0.05);
  for r in range(255, 0):
    matrixwritecommand([0xD0, r, 0, 0]) 
    sleep(0.05);


ser.write("autoscroll on in 2s");
time.sleep(2)
# autoscroll on
matrixwritecommand([0x58])    # Clear screen - 0
matrixwritecommand([0x51])

if (ROWS == 2):
    ser.write("Here's some text");
    time.sleep(2)
    ser.write("Add some more..");
    time.sleep(2)
    ser.write(" which'll scroll");
time.sleep(3)

# autoscroll off
matrixwritecommand([0x58])    # Clear screen - 0
matrixwritecommand([0x52]) 
#ser.write("long long long text that ends @ top left    ");
#time.sleep(4);

# cursor test
matrixwritecommand([0x58])    # Clear screen - 0
matrixwritecommand([0x47,1,1]) 
ser.write('1');
time.sleep(2);
matrixwritecommand([0x47,COLS,1]) 
ser.write('2');
time.sleep(2);
matrixwritecommand([0x47,1,ROWS]) 
ser.write('3');
time.sleep(2);
matrixwritecommand([0x47,COLS,ROWS]) 
ser.write('4');
time.sleep(2);

#underline cursor on
matrixwritecommand([0x4A])
# move cursor left
matrixwritecommand([0x4C])
time.sleep(2);
# cursor off
##matrixwritecommand([0x4B])
matrixwritecommand([0x54])

# block cursor
matrixwritecommand([0x53])
# move cursor right
matrixwritecommand([0x4D])
time.sleep(2);
matrixwritecommand([0x54])
time.sleep(2.5);
ser.write('END');

# baudrate change
matrixwritecommand([0x39, 0x29])
time.sleep(1);
ser.close();
ser = serial.Serial(sys.argv[1], 2400, timeout=1)
matrixwritecommand([0x58])    # Clear screen - 0
ser.write("2400")

matrixwritecommand([0x39, 0xCF])
time.sleep(1);
ser.close();
ser = serial.Serial(sys.argv[1], 4800, timeout=1)
matrixwritecommand([0x58])    # Clear screen - 0
ser.write("4800")

matrixwritecommand([0x39, 0x67])
time.sleep(1);
ser.close();
ser.close();
ser = serial.Serial(sys.argv[1], 9600, timeout=1)
matrixwritecommand([0x58])    # Clear screen - 0
ser.write("9600")

matrixwritecommand([0x39, 0x33])
time.sleep(1);
ser.close();
ser = serial.Serial(sys.argv[1], 19200, timeout=1)
matrixwritecommand([0x58])    # Clear screen - 0
ser.write("19200")

matrixwritecommand([0x39, 0x22])
time.sleep(1);
ser.close();
ser = serial.Serial(sys.argv[1], 28800, timeout=1)
matrixwritecommand([0x58])    # Clear screen - 0
ser.write("28800")

matrixwritecommand([0x39, 0x19])
time.sleep(1);
ser.close();
ser = serial.Serial(sys.argv[1], 38400, timeout=1)
matrixwritecommand([0x58])    # Clear screen - 0
ser.write("38400")

matrixwritecommand([0x39, 0x10])
time.sleep(1);
ser.close();
ser = serial.Serial(sys.argv[1], 57600, timeout=1)
matrixwritecommand([0x58])    # Clear screen - 0
ser.write("57600")

# Revert back to 9600 baud
matrixwritecommand([0x39, 0x67])
time.sleep(1);
ser.close();
ser = serial.Serial(sys.argv[1], 9600, timeout=1)

'''
# Splashscreen change
# matrixwritecommand([0x40, ord('H'),ord('e'),ord('l'),ord('l'),ord('o'),ord(' '),ord('W'),ord('o'),ord('r'),ord('l'),ord('d'),ord('!'),ord(' '),ord(' '),ord(' '),ord(' '),ord('T'),ord('e'),ord('s'),ord('t'),ord('i'),ord('n'),ord('g'),ord(' '),ord('1'),ord('6'),ord('x'),ord('2'),ord(' '),ord('L'),ord('C'),ord('D')])

# matrixwritecommand([0x40, ord(' '),ord(' '),ord('A'),ord('d'),ord('a'),ord('f'),ord('r'),ord('u'),ord('i'),ord('t'),ord('.'),ord('c'),ord('o'),ord('m'),ord(' '),ord(' '),ord('1'),ord('6'),ord('x'),ord('2'),ord(' '),ord('U'),ord('S'),ord('B'),ord('+'),ord('S'),ord('e'),ord('r'),ord(' '),ord('L'),ord('C'),ord('D')])
exit()
