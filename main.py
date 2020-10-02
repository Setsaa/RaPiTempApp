from sense_hat import SenseHat
import time
import csv

sense = SenseHat()
sense.clear()
sense.low_light = True

red = (255,0,0)
green = (0,255,0)
orange = (255,165,0)

def send_email(user, pwd, recipient, subject, body):
    import smtplib

    FROM = user
    TO = recipient if isinstance(recipient, list) else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(user, pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        print('successfully sent the mail')
    except:
        print("failed to send mail")

while(True):
	
	p = sense.get_pressure()
	t = sense.get_temperature()
	h = sense.get_humidity()

	p = round(p,1)
	t = round(t,1)
	h = round(h,1)

	measurements = "Temp: " + str(t) + "," "Pressure: " + str(p) + "," "Humidity: " + str(h)
	temp = str(t)

	if (h >= 40) and (h <= 60):
		normal_hum = True
	else:
		normal_hum = False

	if (h > 56 and h < 60) or (h > 40 and h < 44):
		bc = orange
	elif normal_hum:
		bc = green
	else:
		bc = red

	new_measurements = (p != round(sense.get_pressure(), 1)) or ((t != round(sense.get_temperature(), 1)) or (h != round(sense.get_humidity(), 1)))
	
	if (new_measurements):
		print ("New measurements @ " + str(time.asctime()) + ":")
		print ("Temperature: " + str(t) + "C" "\nPressure:    " + str(p) + "mb" "\nHumidity:    " + str(h) + "%")
		print ("")
		sense.clear(bc)

		if (normal_hum == False):
			email_message = f'The current humidity level in your bedroom is: {h}%. Consider actions.'
			send_email("EMAIL", "PWD", "EMAIL", "Humidity alert for bedroom", email_message)
		# sense.show_message(temp, scroll_speed=0.08)
	time.sleep(10)

	# bedroom = open("BedroomLog.csv", "w", newline="")
	# livingroomUp = open("LivingroomUpLog.csv", "w", newline="")
	"""
	with open("LivingroomUpLog.csv", "w") as livingroomUp:
		logwriter = csv.writer(livingroomUp, delimiter=",",quotechar='"', quoting=csv.QUOTE_MINIMAL)
		logwriter.writerow(measurements)
	"""
	"""
	with open('eggs.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=' ',
                           	quotechar='|', quoting=csv.QUOTE_MINIMAL)
   	spamwriter.writerow(['Spam'] * 5 + ['Baked Beans'])
    spamwriter.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'])
	"""
