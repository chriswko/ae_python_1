from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import time
import sys
import urllib
import math
import pickle

dict_struct = {'Urban': 0, 'Solar': 0, 'Gas': 0, 'Fusion': 0, 'Antimatter': 0, 'Orbital': 0, 'Research': 0, 'Metal': 0, 'Crystal': 0, 'Robotic': 0, 'Shipyards': 0, 'Spaceports': 0, 'Command': 0, 'Nanite': 0, 'Android': 0, 'Economic': 0, 'Terraform': 0, 'Multi-Level': 0, 'Jump': 0, 'Barracks': 0, 'Laser': 0, 'Missile': 0, 'Plasma': 0, 'Ion': 0, 'Photon': 0, 'Disruptor': 0, 'Deflection': 0, 'Planetary': 0}
dict_units = {'Fighters' : 0, 'Bombers' : 0, 'Corvette' : 0, 'Recycler' : 0, 'Destroyer' : 0, 'Frigate' : 0, 'Scout' : 0, 'Outpost' : 0, 'Cruiser' : 0, 'Carrier' : 0, 'Heavy' : 0}
dict_tech = {'Energy' : 0, 'Computer' : 0, 'Armour' : 0, 'Laser' : 0, 'Missiles' : 0, 'Stellar' : 0, 'Plasma' : 0, 'Warp' : 0, 'Shielding' : 0, 'Ion' : 0, 'Photon' : 0, 'Artificial' : 0, 'Disruptor' : 0, 'Cybernetics' : 0, 'Techyon' : 0, 'Anti-Gravity' : 0}
dict_tech_inQueue = {'Energy' : 0, 'Computer' : 0, 'Armour' : 0, 'Laser' : 0, 'Missiles' : 0, 'Stellar' : 0, 'Plasma' : 0, 'Warp' : 0, 'Shielding' : 0, 'Ion' : 0, 'Photon' : 0, 'Artificial' : 0, 'Disruptor' : 0, 'Cybernetics' : 0, 'Techyon' : 0, 'Anti-Gravity' : 0}
dict_costs = {'Urban': 0, 'Solar': 0, 'Gas': 0, 'Fusion': 0, 'Antimatter': 0, 'Orbital': 0, 'Research': 0, 'Metal': 0, 'Crystal': 0, 'Robotic': 0, 'Shipyards': 0, 'Spaceports': 0, 'Command': 0, 'Nanite': 0, 'Android': 0, 'Economic': 0, 'Terraform': 0, 'Multi-Level': 0, 'Jump': 0}
dict_unlocked = {'Planetary' : False, 'Deflection' : False, 'Disruptor' : False, 'Photon' : False, 'Ion' : False, 'Plasma' : False, 'Missile' : False, 'Laser' : False, 'Barracks' : False, 'Spaceports' : True, 'Shipyards' : True, 'Crystal' : True, 'Urban' : True, 'Research' : True, 'Gas' : True, 'Solar' : True, 'Metal' : True, 'Fusion' : False, 'Antimatter' : False, 'Robotic' : False, 'Orbital' : False, 'Command' : False, 'Nanite' : False, 'Android' : False, 'Economic' : False, 'Terraform' : False, 'Multi-Level' : False, 'Jump' : False}
dict_energy = {'Solar' : 0, 'Gas' : 0, 'Fusion' : 4, 'Antimatter' : 10}
dict_advanced = {'Fusion' : True, 'Spaceports' : True, 'Command' : True, 'Jump' : True, 'Metal' : True, 'Crystal' : True, 'Robotic' : True, 'Shipyards' : True, 'Urban' : True, 'Solar' : True, 'Gas' : True, 'Antimatter' : True, 'Research' : True, 'Nanite' : True, 'Android' : True, 'Economic' : True, 'Terraform' : True, 'Orbital' : True, 'Multi-Level' : True}
baseCost = [100,200,500,1000,2000,5000,10000,20000]
scanned = ""
baseEcon = 0
nrTechBase = 0
free = False
upgraded = False
queues = []
bases = 0
tech_bases = 0
name = ""
email = ""
pas = "testtest"
driver = ""

def startDriver():
	global driver
	driver = webdriver.Chrome()
	
def endDriver():
	global driver
	driver.quit()

def find_by_xpath(locator):
        element = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, locator))
        )

        return element
		
class FormPage(object):
	def fill_form(self):
		global email
		global pas
		find_by_xpath('.//*[@id="login"]/table/tbody/tr[1]/td[2]/input').send_keys("chrkolby@gmail.com")
		find_by_xpath('//input[@name = "pass"]').send_keys("kolbykolby")
		return self # makes it so you can call .submit() after calling this function
	
	def login(self):
		global free
		global upgraded
		global bases
		global f
		global scanned
		temp = find_by_xpath('.//*[@id="login"]/table/tbody/tr[3]/th/input')
		driver.execute_script("arguments[0].click();",temp)
		driver.get("http://alpha.astroempires.com/account.aspx")
		status = find_by_xpath(".//*[@id='account_main']/tbody/tr[2]/td/table/tbody/tr/td[2]/div/table/tbody/tr/td[2]/table/tbody/tr/td[1]/center/table/tbody/tr[4]/td[2]").text
		if status == "Free":
			free = True
		if status == "Upgraded":
			upgraded = True
		try:
			fo = open('scanned.txt', 'r')
			scanned = fo.read()
			fo.close()
			print(scanned)
		except:
			pass
		if scanned == "Scanned":
			pass
		else:
			runScan()
		bases = amountOfBases()
		get_tech()
		techBases()
		click_units()
		needBase()
		baseToFill()
		print(free)
		print(upgraded)
		
def runScan():
	f=open('scanned.txt', 'w')
	f.write("Scanned")
	f.close()
	click_empire()
	goHomeRegion()
	checkRegion()
		
def logged():
	bases = amountOfBases()
	get_tech()
	techBases()
	click_units()
	needBase()
	baseToFill()
	
def unlocked():
	global dict_unlocked
	global dict_tech
	if dict_tech['Energy'] > 5:
		dict_unlocked['Fusion'] = True
	if dict_tech['Energy'] > 19:
		dict_unlocked['Antimatter'] = True
	if dict_tech['Computer'] > 1:
		dict_unlocked['Robotic'] = True
	if dict_tech['Computer'] > 5:
		dict_unlocked['Command'] = True
	if dict_tech['Computer'] > 9:
		if dict_tech['Laser'] > 7:
			dict_unlocked['Nanite'] = True
	if dict_tech['Artificial'] > 3:
		dict_unlocked['Android'] = True
	if dict_tech['Computer'] > 9:
		dict_unlocked['Economic'] = True
	if dict_tech['Computer'] > 9:
		if dict_tech['Energy'] > 9:
			dict_unlocked['Terraform'] = True
	if dict_tech['Armour'] > 21:
		dict_unlocked['Multi-Level'] = True
	if dict_tech['Computer'] > 19:
		dict_unlocked['Orbital'] = True
	if dict_tech['Warp'] > 11:
		if dict_tech['Energy'] > 19:
			dict_unlocked['Jump'] = True
	if dict_tech['Laser'] > 0:
		dict_unlocked['Barracks'] = True
		dict_unlocked['Laser'] = True
	if dict_tech['Missiles'] > 0:
		dict_unlocked['Missile'] = True
	if dict_tech['Plasma'] > 0:
		if dict_tech['Armour'] > 5:
			dict_unlocked['Plasma'] = True
	if dict_tech['Ion'] > 0:
		if dict_tech['Armour'] > 9:
			if dict_tech['Shielding'] > 1:
				dict_unlocked['Ion'] = True
	if dict_tech['Photon'] > 0:
		if dict_tech['Armour'] > 13:
			if dict_tech['Shielding'] > 5:
				dict_unlocked['Photon'] = True
	if dict_tech['Disruptor'] > 0:
		if dict_tech['Armour'] > 17:
			if dict_tech['Shielding'] > 7:
				dict_unlocked['Disruptor'] = True
	if dict_tech['Ion'] > 5:
			if dict_tech['Shielding'] > 9:
				dict_unlocked['Deflection'] = True
	if dict_tech['Photon'] > 9:
		if dict_tech['Armour'] > 21:
			if dict_tech['Shielding'] > 11:
				dict_unlocked['Planetary'] = True
	
