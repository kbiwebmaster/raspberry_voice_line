#!/usr/bin/python
# -*- coding: utf-8 -*-

#import pyaudio
import sys
import os
import commands
import time
#import wave
import urllib3
import requests

RATE = 16000
PATH= '/var/tmp/tmp.wav'
RECORD_SECONDS = 5 #input('収録時間をしていしてください（秒数） >>>')

RECOGNIZE_API = 'https://api.apigw.smt.docomo.ne.jp/amiVoice/v1/recognize'
DOCOMO_TOKEN = 'xxx'

LINE_API = 'https://notify-api.line.me/api/notify'
LINE_TOKEN = 'ixxx'

# recording
def listen(sec, path):
  print (">>listening...")
  cmdline = 'arecord -D plughw:0,0 -r '+ str(RATE) +' -f S16_LE -d '+ str(sec) +' '+ path 
  print (cmdline)
  print (commands.getoutput(cmdline))
  return os.path.getsize(PATH)

# play
def play(path):
  print (">>play "+ path)
  cmdline = 'aplay -D plughw:1,0 '+ path 
  print (cmdline)
  os.system(cmdline)

# call docomo recognize API
def recognize(path):
  url = RECOGNIZE_API + '?APIKEY=' + DOCOMO_TOKEN
  f = open(PATH, 'rb')
  data = f.read()
  f.close()
  files = {"a": open(path, 'rb'), "v":"on"}
  r = requests.post(url, files=files)
  message = r.json()['text']
  print (message) 
  return message

# call line API
def notify(message):
  headers = {"Authorization" : "Bearer "+ LINE_TOKEN}
  payload = {"message" :  message}
#files = {"imageFile": open("test.jpg", "rb")} #バイナリで画像ファイルを開きます。対応している形式はPNG/JPEGです。
#r = requests.post(url ,headers = headers ,params=payload, files=files)
  r = requests.post(LINE_API ,headers = headers ,params=payload)

# main
if __name__=='__main__':
  size = listen(RECORD_SECONDS, PATH)
  play(PATH)
  message = recognize(PATH)
  notify(message)
  print (">>exit")
  
  

