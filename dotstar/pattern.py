#!/usr/bin/python

import time
import random
import urllib2
import thread
import json
from dotstar import Adafruit_DotStar

data = {
  'requests': 0,
  'version': 0,
  'pattern': 'swipe'
}

def getData(data = {}):
  time.sleep(5)
  j = urllib2.urlopen('http://j5.fyi/tree.json').read()
  d = json.loads(j)
  data['version'] = d['version']
  data['pattern'] = d['pattern']
  data['requests'] = data['requests'] + 1

def watchRequests(v, r):
  if data['requests'] != r:
    r = data['requests']
    print('request ' + str(r))
    if data['version'] != v:
      v = data['version']
      print('version ' + str(v))
      print(data)
      return True, True
    thread.start_new_thread(getData, (), {'data': data})
  return v, r


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

  version = data['version']
  requests = data['requests']

  r = 0
  while True:
    pixel = 0
    if r >= 20:
      r = 0
      print('20 flickers done')
      version, requests = watchRequests(version, requests)
      if type(version) == bool:
        break
    while pixel < num:
      twinkle(pixel)
      pixel = pixel + 1

    s.show()
    time.sleep(1.0 / 20)
    r = r + 1

def swipe():
  layers = [77, 59, 49, 42, 31, 22, 12, 6, 6, 1]
  total = 305
  shown = {
    3: 39,
    4: 28,
    5: 19,
    6: 9
  }
  offsets = {
    0: 10
  }

  version = data['version']
  requests = data['requests']

  while True:
    percent = 0.0
    print('repeat swipe')
    version, requests = watchRequests(version, requests)
    if type(version) == bool:
      break

    while percent <= 1.0:
      begin = 0
      px = 0
      while px < total:
        v = mono(s.getPixelColor(px))
        if v > 0:
          v = v - 5
          s.setPixelColor(px, rgb(v))
        px = px + 1

      for l, num in enumerate(layers):
        n = num
        if l in shown:
          n = shown[l]
        if l in offsets:
          n = n - offsets[l]
          if n < 0:
            n = n + num
        px = int(round(n * percent)) + begin
        s.setPixelColor(px, 0xFFFFFF)

        begin = begin + num
      s.show()
      percent = percent + 0.01
      time.sleep(1.0 / 50)

thread.start_new_thread(getData, (), {'data':data})

swipe()

methods = globals().copy()
while True:
  function = methods.get(data['pattern'])
  print('switching')
  if function != None:
    function()
  else:
    swipe()