def log():
	driver.get('http://alpha.astroempires.com')
	FormPage().fill_form()
	FormPage().login()
	
def changeDisplay():
	find_by_xpath(".//*[@id='account']").send_keys(Keys.ENTER)
	btn_display = find_by_xpath(".//*[@id='menu_button_display']/div[2]/div")
	driver.execute_script("arguments[0].click();", btn_display)
	find_by_xpath("//select[@name='skin']/option[text()='Blue Nova (v1)']").click()
	btn = find_by_xpath(".//*[@id='account_main']/div[2]/div[2]/table/tbody/tr/td[2]/div[1]/div/div[2]/div[2]/table/tbody/tr[6]/td[2]/input")
	driver.execute_script("arguments[0].click();", btn)
	
def click_empire():
	driver.get('http://alpha.astroempires.com/empire.aspx')

def click_bases():
	driver.get('http://alpha.astroempires.com/base.aspx')
	
def click_map():
	driver.get('http://alpha.astroempires.com/map.aspx')
	
def click_fleets():
	driver.get('http://alpha.astroempires.com/fleet.aspx')
	
def click_commanders():
	driver.get('http://alpha.astroempires.com/commander.aspx')
	
def click_guild():
	driver.get('http://alpha.astroempires.com/guild.aspx')
	
def num_there(s):
    return any(i.isdigit() for i in s)
	
def get_num(s):
	return ''.join(x for x in s if x.isdigit())
	
	
def check_Msg():
	message = find_by_xpath(".//*[@id='main-header-infobox_content']/tbody/tr[1]/td[7]/table/tbody/tr/td[2]")
	print(message.text)
	s = ''.join(x for x in message.text if x.isdigit())
	print(s)
	int(s)
	a = '0'
	if s != a:
		print(s)
		find_by_xpath(".//*[@id='messages']/tbody/tr/td[2]/a").send_keys(Keys.ENTER)
		
def amountOfBases():
	global tech_bases
	driver.get("http://alpha.astroempires.com/empire.aspx?view=economy")
	x = find_by_xpath('//*[@id="empire_economy_summary"]/tbody/tr[2]/td/table/tbody/tr/td[2]/div/table/tbody/tr[2]/td[2]').text
	x = int(x)
	click_empire()
	tech_bases = 0
	print(x)
	return x
		
def techBases():
	click_empire()
	global tech_bases
	for i in range(bases):
		i = i+1
		click_empire()
		try:
			x = find_by_xpath(".//*[@id='empire_events']/tbody/tr[2]/td/table/tbody/tr/td[2]/div/table/tbody/tr[%d]/td[8]/a" %i)
			x.send_keys(Keys.ENTER)
			while 1:
				filled = True
				filled = doTech()
				if filled:
					pass
				else:
					break
			tech_bases = tech_bases + 1
		except:
			print("LMAO FUCK YOU")
			pass
	print(tech_bases)
	
def FTProd():
	print("FTPROD")
	find_by_xpath(".//*[@id='production']/tbody/tr/td[2]/a").send_keys(Keys.ENTER)
	ftCount = 0
	try:
		ftCount = find_by_xpath(".//*[@id='base_production']/tbody/tr[2]/td/table/tbody/tr/td[2]/div/form/table/tbody/tr[2]/td[2]/span/b").text
	except:
		pass
	ftCount = int(ftCount)
	print(ftCount)
	print(bases)
	if bases < 3:
		print("<3")
		if ftCount < 1:
			queueFT(1)
	elif bases < 5:
		print("<5")
		if ftCount < 20:
			amountToQueue = 20 - ftCount
			queueFT(amountToQueue)
	elif bases < 6:
		print("<6")
		if ftCount < 100:
			amountToQueue = 100 - ftCount
			queueFT(amountToQueue)
	elif bases < 7:
		print("<7")
		if ftCount < 100:
			amountToQueue = 100 - ftCount
			queueFT(amountToQueue)
	elif bases < 8:
		print("<8")
		if ftCount < 200:
			amountToQueue = 200 - ftCount
			queueFT(amountToQueue)
	elif bases < 9:
		print("<9")
		if ftCount < 300:
			amountToQueue = 300 - ftCount
			queueFT(amountToQueue)
	elif bases > 8:
		print(">8")
		if ftCount < 500:
			amountToQueue = 500 - ftCount
			queueFT(amountToQueue)
			
def queueFT(i):
	print("queueFT")
	print(i)
	try:
		OSquant = find_by_xpath(".//*[@id='quantFighters']").send_keys("%d" %i)
		button = driver.find_elements_by_class_name("input-button")[1]
		driver.execute_script("arguments[0].click();", button)
	except:
		pass
	
		
