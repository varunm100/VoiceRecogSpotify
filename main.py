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
import shutil
import subprocess
from os import listdir

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
	AllSongNames = ''
	playSound('What song would you like to play?')
	SongName = GetVoice('Say the name of the song Outloud')
	if 'playlist' in SongName:
		AllSongNames = listdir('Songs')
		for SingleSongs in AllSongNames:
			print("Currently Playing - " + str(SingleSongs))
			subprocess.call(['vlc', '-vvv', 'Songs/' + str(SingleSongs)])
	elif 'play all' in SongName:
		AllSongNames = listdir('Songs')
		for SingleSongs in AllSongNames:
			print("Currently Playing - " + str(SingleSongs))
			subprocess.call(['vlc', '-vvv', 'Songs/' + str(SingleSongs)])
	else:
		AddPlaylistBool = GetVoice('Would you like to add ' + str(SongName) + ' to your playlist?')
		if AddPlaylistBool == 'yes':
			AddPlaylistBool = True
			playSound("Ok, this song will be added to your playlist")
		else:
			AddPlaylistBool = False
			playSound("Ok, I will not add this to your playlist")
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
			try:
				print("Filename: " + filename)
			except:
				pass
			shutil.move(filename, "Songs/")
			if AddPlaylistBool != True:
				os.remove('Songs/' + str(filename))
			subprocess.call(['vlc', '-vvv', 'Songs/' + str(filename)])

PlaySong()