from __future__ import unicode_literals
import youtube_dl
from pydub import AudioSegment
import numpy as np
import sys
import os
import bs4
from selenium import webdriver
from bs4 import BeautifulSoup as soup
from gtts import gTTS
import pyaudio
import re
import speech_recognition as sr
from urllib2 import urlopen
import pyaudio  
import wave

r = sr.Recognizer()
r.energy_threshold = 4000
chunk = 1024

def playSound(input):
	tts = gTTS(text=input, lang='en')
	tts.save("output.mp3")
	os.system("mpg321 output.mp3")
	os.remove("output.mp3")

def GetVoice(text):
	with sr.Microphone() as source:
		print(text)
		audio = r.listen(source)
	try: 
	    Voice = r.recognize_google(audio)
	except LookupError:
	    print("Could not understand audio")
	
	Voice = Voice.strip()
	return Voice


def PlaySong():
	playSound('What song would you like to play?')
	SongName = GetVoice('Say the name of the song Outloud')
	url = 'https://www.youtube.com/results?search_query=' + SongName.replace(' ', '%20')
	content = urlopen(url).read()
	htmlSoup = soup(content, "lxml")
	tag = htmlSoup.find('a', {'rel': 'spf-prefetch'})
	title = tag.text
	playSound('Would you like to play' + title)
	YesNo = GetVoice('Answer Yes or No')
	renamed = tag.get('href')
	video_url = 'http://www.youtube.com/' + tag.get('href')
	renamed = renamed.replace('watch?v=','')
	renamed = renamed.replace('/','')
	print(renamed)
	if YesNo == 'yes':
		ydl_opts = {
			'format': 'bestaudio/best',
			'postprocessors': [{
			'key': 'FFmpegExtractAudio',
			'preferredcodec': 'wav',
			'preferredquality': '192',
			}],
		}
		with youtube_dl.YoutubeDL(ydl_opts) as ydl:
			ydl.download([video_url])
		print('Playing: ' + SongName + '\n')
		filename = title + '-' + renamed + '.wav'
		print("Filename: " + filename)
		f = wave.open(filename,"rb")  
		p = pyaudio.PyAudio()  
		stream = p.open(format = p.get_format_from_width(f.getsampwidth()),  
		                channels = f.getnchannels(),  
		                rate = f.getframerate(),  
		                output = True)  
		data = f.readframes(chunk)  
		while data:  
		    stream.write(data)  
		    data = f.readframes(chunk)   
		stream.stop_stream()  
		stream.close()  
		p.terminate() 
		os.remove(filename)
	else:
		playSound('I will not play ' + SongName)


PlaySong()