def fillDicts():
	aaaa = find_by_xpath(".//*[@id='base_structures']/tbody/tr[2]/td/table/tbody/tr/td[2]/div/table/tbody").text
	aaa = len(aaaa.splitlines())
	long = int(((aaa-1)/5))
	global dict_struct
	global dict_def
	for i in range(long*2):
		i = i+2
		try:		
			s = 0
			str = (".//*[@id='base_structures']/tbody/tr[2]/td/table/tbody/tr/td[2]/div/table/tbody/tr[%d]/td[2]" %i)
			hh = find_by_xpath(str)
			temp = hh.text
			fword = temp.partition(' ')[0]
			fword = fword.partition('\n')[0]
			fword = re.sub('[-]', '', fword)
			fline = temp.splitlines()
			if num_there(fline[0]):
				s = ''.join(x for x in fline[0] if x.isdigit())
			else:
				s = 0
			dict_struct[fword] = int(s)
		except:
			print("error")
			
	i = 0
	while(i < (long*2)):
		i = i+2
		try:
			current = find_by_xpath(".//*[@id='base_structures']/tbody/tr[2]/td/table/tbody/tr/td[2]/div/table/tbody/tr[%d]/td[7]" %i).text
			fword = current.partition(':')[0]
		except: 
			print("error")
		print(fword)
		if num_there(fword):
			str = find_by_xpath(".//*[@id='base_structures']/tbody/tr[2]/td/table/tbody/tr/td[2]/div/table/tbody/tr[%d]/td[2]" %i).text
			fword = str.partition(' ')[0]
			fword = fword.partition('\n')[0]
			fword = re.sub('[-]', '', fword)
			dict_struct[fword] = int(dict_struct[fword]) + 1

	findEnergyValues()
	godef = find_by_xpath(".//*[@id='defenses']/tbody/tr/td[2]/a")
	godef.send_keys(Keys.ENTER)
	new = ""
	try:
		new = find_by_xpath('//*[@id="base_defenses"]/tbody/tr[2]/td/table/tbody/tr/td[2]/div/center').text
		print(new)
	except:
		pass
	if "You must" in new:
		find_by_xpath(".//*[@id='structures']/tbody/tr/td[2]/a").send_keys(Keys.ENTER)
	else:
		aaaa = find_by_xpath(".//*[@id='base_defenses']/tbody/tr[2]/td/table/tbody/tr/td[2]/div/table/tbody").text
		aaa = len(aaaa.splitlines())
		long = int(((aaa-1)/5))
		print(long)
		for i in range(long*2):
			i = i+2
			try:		
				str = (".//*[@id='base_defenses']/tbody/tr[2]/td/table/tbody/tr/td[2]/div/table/tbody/tr[%d]/td[2]" %i)
				hh = find_by_xpath(str)
				temp = hh.text
				fword = temp.partition(' ')[0]
				fword = fword.partition('\n')[0]
				fword = re.sub('[-]', '', fword)
				fline = temp.splitlines()
				word = fline[0]
				m = 0
				for i, c in enumerate(word):
					if c.isdigit():
						m = i
						break
				if m:
					s = word[m]
				else:
					s = 0
				dict_struct[fword] = int(s)
			except:
				print("error")
			
	global queues
	queues.clear()
	inQueue()
	print(queues)
	for i, x in enumerate(queues):
		if "\n" in x:
			pass
		else:
			fword = x.partition(' ')[0]
			dict_struct[fword] = int(dict_struct[fword]) + 1
		
	i = 0
	if "You must" in new:
		pass
	else:
		while(i < (long*2)):
			i = i+2
			try:
				current = find_by_xpath(".//*[@id='base_defenses']/tbody/tr[2]/td/table/tbody/tr/td[2]/div/table/tbody/tr[%d]/td[7]" %i).text
				fword = current.partition(':')[0]
			except: 
				print("error")
			if num_there(fword):
				str = find_by_xpath(".//*[@id='base_defenses']/tbody/tr[2]/td/table/tbody/tr/td[2]/div/table/tbody/tr[%d]/td[2]" %i).text
				fword = str.partition(' ')[0]
				fword = fword.partition('\n')[0]
				fword = re.sub('[-]', '', fword)
				dict_struct[fword] = int(dict_struct[fword]) + 1

	find_cost()
	freeLimit()
	#find_by_xpath(".//*[@id='structures']/tbody/tr/td[2]/a").send_keys(Keys.ENTER)
	#findEnergyValues()
			
def find_cost():
	print("find_cost")
	global dict_costs
	dict_costs['Urban'] = int(math.ceil((1*pow(1.5,(int(dict_struct['Urban']))))))
	dict_costs['Solar'] = int(math.ceil((1*pow(1.5,(int(dict_struct['Solar']))))))
	dict_costs['Gas'] = int(math.ceil((1*pow(1.5,(int(dict_struct['Gas']))))))
	dict_costs['Fusion'] = int(math.ceil((20*pow(1.5,(int(dict_struct['Fusion']))))))
	dict_costs['Antimatter'] = int(math.ceil((2000*pow(1.5,(int(dict_struct['Antimatter']))))))
	dict_costs['Research'] = int(math.ceil((2*pow(1.5,(int(dict_struct['Research']))))))
	dict_costs['Metal'] = int(math.ceil((1*pow(1.5,(int(dict_struct['Metal']))))))
	dict_costs['Crystal'] = int(math.ceil((2*pow(1.5,(int(dict_struct['Crystal']))))))
	dict_costs['Robotic'] = int(math.ceil((5*pow(1.5,(int(dict_struct['Robotic']))))))
	dict_costs['Shipyards'] = int(math.ceil((5*pow(1.5,(int(dict_struct['Shipyards']))))))
	dict_costs['Spaceports'] = int(math.ceil((5*pow(1.5,(int(dict_struct['Spaceports']))))))
	dict_costs['Command'] = int(math.ceil((20*pow(1.5,(int(dict_struct['Command']))))))
	dict_costs['Nanite'] = int(math.ceil((80*pow(1.5,(int(dict_struct['Nanite']))))))
	dict_costs['Android'] = int(math.ceil((1000*pow(1.5,(int(dict_struct['Android']))))))
	dict_costs['Economic'] = int(math.ceil((80*pow(1.5,(int(dict_struct['Economic']))))))
	dict_costs['Terraform'] = int(math.ceil((80*pow(1.5,(int(dict_struct['Terraform']))))))
	dict_costs['Multi-Level'] = int(math.ceil((10000*pow(1.5,(int(dict_struct['Multi-Level']))))))
	dict_costs['Orbital'] = int(math.ceil((2000*pow(1.5,(int(dict_struct['Orbital']))))))
	dict_costs['Jump'] = int(math.ceil((5000*pow(1.5,(int(dict_struct['Jump']))))))
	for i, x in enumerate(dict_costs):
		print ("dict['%s']: " % x, dict_costs[x])
		
def doTheBase():
	fillDicts()
	#find_by_xpath(".//*[@id='structures']/tbody/tr/td[2]/a").send_keys(Keys.ENTER)
	while 1:
		try:
			done = False
			print("doTheBase in while")
			if(bases == 1):
				done = doBaseOne()
			else:
				done = whatToQueue()
			print("just kill me")
			
			if done:
				break
			
		except:
			break
	print("before FTProd")
	FTProd()
	goTrade()

def doBaseOne():
	cant = False
	print("doBaseOne")
	find_by_xpath(".//*[@id='structures']/tbody/tr/td[2]/a").send_keys(Keys.ENTER)
	if dict_struct["Metal"] < 3:
		print("in first metal")
		whatToQueue()
	elif dict_struct["Research"] < 3:
		print("TESTERONI")
		try:
			find_by_xpath("//select[@name='item']/option[text()='Research Labs']").click()
			dict_struct["Research"] = dict_struct["Research"] + 1
			addToQueue()
		except:
			cant = True
			print(cant)
	elif dict_struct["Metal"] < 8:
		whatToQueue()
	elif dict_struct["Research"] < 6:
		try:
			find_by_xpath("//select[@name='item']/option[text()='Research Labs']").click()
			dict_struct["Research"] = dict_struct["Research"] + 1
			addToQueue()
		except:
			cant = True
	elif dict_struct["Shipyards"] < 8:
		try:
			find_by_xpath("//select[@name='item']/option[text()='Shipyards']").click()
			dict_struct["Shipyards"] = dict_struct["Shipyards"] + 1
			addToQueue()
		except:
			cant = True
	elif dict_struct["Research"] < 8:
		try:
			find_by_xpath("//select[@name='item']/option[text()='Research Labs']").click()
			dict_struct["Research"] = dict_struct["Research"] + 1
			addToQueue()
		except:
			cant = True
	else: 
		return True
	if cant:
		temp = nextEnergy()
		print("ENERGY")
		try:
			find_by_xpath("//select[@name='item']/option[text()='%s']" %temp).click()
			fword = temp.partition(' ')[0]
			dict_struct[fword] = dict_struct[fword] + 1
			dict_costs[fword] = dict_costs[fword]*1.5
			print("ENERGY")
		except:
			temp = nextPop()
			print("POP")
			try:
				find_by_xpath("//select[@name='item']/option[text()='Urban Structures']").click()
				find_by_xpath("//select[@name='item']/option[text()='%s']" %temp).click()
				fword = temp.partition(' ')[0]
				dict_struct[fword] = dict_struct[fword] + 1
				dict_costs[fword] = dict_costs[fword]*1.5
				print("POP")
			except:
				temp = nextArea()
				print("AREA")
				try:
					find_by_xpath("//select[@name='item']/option[text()='%s']" %temp).click()
					fword = temp.partition(' ')[0]
					dict_struct[fword] = dict_struct[fword] + 1
					dict_costs[fword] = dict_costs[fword]*1.5
					print("AREA")
				except:
					print("FUCK YOU")
		addToQueue()
	
