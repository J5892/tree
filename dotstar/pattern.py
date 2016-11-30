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

def flicker():
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

def swipe():
  layers = [77, 59, 49, 42, 31, 22, 12, 6, 6, 1]
  total = 305
  shown = {
    3: 39,
    4: 28,
    5: 19,
    6: 9
  }

  while True:
    percent = 0.0

    while percent <= 1.0:
      begin = 0
      px = 0
      while px < total:
        v = mono(s.getPixelColor(px))
        if v > 0:
          v = v - 2
          s.setPixelColor(px, rgb(v))

      for l, num in enumerate(layers):
        n = num
        if l in shown:
          n = shown[l]
        px = int(round(n * percent)) + begin
        s.setPixelColor(px - 1, 0)
        s.setPixelColor(px, 0xFFFFFF)

        begin = begin + num
      percent = percent + 0.01
      time.sleep(1.0 / 50)

swipe()
