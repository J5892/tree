#!/usr/bin/python

# Simple strand test for Adafruit Dot Star RGB LED strip.
# This is a basic diagnostic tool, NOT a graphics demo...helps confirm
# correct wiring and tests each pixel's ability to display red, green
# and blue and to forward data down the line.  By limiting the number
# and color of LEDs, it's reasonably safe to power a couple meters off
# USB.  DON'T try that with other code!

import time
from dotstar import Adafruit_DotStar

px = 305
numpixels = 305 # Number of LEDs in strip
begin = 0

# Here's how to control the strip from any two GPIO pins:
datapin   = 23
clockpin  = 24
strip     = Adafruit_DotStar(numpixels, 12000000)

# Alternate ways of declaring strip:
# strip   = Adafruit_DotStar(numpixels)           # Use SPI (pins 10=MOSI, 11=SCLK)
# strip   = Adafruit_DotStar(numpixels, 32000000) # SPI @ ~32 MHz
# strip   = Adafruit_DotStar()                    # SPI, No pixel buffer
# strip   = Adafruit_DotStar(32000000)            # 32 MHz SPI, no pixel buf
# See image-pov.py for explanation of no-pixel-buffer use.
# Append "order='gbr'" to declaration for proper colors w/older DotStar strips)

strip.begin()           # Initialize pins for output
strip.setBrightness(32) # Limit brightness to ~1/4 duty cycle

# Runs 10 LEDs at a time along strip, cycling through red, green and blue.
# This requires about 200 mA for all the 'on' pixels + 1 mA per 'off' pixel.

head  = begin               # Index of first 'on' pixel
tail  = -5             # Index of last 'off' pixel
color = 0xFFFFFF       # 'On' color (starts red)

b = 0
while b < 400:
	strip.setPixelColor(b, 0)
	b = b + 1
	print(strip.getPixelColor(b))
strip.show()

while True:                              # Loop forever

	strip.setPixelColor(head, color) # Turn on 'head' pixel
	#strip.setPixelColor(tail, 0)     # Turn off 'tail'
	strip.show()                     # Refresh strip
	time.sleep(1.0 / 50)             # Pause 20 milliseconds (~50 fps)

	head += 1                        # Advance head position
	if(head >= px + begin):           # Off end of strip?
		head    = begin              # Reset to start
		#color >>= 8              # Red->green->blue->black
		#if(color == 0): color = 0xAA0000 # If black, reset to red

	tail += 1                        # Advance tail position
	if(tail >= px + begin): tail = 0  # Off end? Reset