def needBase():
	creds = findCredits()
	creds = int(creds)
	if(bases < 9 ):
		if(baseCost[bases-1]<creds):
			if(dict_units['Outpost']>0):
				find_OS()
			else:
				prodOS()		
			
def prodOS():
	click_empire()
	try:
		find_by_xpath(".//*[@id='empire_events']/tbody/tr[2]/td/table/tbody/tr/td[2]/div/table/tbody/tr[1]/td[7]/a").send_keys(Keys.ENTER)
		OSquant = find_by_xpath(".//*[@id='quantOutpost Ship']").send_keys("1")
		button = driver.find_elements_by_class_name("input-button")[1]
		driver.execute_script("arguments[0].click();", button)
	except:
		pass
		
def techInQueue():
	global queues
	queues.clear()
	inQueue()
	global dict_tech_inQueue
	dict_tech_inQueue = {'Energy' : 0, 'Computer' : 0, 'Armour' : 0, 'Laser' : 0, 'Missiles' : 0, 'Stellar' : 0, 'Plasma' : 0, 'Warp' : 0, 'Shielding' : 0, 'Ion' : 0, 'Photon' : 0, 'Artificial' : 0, 'Disruptor' : 0, 'Cybernetics' : 0, 'Techyon' : 0, 'Anti-Gravity' : 0}
	print("techInQueue")
	print(queues)
	for i, x in enumerate(queues):
		if "\n" in x:
			pass
		else:
			fword = x.partition(' ')[0]
			print(fword)
			dict_tech_inQueue[fword] = int(dict_tech_inQueue[fword]) + 1
	aaaa = find_by_xpath(".//*[@id='base_reseach']/tbody/tr[2]/td/table/tbody/tr/td[2]/div/table/tbody").text
	aaa = len(aaaa.splitlines())
	long = int(((aaa-1)/5))
	i = 0
	print(long)
	while(i < (long*2)):
		i = i+2
		try:
			current = find_by_xpath(".//*[@id='base_reseach']/tbody/tr[2]/td/table/tbody/tr/td[2]/div/table/tbody/tr[%d]/td[5]" %i).text
			fword = current.partition(':')[0]
		except: 
			print("error")
		print(fword)
		if num_there(fword):
			str = find_by_xpath(".//*[@id='base_reseach']/tbody/tr[2]/td/table/tbody/tr/td[2]/div/table/tbody/tr[%d]/td[2]" %i).text
			fword = str.partition(' ')[0]
			fword = fword.partition('\n')[0]
			fword = re.sub('[-]', '', fword)
			dict_tech_inQueue[fword] = int(dict_tech_inQueue[fword]) + 1
	for i, x in enumerate(dict_tech_inQueue):
		print(x)
		print("dict_tech_inQueue[%s]" %x, dict_tech_inQueue[x])
	
	
def doTech():
	filled = True
	print("doTech")
	techInQueue()
	global dict_tech
	global dict_tech_inQueue
	if (dict_tech["Computer"]+dict_tech_inQueue["Computer"]) < 2:
		filled = queueTech("Computer")
	elif (dict_tech["Energy"]+dict_tech_inQueue["Energy"]) < 2:
		filled = queueTech("Energy")
	elif (dict_tech["Laser"]+dict_tech_inQueue["Laser"]) < 1:
		filled = queueTech("Laser")
	elif (dict_tech["Energy"]+dict_tech_inQueue["Energy"]) < 8:
		filled = queueTech("Energy")
	elif (dict_tech["Stellar"]+dict_tech_inQueue["Stellar"]) < 4:
		filled = queueTech("Stellar Drive")
	elif (dict_tech["Warp"]+dict_tech_inQueue["Warp"]) < 1:
		filled = queueTech("Warp Drive")
	if bases > 1:
		if (dict_tech["Computer"]+dict_tech_inQueue["Computer"]) < 4:
			filled = queueTech("Computer")
		elif (dict_tech["Missiles"]+dict_tech_inQueue["Missiles"]) < 1:
			filled = queueTech("Missiles")
		if bases > 2:
			if (dict_tech["Energy"]+dict_tech_inQueue["Energy"]) < 10:
				filled = queueTech("Energy")
			elif (dict_tech["Computer"]+dict_tech_inQueue["Computer"]) < 10:
				filled = queueTech("Computer")
			elif (dict_tech["Laser"]+dict_tech_inQueue["Laser"]) < 8:
				filled = queueTech("Laser")
			elif (dict_tech["Armour"]+dict_tech_inQueue["Armour"]) < 8:
				filled = queueTech("Armour")
			if bases > 3:
				if (dict_tech["Energy"]+dict_tech_inQueue["Energy"]) < 12:
					filled = queueTech("Energy")
				elif (dict_tech["Armour"]+dict_tech_inQueue["Armour"]) < 10:
					filled = queueTech("Armour")
				elif (dict_tech["Laser"]+dict_tech_inQueue["Laser"]) < 10:
					filled = queueTech("Laser")
				elif (dict_tech["Shielding"]+dict_tech_inQueue["Shielding"]) < 2:
					filled = queueTech("Shielding")
				elif (dict_tech["Ion"]+dict_tech_inQueue["Ion"]) < 1:
					filled = queueTech("Ion")
				elif (dict_tech["Energy"]+dict_tech_inQueue["Energy"]) < 16:
					filled = queueTech("Energy")
				elif (dict_tech["Armour"]+dict_tech_inQueue["Armour"]) < 14:
					filled = queueTech("Armour")
				elif (dict_tech["Shielding"]+dict_tech_inQueue["Shielding"]) < 6:
					filled = queueTech("Shielding")
				elif (dict_tech["Plasma"]+dict_tech_inQueue["Plasma"]) < 8:
					filled = queueTech("Plasma")
				elif (dict_tech["Photon"]+dict_tech_inQueue["Photon"]) < 1:
					filled = queueTech("Photon")
				elif (dict_tech["Computer"]+dict_tech_inQueue["Computer"]) < 20:
					filled = queueTech("Computer")
				elif (dict_tech["Energy"]+dict_tech_inQueue["Energy"]) < 20:
					filled = queueTech("Energy")
				elif (dict_tech["Armour"]+dict_tech_inQueue["Armour"]) < 18:
					filled = queueTech("Armour")
				elif (dict_tech["Shielding"]+dict_tech_inQueue["Shielding"]) < 8:
					filled = queueTech("Shielding")
				elif (dict_tech["Laser"]+dict_tech_inQueue["Laser"]) < 18:
					filled = queueTech("Laser")
				elif (dict_tech["Disruptor"]+dict_tech_inQueue["Disruptor"]) < 1:
					filled = queueTech("Disruptor")
				elif (dict_tech["Armour"]+dict_tech_inQueue["Armour"]) < 22:
					filled = queueTech("Armour")
	return filled
	
	
