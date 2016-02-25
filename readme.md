# TellBurgerkingKr 설문조사 Python 자동화 스크립트

버거킹에서 구매하면 주는 설문조사 코드를 이용하여 무료 세트업그레이드 쿠폰을 자동으로 얻는 코드를 작성하였습니다.

# CODE

```Python
#-*- coding: utf-8 -*-
import urllib
import urllib2
import cookielib
from bs4 import BeautifulSoup

#Returns input_name, input_alias, input_choices
def parse_input_item(html_str):
	_soup = BeautifulSoup(html_str, "html.parser")
	try:
		_input_action = _soup.select('form')[0].get('action')
	except IndexError:
		_input_action = ""
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

	# print _input_name
	# print _input_alias
	# print _input_choices

	#Make HTTP POST data
	_payload = {}
	for each_input_name in _input_name:
		if _input_choices[each_input_name][0] != None:
			if len(_input_choices[each_input_name]) < 2:
				_payload[each_input_name] = _input_choices[each_input_name][0].encode('utf-8')

	#Change JS setting
	if _payload.get('JavaScriptEnabled') != None:
		_payload['JavaScriptEnabled'] = '1'

	return _payload, _input_action



cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
urllib2.install_opener(opener)

#Find form action link
html = urllib2.urlopen('https://kor.tellburgerking.com/')

#Make HTTP POST data
payload, input_action = parse_input_item(html)
data = urllib.urlencode(payload)

#Send HTTP POST request
req = urllib2.Request('https://kor.tellburgerking.com/' + input_action, data)
html = urllib2.urlopen(req)

#Make HTTP POST data
payload, input_action = parse_input_item(html)

#Input burgerking code
print u'버거킹 코드 입력(-입력, 공백 없이):',
while True:
	code = raw_input()
	if len(code) == 16:
		break
	else:
		print u'코드 길이가 안맞습니다!'

#Make HTTP POST data
payload.update({
	'CN1' : code[0:3],
	'CN2' : code[3:6],
	'CN3' : code[6:9],
	'CN4' : code[9:12],
	'CN5' : code[12:15],
	'CN6' : code[15],
})
data = urllib.urlencode(payload)

#Send HTTP POST request
req = urllib2.Request('https://kor.tellburgerking.com/' + input_action, data)
html = urllib2.urlopen(req).read()

i = 0
while True:
	#Make HTTP POST data
	payload, input_action = parse_input_item(html)
	if len(payload) < 1 or input_action == "":
		break
	data = urllib.urlencode(payload)

	#Send HTTP POST request
	req = urllib2.Request('https://kor.tellburgerking.com/' + input_action, data)
	html = urllib2.urlopen(req).read()
	i += 1

soup = BeautifulSoup(html, "html.parser")
code = soup.select('p.ValCode')[0].text
print code
raw_input()

```