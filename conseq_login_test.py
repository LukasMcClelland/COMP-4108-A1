import os, requests, time, datetime

url = 'http://127.0.0.1:5000/login'
names = open('found_usernames.txt', 'r')
nameList = names.readlines()
names.close()
times = [300, 360, 600, 900]
timeCounter = 0

for x in range(7481, 8495):
	while True:
		name = nameList[x]
		name = name.strip('\n')
		print(name)
		payload = {'username': name, 'password': ''}
		r = requests.post(url, payload)
		errorLine = r.text.splitlines()[59]
		print(errorLine)		
		if errorLine.lstrip().startswith("You have exceeded"):
			print("Lockout occured when waiting: " + str(times[timeCounter] / 60) + " minutes.")
			break
		print("No lockout. Waiting " + str(times[timeCounter] / 60) + " minutes.")
		time.sleep(times[timeCounter])		
	timeCounter += 1
	print("Trying next account.")