def queueTech(temp):
	filled = True
	try:
		find_by_xpath("//select[@name='item']/option[text()='%s']" %temp).click()
		driver.execute_script("arguments[0].click();",find_by_xpath(".//*[@id='add-to-queue']"))
		time.sleep(1)
	except:
		filled = False
	return filled
		
def baseTechToFill():
	global bases
	global nrTechBase
	for i in range(bases):
		click_empire()
		i = i+1
		try:
			base = find_by_xpath(".//*[@id='empire_events']/tbody/tr[2]/td/table/tbody/tr/td[2]/div/table/tbody/tr[%d]/td[8]/a" %i)
			baseText = base.text
			if free:
				if "(2)" in baseText:
					pass
				else:
					base.send_keys(Keys.ENTER)
					nrTechBase = nrTechBase + 1
					doTech()
			if upgraded:
				if "(5)" in baseText:
					pass
				else:
					base.send_keys(Keys.ENTER)
					nrTechBase = nrTechBase + 1
					doTech()
		except:
			pass
	
def baseToFill():
	global baseEcon
	global bases
	#bases = amountOfBases()
	for i in range(bases):
		click_empire()
		i = i+1
		try:
			base = find_by_xpath(".//*[@id='empire_events']/tbody/tr[2]/td/table/tbody/tr/td[2]/div/table/tbody/tr[%d]/td[6]/a" %i)
			baseEcon = find_by_xpath(".//*[@id='empire_events']/tbody/tr[2]/td/table/tbody/tr/td[2]/div/table/tbody/tr[%d]/td[3]" %i).text
			baseEcon = baseEcon.partition('/')[2]
			baseEcon = int(baseEcon)
			print(baseEcon)
			baseText = base.text
			print(baseText)
			if free:
				if "(2)" in baseText:
					pass
				else:
					base.send_keys(Keys.ENTER)
					doTheBase()
			if upgraded:
				if "(5)" in baseText:
					pass
				else:
					base.send_keys(Keys.ENTER)
					doTheBase()
		except:
			pass
		
def findEnergyValues():
	try:
		temp = find_by_xpath(".//*[@id='base_structures']/tbody/tr[2]/td/table/tbody/tr/td[2]/div/table/tbody/tr[4]/td[2]").text
		fword = temp.partition(' ')[0]
		print(temp)
		print(fword)
		if fword == "Solar":
			sol = find_by_xpath(".//*[@id='base_structures']/tbody/tr[2]/td/table/tbody/tr/td[2]/div/table/tbody/tr[4]/td[4]").text
			if num_there(sol):
				s = ''.join(x for x in sol if x.isdigit())
			else:
				s = 0
			dict_energy[fword] = int(s)
	except:
		print("error")
	try:
		temp = find_by_xpath(".//*[@id='base_structures']/tbody/tr[2]/td/table/tbody/tr/td[2]/div/table/tbody/tr[6]/td[2]").text
		fword = temp.partition(' ')[0]
		if fword == "Gas":
			gas = find_by_xpath(".//*[@id='base_structures']/tbody/tr[2]/td/table/tbody/tr/td[2]/div/table/tbody/tr[6]/td[4]").text
			if num_there(gas):
				s = ''.join(x for x in gas if x.isdigit())
			else:
				s = 0
			dict_energy[fword] = int(s)
	except:
		print("error")
	for i, x in enumerate(dict_energy):
		print ("dict['%s']: " %x, dict_energy[x])
		
def freeLimit():
	if dict_struct["Nanite"] > 4:
		dict_advanced["Nanite"] = False
	if dict_struct["Android"] > 4:
		dict_advanced["Android"] = False
	if dict_struct["Economic"] > 4:
		dict_advanced["Economic"] = False
	if dict_struct["Terraform"] > 4:
		dict_advanced["Terraform"] = False
	if dict_struct["Orbital"] > 4:
		dict_advanced["Orbital"] = False
	if dict_struct["Multi-Level"] > 4:
		dict_advanced["Multi-Level"] = False
	
		
def nextEcon():
	global dict_costs
	global dict_unlocked
	structs = ["Metal Refineries", "Robotic Factories", "Nanite Factories", "Android Factories", "Shipyards", "Spaceports", "Economic Centers"];
	divide = [1.1,1,2,2,1,2,4]
	temp = 500000000
	best = 0
	for i, x in enumerate(structs):
		fword = x.partition(' ')[0]
		if((dict_costs[fword]/divide[i])<temp):
			if dict_unlocked[fword]:	
				if dict_advanced[fword]:
					best = i
					temp = dict_costs[fword]/divide[i]
					print(temp)
					print(dict_costs[fword])
	return structs[best]

def nextEnergy():
	global dict_costs
	global dict_energy
	global dict_unlocked
	structs = ["Solar Plants", "Gas Plants", "Fusion Plants", "Antimatter Plants"]
	temp = 500000000
	best = 0
	for i, x in enumerate(structs):
		fword = x.partition(' ')[0]
		if(dict_energy[fword] > 2):
			if(dict_costs[fword]/dict_energy[fword]<temp):
				if dict_unlocked[fword]:
					if dict_advanced[fword]:
						best = i
						temp = dict_costs[fword]/dict_energy[fword]
	return structs[best]
	
def nextPop():
	populationfrac = find_by_xpath(".//*[@id='local-header_content']/table/tbody/tr[2]/td[5]").text
	totalpopulation = populationfrac.partition('/')[2]
	totalpopulation = int(totalpopulation)
	if(dict_struct['Orbital'] > 0):
		totalpopulation = totalpopulation - (int(dict_struct['Orbital'])*10)
	fert = totalpopulation/int(dict_struct['Urban'])
	divide = [int(fert), 10]
	structs = ["Urban Structures", "Orbital Base"]
	temp = 500000000
	best = 0
	global dict_unlocked
	for i, x in enumerate(structs):
		fword = x.partition(' ')[0]
		if(dict_struct[fword]/divide[i]<temp):
			if dict_unlocked[fword]:
				if dict_advanced[fword]:
					best = i
					temp = dict_costs[fword]/divide[i]
	print(structs[best])
				
	return structs[best]
	
def nextArea():
	global dict_costs
	global dict_unlocked
	temp = 500000000
	best = 0
	divide = [5,10]
	structs = ["Terraform", "Multi-Level Platform"]
	for i, x in enumerate(structs):
		fword = x.partition(' ')[0]
		if(dict_costs[fword]/divide[i]<temp):
			if dict_unlocked[fword]:
				if dict_advanced[fword]:
					best = i
					temp = dict_costs[fword]/divide[i]
	print(structs[best])
	return structs[best]			
	
	

