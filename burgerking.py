#-*- coding: utf-8 -*-
import urllib
import urllib2
import cookielib
from bs4 import BeautifulSoup

#Returns input_name, input_alias, input_choices
def parse_input_item(html_str):
	_soup = BeautifulSoup(html_str, "html.parser")
	_input_list = _soup.select('input')
	_input_name = []
	_input_alias = {}
	_input_choices = {}

	for eachinput in _input_list:
		try:
			_input_name.index(eachinput.get('name'))
		except ValueError:
			_input_name.append(eachinput.get('name'))
			_input_alias[eachinput.get('name')] = [eachinput.get('alt')]
			_input_choices[eachinput.get('name')] = [eachinput.get('value')]
		else:
			_input_alias[eachinput.get('name')].append(eachinput.get('alt'))
			_input_choices[eachinput.get('name')].append(eachinput.get('value'))

	return _input_name, _input_alias, _input_choices
		



cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
urllib2.install_opener(opener)

#Find form action link
html = urllib2.urlopen('https://kor.tellburgerking.com/Index.aspx?c=330406')
soup = BeautifulSoup(html, "html.parser")
form = soup.select('form')[0]['action']

#Make HTTP POST data
payload = {
	'JavaScriptEnabled' : '1',
	'FIP': 'True',
	'AcceptCookies' : 'Y',
	'NextButton' : u'계속'
}
data = urllib.urlencode(payload)

#Send HTTP POST request
req = urllib2.Request('https://kor.tellburgerking.com/' + form, data)
html = urllib2.urlopen(req)
soup = BeautifulSoup(html, "html.parser")
form = soup.select('form')[0]['action']

#Input burgerking code
print '버거킹 코드 입력(-입력, 공백 없이):',
while True:
	code = raw_input()
	if len(code) == 16:
		break
	else:
		print '코드 길이가 안맞습니다!'

#Make HTTP POST data
payload = {
	'JavaScriptEnabled' : '1',
	'FIP' : 'True',
	'CN1' : code[0:2],
	'CN2' : code[3:5],
	'CN3' : code[6:8],
	'CN4' : code[9:11],
	'CN5' : code[12:14],
	'CN6' : code[15],
	'NextButton' : u'계속'
}
data = urllib.urlencode(payload)

#Send HTTP POST request
req = urllib2.Request('https://kor.tellburgerking.com/' + form, data)
html = urllib2.urlopen(req)
soup = BeautifulSoup(html, "html.parser")
form = soup.select('form')[0]['action']

#주문유형?
#Make HTTP POST data
payload = {
	'R001000': '1', #내점 : 1, #takeout : 2
	'IoNF' : '2',
	'PostedFNS' : 'S001000|R001000'
}
data = urllib.urlencode(payload)

#Send HTTP POST request
req = urllib2.Request('https://kor.tellburgerking.com/' + form, data)
html = urllib2.urlopen(req)
soup = BeautifulSoup(html, "html.parser")
form = soup.select('form')[0]['action']

#방문자수
#Make HTTP POST data
payload = {
	'R002000': '1', #1, 2, 3, 4 : 인원수
	'IoNF' : '2',
	'PostedFNS' : 'R002000'
}
data = urllib.urlencode(payload)

#Send HTTP POST request
req = urllib2.Request('https://kor.tellburgerking.com/' + form, data)
html = urllib2.urlopen(req)
soup = BeautifulSoup(html, "html.parser")
form = soup.select('form')[0]['action']

#12세 미만?
#Make HTTP POST data
payload = {
	'R003000': '1', #1:Y, 2:N
	'IoNF' : '2',
	'PostedFNS' : 'R003000'
}
data = urllib.urlencode(payload)

#Send HTTP POST request
req = urllib2.Request('https://kor.tellburgerking.com/' + form, data)
html = urllib2.urlopen(req)
soup = BeautifulSoup(html, "html.parser")
form = soup.select('form')[0]['action']
