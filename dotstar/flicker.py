#!/usr/bin/python

import time
import random
from dotstar import Adafruit_DotStar


num = 500

s = Adafruit_DotStar(num, 12000000)

s.begin()
s.setBrightness(255)

def mono(h):
  return h >> 16

def rgb(d):
  return (d << 16) + (d << 8) + d

def twinkle(p):
  i = mono(s.getPixelColor(p))
  if i == 0:
    if random.random() < 0.03:
      s.setPixelColor(p, 0xFFFFFF)
      return True
    s.setPixelColor(p, 0)
    return True

  else:
    i = i - 20
    if (i < 0):
      s.setPixelColor(p, 0)
      return True
    s.setPixelColor(p, rgb(i))
    return True

s.setPixelColor(0, 0xFFFFFF)
s.show()
time.sleep(2)
s.setPixelColor(0, 0x000000)
s.show()

while True:
  pixel = 0
  while pixel < num:
    twinkle(pixel)
    pixel = pixel + 1

  s.show()
  time.sleep(1.0 / 20)