def whatToQueue():
	structure = ""
	global dict_struct
	global baseEcon
	global bases
	print("whatToQueue")
	print(baseEcon)
	do = False
	if bases > 2:
		if baseEcon > 20:
			print("in 20")
			if dict_struct["Missile"] < 2:
				if dict_unlocked["Missile"]:
					find_by_xpath(".//*[@id='defenses']/tbody/tr/td[2]/a").send_keys(Keys.ENTER)
					print("in MT")
					try:
						print("in MT TRY")
						find_by_xpath("//select[@name='item']/option[text()='Missile Turrets']" ).click()
						dict_struct["Missile"] = dict_struct["Missile"] + 1
						addToQueue()
					except:
						pass
		if baseEcon > 40:
			print("in 40")
			if dict_struct["Ion"] < 2:
				if dict_unlocked["Ion"]:
					find_by_xpath(".//*[@id='defenses']/tbody/tr/td[2]/a").send_keys(Keys.ENTER)
					print("in IT")
					try:
						print("in IT try")
						find_by_xpath("//select[@name='item']/option[text()='Ion Turrets']" ).click()
						dict_struct["Ion"] = dict_struct["Ion"] + 1
						addToQueue()
					except:
						pass
		if baseEcon > 60:
			if dict_struct["Photon"] < 2:
				if dict_unlocked["Photon"]:
					find_by_xpath(".//*[@id='defenses']/tbody/tr/td[2]/a").send_keys(Keys.ENTER)
					try:
						find_by_xpath("//select[@name='item']/option[text()='Photon Turrets']" ).click()
						dict_struct["Photon"] = dict_struct["Photon"] + 1
						addToQueue()
					except:
						pass
		if baseEcon > 80:
			if dict_struct["Disruptor"] < 2:
				if dict_unlocked["Disruptor"]:
					find_by_xpath(".//*[@id='defenses']/tbody/tr/td[2]/a").send_keys(Keys.ENTER)
					try:
						find_by_xpath("//select[@name='item']/option[text()='Disruptor Turrets']" ).click()
						dict_struct["Disruptor"] = dict_struct["Disruptor"] + 1
						addToQueue()
					except:
						pass
	print("before structures")
	find_by_xpath(".//*[@id='structures']/tbody/tr/td[2]/a").send_keys(Keys.ENTER)
	if dict_struct["Research"] > 0:
		if bases > 2:
			if dict_struct["Research"] < 12:
				try:
					find_by_xpath("//select[@name='item']/option[text()='Research Labs']" ).click()
					addToQueue()
				except:
					pass
		if bases > 5:
			if dict_struct["Research"] < 16:
				try:
					find_by_xpath("//select[@name='item']/option[text()='Research Labs']" ).click()
					addToQueue()
				except:
					pass
					
		if bases > 8:
			if dict_struct["Research"] < 20:
				try:
					find_by_xpath("//select[@name='item']/option[text()='Research Labs']" ).click()
					addToQueue()
				except:
					pass
	if bases > 2:
		if baseEcon < 30:
			do = True
	if bases > 4:
		if baseEcon < 40:
			do = True
	if bases > 5:
		if baseEcon < 58:
			do = True
	if bases > 6:
		if baseEcon < 68:
			do = True
	if bases > 7:
		if baseEcon < 85:
			do = True
	if bases > 8:
		do = True
		
	if do:
		temp = nextEcon()
		print("RIGHT AFTER NEXTECON")
		try:
			find_by_xpath("//select[@name='item']/option[text()='%s']" %temp).click()
			fword = temp.partition(' ')[0]
			dict_struct[fword] = dict_struct[fword] + 1
			dict_costs[fword] = dict_costs[fword]*1.5
			print("ECON")
			
		except:
			print("RIGHT BEFORE NEXT ENERGY")
			temp = nextEnergy()
			print("ENERGY")
			try:
				find_by_xpath("//select[@name='item']/option[text()='%s']" %temp).click()
				fword = temp.partition(' ')[0]
				dict_struct[fword] = dict_struct[fword] + 1
				dict_costs[fword] = dict_costs[fword]*1.5
				print("ENERGY")
			except:
				temp = nextPop()
				print("POP")
				try:
					find_by_xpath("//select[@name='item']/option[text()='Urban Structures']").click()
					find_by_xpath("//select[@name='item']/option[text()='%s']" %temp).click()
					fword = temp.partition(' ')[0]
					dict_struct[fword] = dict_struct[fword] + 1
					dict_costs[fword] = dict_costs[fword]*1.5
					print("POP")
				except:
					temp = nextArea()
					print("AREA")
					try:
						find_by_xpath("//select[@name='item']/option[text()='%s']" %temp).click()
						fword = temp.partition(' ')[0]
						dict_struct[fword] = dict_struct[fword] + 1
						dict_costs[fword] = dict_costs[fword]*1.5
						print("AREA")
					except:
						return True
	else:
		return True
	addToQueue()
	
def addToQueue():
	driver.execute_script("arguments[0].click();",find_by_xpath(".//*[@id='add-to-queue']"))
	time.sleep(1)

def move_one_OS():
	find_by_xpath(".//*[@id='quantOutpost Ship']").send_keys('1')
	find_by_xpath(".//*[@id='move_fleet_form']/table[3]/tbody/tr/td[4]/small/a[1]").send_keys(Keys.ENTER)
	find_by_xpath(".//*[@id='move_fleet_form']/center/input").send_keys(Keys.ENTER)
			
def fillTrade():
	find_by_xpath(".//*[@id='base_trade']/tbody/tr[2]/td/table/tbody/tr/td[2]/div/center/a").send_keys(Keys.ENTER)
	for i in range(int(bases)+1):
			try:
				find_by_xpath(".//*[@id='base_new-trade']/tbody/tr[2]/td/table/tbody/tr/td[2]/div/form/table/tbody/tr[7]/td[1]/small/a[%d]" %i).send_keys(Keys.ENTER)
				driver.execute_script("arguments[0].click();",find_by_xpath(".//*[@id='base_new-trade']/tbody/tr[2]/td/table/tbody/tr/td[2]/div/form/table/tbody/tr[5]/th/input[2]"))
				success = "no"
				tt = "New Trade Route Set"
				try:
					temp = find_by_xpath(".//*[@id='background-content']/table[4]/tbody/tr[2]/td/table/tbody/tr/td[2]/div/table/tbody/tr/td[2]")
					success = temp.text
				except:
					print(".")
				if success == tt:
					break
			except: 
				print("error")

def goTrade():
	trades = find_by_xpath(".//*[@id='local-header_content']/table/tbody/tr[2]/td[6]")
	trades2 = trades.text.split("/")
	print(bases)
	trades3 = int(trades2[1]) - int(trades2[0])
	for x in range(trades3):
		find_by_xpath(".//*[@id='trade']/tbody/tr/td[2]/a").send_keys(Keys.ENTER)
		time.sleep(2)
		driver.refresh()
		try:
			find_by_xpath(".//*[@id='base_trade']/tbody/tr[2]/td/table/tbody/tr/td[2]/div/center/a").text
			y = 1
		except:
			y = 0
		if y == 1:
			fillTrade()
	
