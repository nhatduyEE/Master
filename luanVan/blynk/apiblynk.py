import subprocess
import os
import RPi.GPIO as io
import dropbox
from dropbox.files import WriteMode
from blynkapi import Blynk
import time
import unicodedata
import thread


files='/home/pi/hinh/{0}.jpeg'
f=open('/home/pi/config/auth.txt','r')
auth=f.read(32)
f.close()
e=open('/home/pi/config/email.txt','r')
em=e.read().strip()
e.close()
#auth="5308db499c81455cac655562ba5967f0"
notification='The door is open, Image Link send to email'

notify=Blynk(auth)
sendmail=Blynk(auth)
led=Blynk(auth,pin='V5')
device1=Blynk(auth,pin='V3')
std1=Blynk(auth,pin='V2')
###########################################################
# create IO
io.setmode(io.BCM)
io.setup(4,io.IN,pull_up_down=io.PUD_DOWN) # Sensor input
io.setup(16,io.OUT)
# configarution dropbox
dbx=dropbox.Dropbox('58tDXm_qTmAAAAAAAAAAEmntpAVf_FVI3S2DtJvR8zKBLy_eNuz9rB2TmCOREfiX')
link='https://www.dropbox.com/sh/yzlaq6k5oicazzu/AAA83ia5wBg4UzqATkR3EPbTa?dl=0'

##########################################################
# function upload image
def upfile(i):
        with open(files.format(i), 'rb') as f:
            dbx.files_upload(f.read(),'/home/Hinh{0}.jpeg'.format(i), mode=WriteMode('overwrite'))

##########################################################
# function capture image
def captureImage(i):
        subprocess.call('fswebcam -r 640x480 --set brightness=50%  --jpeg 95 /home/pi/hinh/{0}.jpeg'.format(i),shell=True)


def statushw(e):
	while 1:
		led.set_val('["255"]')
		time.sleep(e)
       		led.off()
		time.sleep(e)


a=0
def main():
	global a
	print('OK')
	while 1:
    		if io.input(4)==1:
        		print('Open')
			for i in range(5):
	            		captureImage(i)
        	    		upfile(i)
        		notify.push(notification)
			d=sendmail.email(em,'https://www.dropbox.com/sh/yzlaq6k5oicazzu/AAA83ia5wBg4UzqATkR3EPbTa?dl=0','Link')
			io.output(16,io.HIGH)
			time.sleep(5)
			io.output(16,io.LOW)
			a=1

		d1=device1.get_val()
		if(d1==[u'1']):
			std1.set_val('["255"]')
		else:
			std1.off()
if __name__ == '__main__':
    thread.start_new_thread( statushw, (1,))
    main()
