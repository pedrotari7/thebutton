#! /usr/bin/python

from BeautifulSoup import BeautifulSoup as BS
import requests
import requests.auth
import json
from websocket import create_connection
import imaplib
import smtplib
import pygame
import json


def hex_to_rgb(value):
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

def get_color(time):
	time = int(time) 
	if time > 0 and time <= 11:
		color = 'e50000'
	elif time > 11 and time <= 21:
		color = 'e59500' 
	elif time > 21 and time <= 31:
		color = 'e5d900'
	elif time > 31 and time <= 41:
		color = '02be01'
	elif time > 41 and time <= 51:
		color = '0083c7'
	elif time > 51 and time <= 60:
		color = '820080'
	print "color: " + str(color)
	print "hex_to_rgb(color): " + str(hex_to_rgb(color))	
	return hex_to_rgb(color)

def get_center_font(image_size,font,text):

	font_dimensions =  font.size(text)
	center = [int(image_size[0]/2), int(image_size[1]/2)]
 	center[0] -= int(font_dimensions[0]/2)
 	center[1] -= int(font_dimensions[1]/2)
 	center = tuple(center)

 	return center

def send_email(receivers, subject, message):
	username='askpedrobot'
	password='askpedrobot2458'
	sender = 'askpedrobot@gmail.com'
	body ="""From: askpedrobot <%s>\nTo: the button slave <%s>\nSubject:%s\n\n%s""" % (sender,receiver,subject,message) 
	print body
	try:
 		smtpObj = smtplib.SMTP('smtp.gmail.com',587)
		smtpObj.ehlo()
		smtpObj.starttls()
		smtpObj.ehlo()
 		smtpObj.login(username,password)
		smtpObj.sendmail(sender, receivers, body)        
		print "Successfully sent email"
	except:
		raise
		print "Error: unable to send email"


url_reddit = 'http://www.reddit.com/r/thebutton'

url = 'http://cors-unblocker.herokuapp.com/get?url=' + url_reddit

button_page =  requests.get(url,headers={}).text

button_soup = BS(button_page)

button_div = button_soup.findAll("script", { "id" : "config" })

button_wss_dict = json.loads(str(button_div[0].text)[0:-1].replace('r.setup(',''))

button_wss = button_wss_dict['thebutton_websocket']

print "button_wss: " + str(button_wss)

ws = create_connection(button_wss)
print "ws: " + str(ws)

#pygame.init()

#image_size = (1024,742)

#window = pygame.display.set_mode(image_size,pygame.RESIZABLE)

#pygame.font.init()
# font = pygame.font.SysFont('monospace',500)
# font.set_bold(True)

f = open('button_record.txt','r')

record = int(f.read(50))

f.close()

print "current record: " + str(record)

receiver = ['pedrotari7@gmail.com','qasar9@gmail.com','rufoliveira@gmail.com']

while 1:

	data = ws.recv()

	data = json.loads(data)

	try:
		current_time = str(int(data['payload']['seconds_left']))
		participants = data['payload']['participants_text']

		# color = get_color(current_time)

		# window.fill(color)

		# for event in pygame.event.get():
			# if event.type == pygame.QUIT: 
				# pygame.quit()
			# elif event.type == pygame.VIDEORESIZE:
				# image_size = event.size
				# window = pygame.display.set_mode(image_size,pygame.RESIZABLE)

		# center = get_center_font(image_size,font,current_time)
		# rendered_font = font.render(current_time,True,(255, 255, 255))
		# window.blit(rendered_font,center)

		if int(current_time) < int(record):

			print 'new record'
			subject = 'New Record : ' + current_time
			message = 'Current number of participants: ' + str(participants)
			send_email(receiver, subject, message)

			record = current_time

			f = open('button_record.txt','w')

			f.write(record)

			f.close()

		if float(participants.replace(',','')) % 100000.0 == 0.0:

			subject = 'Participants : ' + str(participants)
			message = 'Current recor: ' + str(record)
			send_email(receiver, subject, message)

		# pygame.display.update()

	except:
		raise
		pass