def goHomeRegion():
	find_by_xpath(".//*[@id='empire_events']/tbody/tr[2]/td/table/tbody/tr/td[2]/div/table/tbody/tr[1]/td[2]/a").send_keys(Keys.ENTER)
	find_by_xpath(".//*[@id='background-content']/center[1]/b/a[2]").send_keys(Keys.ENTER)
	
def add_bookmark():
	find_by_xpath(".//*[@id='background-content']/center[1]/a").send_keys(Keys.ENTER)
	
def back_to_system():
	driver.execute_script("window.history.go(-1)")
	find_by_xpath(".//*[@id='background-content']/center[1]/b/a[3]")

def bookmark(specs, metal, gas):
	spec = specs.splitlines()
	area = int(get_num(spec[2]))
	energy = int(get_num(spec[3]))
	fert = int(get_num(spec[4]))
	print("hehehehehhe")
	if area >= 85:
		print("area")
		if energy >= 3 or gas >= 3:
			print("energy")
			if fert >= 5:
				print("fert")
				if metal >= 2:
					add_bookmark()
					back_to_system()

def checkRegion():
	tt = find_by_xpath(".//*[@id='map-region_content']/tbody/tr[2]/td[2]").text
	ttt = tt.splitlines()
	global f
	for x in range(len(ttt)):
		time.sleep(5)
		x = x+1
		find_by_xpath(".//*[@id='map-region_content']/tbody/tr[2]/td[2]/div/div/a[%d]" %x).send_keys(Keys.ENTER)
		for i in range(20):
			i = i+1
			try:
				find_by_xpath(".//*[@id='map-system_content']/div[%d]/div/a" %i).send_keys(Keys.ENTER)
				if "base" in driver.current_url:
					driver.execute_script("window.history.go(-1)")
				else:
					try:
						gas = find_by_xpath(".//*[@id='base_resources']/tbody/tr[2]/td/table/tbody/tr/td[2]/div/table/tbody/tr[2]/td[2]").text
						metal = find_by_xpath(".//*[@id='base_resources']/tbody/tr[2]/td/table/tbody/tr/td[2]/div/table/tbody/tr[1]/td[2]").text
						specs = find_by_xpath(".//*[@id='astro_specs']").text
						bookmark(specs, int(metal), int(gas))
					except:
						pass
						
						
			except: 
				break
			try:
				find_by_xpath(".//*[@id='background-content']/center/b/a[3]").send_keys(Keys.ENTER)
			except:
				pass
		try:
			find_by_xpath(".//*[@id='background-content']/center/b/a[2]").send_keys(Keys.ENTER)
		except:
			pass
			
		
def click_units():
	click_empire()
	find_by_xpath(".//*[@id='empire-units']/tbody/tr/td[2]/a").send_keys(Keys.ENTER)
	global dict_units
	units = find_by_xpath(".//*[@id='empire_units_units']/tbody/tr[2]/td/table/tbody/tr/td[2]").text
	unit = units.splitlines()
	for i in range(len(unit)):
		print(unit[i])
		#fword = unit[i].partition(' ')[0]
		unitsplit = unit[i].split(" ")
		print(len(unitsplit))
		try:
			if len(unitsplit) <= 10:
				quant = int(unitsplit[1]) + int(unitsplit[4])
				fword = unitsplit[0]
				dict_units[fword] = quant
				print ("dict['%s']: " %fword, dict_units[fword])
				print(fword)
			if len(unitsplit) == 11:
				quant = int(unitsplit[2]) + int(unitsplit[5])
				fword = unitsplit[0]
				dict_units[fword] = quant
				print ("dict['%s']: " %fword, dict_units[fword])
				print(fword)
		except:
			pass
					

name = ""
email = ""
pas = "testtest"
def get_name():
	driver.get("http://random-name-generator.info/random/?n=10&g=1&st=2")
	temp = find_by_xpath(".//*[@id='main']/div[3]/div[2]/ol/li[1]")
	global name
	name = temp.text
	name = name.replace(" ", "")
	return name

def get_email():
	
	get_name()
	driver.get("https://temp-mail.org/en/")
	email = find_by_xpath(".//*[@id='mail']").get_attribute('value')
	print(email)
	return email
	
def fill_reg_form():
	driver.get("http://alpha.astroempires.com/register.aspx")
	find_by_xpath(".//*[@id='registration-inside']/div[2]/div[2]/form/table/tbody/tr[2]/td[2]/input").send_keys(name)
	find_by_xpath(".//*[@id='registration-inside']/div[2]/div[2]/form/table/tbody/tr[4]/td[2]/input").send_keys(email)
	find_by_xpath(".//*[@id='registration-inside']/div[2]/div[2]/form/table/tbody/tr[7]/td[2]/input").send_keys(pas)
	code = solveCode()
	try:
		print("need code")
		find_by_xpath('//*[@id="registration-inside"]/div[2]/div[2]/form/table/tbody/tr[12]/td[2]/input').send_keys(code)
	except:
		pass
	find_by_xpath("//select[@name='country']/option[text()='United States']").click()
	sumbit = ""
	try:
		sumbit = find_by_xpath('//*[@id="registration-inside"]/div[2]/div[2]/form/table/tbody/tr[16]/td/input')
	except:
		pass
	try:
		sumbit = find_by_xpath('//*[@id="registration-inside"]/div[2]/div[2]/form/table/tbody/tr[13]/td/input')
	except:
		pass
	driver.execute_script("arguments[0].click();",sumbit)	
	try:
		error = find_by_xpath('//*[@id="registration-inside"]/div[2]/div[2]/form/table/tbody/tr[12]/td[3]').text
		print("is error")
		if error == "Incorrect":
			print("yup it's fucked")
			fill_reg_form()
	except:
		pass
			
def make_acc():
	global email
	email = get_email()
	fill_reg_form()
	driver.get("https://temp-mail.org/en/")
	driver.execute_script("arguments[0].click();", find_by_xpath(".//*[@id='click-to-refresh']"))
	clk = 10
	t = 0
	for i in range(clk):
		print(t)
		time.sleep(5)
		#print(driver.page_source)
		if "alpha" in driver.current_url:
			break
		try:
			aa = find_by_xpath("./td")
			print(aa)
		except:
			pass
		a = 1
		while True:
			try:
				link = find_by_xpath(".//*[@id='mails']/tbody/tr[%d]/td[2]/a" %a)
				a = a + 1
				if "Account" in link.text:
					print("inside")
					link.send_keys(Keys.ENTER)
					driver.execute_script("arguments[0].click();",link)
					break
			except:
				break
		try:
			print("second")
			a = find_by_xpath("html/body/div[1]/div/div/div[2]/div/div/div[4]/table/tbody/tr[1]/td/table/tbody/tr[2]/td[2]/p/font/a")
			driver.execute_script("arguments[0].click();",a)
			t = 1
			print(t)
		except:
			pass
		try:
			driver.execute_script("arguments[0].click();",find_by_xpath('//*[@id="background-content"]/div/div/div[2]/div[2]/center/form[1]/input[1]'))
		except:
			pass
		try:
			find_by_xpath("//select[@name='galaxy']/option[text()='alpha-05']").click()
		except:
			pass
		try:
			driver.execute_script("arguments[0].click();",find_by_xpath(".//*[@id='background-content']/div/div/div[2]/div[2]/center/form[2]/input[1]"))
		except:
			pass
			
	
