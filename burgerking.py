from bs4 import BeautifulSoup
from urllib.request import urlopen, HTTPCookieProcessor, build_opener, install_opener
from urllib.parse import urlencode
import http.cookiejar
import sys
import random
import json
import time

"""
returns tuple of (action url, parameter dict)
"""
def parse(text):
    param_dict = {}
    soup = BeautifulSoup(text, 'html.parser')
    for input_item in soup.find_all('input'):
        name = input_item.get("name", None)
        value = input_item.get("value", None)
        if name in param_dict and name is not None:
            param_dict[name].append(value)
        elif name is not None:
            param_dict[name] = [value]
    action = soup.find('form').get('action', None)
    if param_dict.get('JavaScriptEnabled') != None:
            param_dict['JavaScriptEnabled'] = '1'
    return (action, param_dict)

def select_option(param_dict):
    for key in param_dict:
        count = len(param_dict[key])
        if count > 0:
            param_dict[key] = param_dict[key][random.randrange(0,count)]

def parse_code(text):
    soup = BeautifulSoup(text, 'html.parser')
    return soup.select('p.ValCode')[0].text

baseURL = "https://kor.tellburgerking.com/"

if __name__ == "__main__":
    cj = http.cookiejar.CookieJar()
    opener = build_opener(HTTPCookieProcessor(cj))
    install_opener(opener)
    html = urlopen(baseURL).read()
    a, d = parse(html)
    select_option(d)
    post_data = urlencode(d).encode('utf-8')
    html = urlopen(baseURL + a, data=post_data).read().decode('utf-8')

    a, d = parse(html)
    select_option(d)
    
    #Input burgerking code
    print ('버거킹 코드 입력(-입력, 공백 없이):')
    while True:
        code = input()
        if len(code) == 16:
            break
        else:
            print ('코드 길이가 안맞습니다!')

    start_time = time.time()
    
    #Make HTTP POST data
    d.update({
        'CN1': code[0:3],
        'CN2': code[3:6],
        'CN3': code[6:9],
        'CN4': code[9:12],
        'CN5': code[12:15],
        'CN6': code[15],
    })

    while True:
        post_data = urlencode(d).encode('utf-8')
        html = urlopen(
            baseURL + a, data=post_data).read().decode('utf-8')
        a, d = parse(html)
        select_option(d)
        if d == {}:
            break
    
    end_time = time.time()
    print ("%s sec elapsed" % (end_time - start_time))

    print(parse_code(html))