def get_tech():
	click_empire()
	find_by_xpath(".//*[@id='empire-technologies']/tbody/tr/td[2]/a").send_keys(Keys.ENTER)
	i = 2
	while i < 18:
		print(i)
		tech_na = find_by_xpath(".//*[@id='empire_technologies']/tbody/tr[2]/td/table/tbody/tr/td[2]/div/table/tbody/tr[%d]/td[1]/div[1]" %i).text
		tech_name = tech_na.split(" ")
		tech_level = find_by_xpath(".//*[@id='empire_technologies']/tbody/tr[2]/td/table/tbody/tr/td[2]/div/table/tbody/tr[%d]/td[5]" %i).text
		print(tech_name[0])
		dict_tech[tech_name[0]] = int(tech_level)
		print ("dict['%s']: " %tech_name[0], dict_tech[tech_name[0]])
		i = i + 1
	unlocked()

def move_one_OS():
	find_by_xpath(".//*[@id='move']/tbody/tr/td[2]/a").send_keys(Keys.ENTER)
	find_by_xpath(".//*[@id='quantOutpost Ship']").send_keys('1')
	find_by_xpath(".//*[@id='move_fleet_form']/table[3]/tbody/tr/td[4]/small/a[1]").send_keys(Keys.ENTER)
	find_by_xpath(".//*[@id='move_fleet_form']/center/input").send_keys(Keys.ENTER)
	delete_bookmark()
	
def find_OS():
	click_fleets()
	try:
		temp = find_by_xpath(".//*[@id='fleets-list']/tbody/tr[2]/td/table/tbody/tr/td[2]/div/table/tbody").text
		length = temp.splitlines()
	except:
		pass
	try:
		for i in range(len(length)+1):
			i = i+1
			find_by_xpath(".//*[@id='fleets-list']/tbody/tr[2]/td/table/tbody/tr/td[2]/div/table/tbody/tr[%d]/td[1]/a" %i).send_keys(Keys.ENTER)
			txtbody = find_by_xpath('//*[@id="fleet_overview"]/tbody/tr[2]/td/table/tbody').text
			fline = txtbody.splitlines()
			for i, x in enumerate(fline):
				if "Outpost" in x:
					build_base()
					return
	except:
		pass
				
def findCredits():
	credits = find_by_xpath(".//*[@id='main-header-infobox_content']/tbody/tr[2]/td[3]/table/tbody/tr/td[2]").text
	return credits	
		
def build_base():
	find_by_xpath(".//*[@id='build_base']/tbody/tr/td[2]/a").send_keys(Keys.ENTER)
	try:
		global bases
		name = bases + 1
		find_by_xpath(".//*[@id='background-content']/table[4]/tbody/tr[2]/td/table/tbody/tr/td[2]/div/center/form/input[1]").send_keys(name)
		driver.execute_script("arguments[0].click();", find_by_xpath(".//*[@id='background-content']/table[4]/tbody/tr[2]/td/table/tbody/tr/td[2]/div/center/form/input[2]"))
		return
	except:
		move_one_OS()
				
def delete_bookmark():
	find_by_xpath(".//*[@id='bookmarks']/tbody/tr/td[2]/a").send_keys(Keys.ENTER)
	find_by_xpath(".//*[@id='bookmarks-table']/tbody/tr[2]/td/table/tbody/tr/td[2]/div/form/table/tbody/tr[1]/td[5]/a").send_keys(Keys.ENTER)
			

def inQueue():
	i = 0
	y = 0
	while 1:
		i = i+1
		print(i)
		try:
			q = find_by_xpath(".//*[@id='base-queue_content']/form/table/tbody/tr[%d]/td[1]" %i).text
			print(q)
			global queues
			if(len(q) < 30):
				if q != "":
					if "Barracks" in q: 
						pass
					else:
						queues.append(q)
		except:
			y = y+1
			
		if y == 1:
			break
			
def apply_guild():
	driver.get("http://alpha.astroempires.com/guild.aspx?guild=31&action=request_join")
	driver.execute_script("arguments[0].click();", find_by_xpath('//*[@id="background-content"]/div[2]/div/div[2]/div[2]/div/div/div[2]/center/form/input[1]'))
		
class Base:
	structs = ""
	Solar = 0
	gas = 0
	def __init__(self,dict):
		self.structs = dict
		

def solveCode():
	code = ""
	try:
		tt = find_by_xpath('//*[@id="registration-inside"]/div[2]/div[2]/form/table/tbody/tr[11]/td[2]/img')
		src = tt.get_attribute('src')
		urllib.request.urlretrieve(src, "test.png")
		im = Image.open("test.png")
		code = getCode(im)
	except:
		pass
	print("go code")
	return code

def getCode(im):
	print("we code")
	temp = im
	x = 0
	w = 1
	h = 0.3125
	count = 0
	nr1 = []
	nr2 = []
	nr3 = []
	nr4 = []
	nr5 = []
	temp = temp.filter(ImageFilter.SHARPEN)
	temp = temp.filter(ImageFilter.SMOOTH_MORE)
	temp = temp.filter(ImageFilter.MedianFilter(size=1))
	temp = temp.filter(ImageFilter.EDGE_ENHANCE_MORE)
	temp = temp.filter(ImageFilter.SMOOTH_MORE)
	temp = temp.filter(ImageFilter.MedianFilter(size=3))
	for x in range(160):
		x = x+1
		print(x)
		tempw = math.floor(w*x)
		temph = math.floor(h*x)
		if temph == 0:
			temph = temph + 1
		if tempw == 0:
			tempw = tempw + 1
		int(tempw)
		int(temph)
		print(tempw)
		print(temph)
		im = temp.resize((tempw, temph), Image.LANCZOS)
		try:
			text = pyt.image_to_string(im)
		except:
			pass
		try:
			if text.isdigit():
				l = list(text)
				print(l)
				i = 0
				for i, item in enumerate(l):
					int(l[i])
					if l[i].isdigit():
						index = l[i]
						if i == 0:
							nr1.append(item)
						if i == 1:
							nr2.append(item)
						if i == 2:
							nr3.append(item)
						if i == 3:
							nr4.append(item)
						if i == 4:
							nr5.append(item)
							break
					i = i + 1
		except:
			pass
	full = ""
	count = 0
	index1 = 0
	index2 = 0
	index3 = 0
	index4 = 0
	index5 = 0
	for i, item in enumerate(nr1):
		if nr1.count(item) > count:
			count = nr1.count(item)
			index1 = item
	count = 0
	for i, item in enumerate(nr2):
		if nr2.count(item) > count:
			count = nr2.count(item)
			index2 = item
	count = 0
	for i, item in enumerate(nr3):
		if nr3.count(item) > count:
			count = nr3.count(item)
			index3 = item
	count = 0
	for i, item in enumerate(nr4):
		if nr4.count(item) > count:
			count = nr4.count(item)
			index4 = item
	count = 0
	for i, item in enumerate(nr5):
		if nr5.count(item) > count:
			count = nr5.count(item)
			index5 = item

	full = index1 + index2 + index3 + index4 + index5
	most = int(full)
	
	return most
	
startDriver()
i = False
while 1:
	if i:
		logged()
	else:
		log()
		i = True
	time.sleep(600)
	i = True

