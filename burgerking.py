from bs4 import BeautifulSoup
from urllib.request import urlopen, HTTPCookieProcessor, build_opener, install_opener
from urllib.parse import urlencode
import http.cookiejar
import random
import time


class TellBurgerkingKr:
    def __init__(self):
        self.base_url = "https://kor.tellburgerking.com/"
        cookie_jar = http.cookiejar.CookieJar()
        opener = build_opener(HTTPCookieProcessor(cookie_jar))
        install_opener(opener)

    def parse(self, text):
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
        if param_dict.get('JavaScriptEnabled') is not None:
            param_dict['JavaScriptEnabled'] = '1'
        return (action, param_dict)

    def select_option(self, param_dict):
        for key in param_dict:
            count = len(param_dict[key])
            if count > 0:
                param_dict[key] = param_dict[key][random.randrange(0,count)]

    def parse_code(self, text):
        soup = BeautifulSoup(text, 'html.parser')
        return soup.select('p.ValCode')[0].text

    def get_freeupgrade_code(self, code):
        html = urlopen(self.base_url).read()
        action_url, param_dict = self.parse(html)
        self.select_option(param_dict)
        post_data = urlencode(param_dict).encode('utf-8')
        html = urlopen(self.base_url + action_url, data=post_data).read().decode('utf-8')

        action_url, param_dict = self.parse(html)
        self.select_option(param_dict)
        if len(code) != 16:
            raise Exception('코드 길이가 안맞습니다!')
        start_time = time.time()

        #Make HTTP POST data
        param_dict.update({
            'CN1': code[0:3],
            'CN2': code[3:6],
            'CN3': code[6:9],
            'CN4': code[9:12],
            'CN5': code[12:15],
            'CN6': code[15],
        })

        while True:
            post_data = urlencode(param_dict).encode('utf-8')
            html = urlopen(
                self.base_url + action_url, data=post_data).read().decode('utf-8')
            action_url, param_dict = self.parse(html)
            self.select_option(param_dict)
            if param_dict == {}:
                break

        end_time = time.time()
        print("%s sec elapsed" % (end_time - start_time))

        return self.parse_code(html)

    def do_cli(self):
        print ('버거킹 코드 입력(-입력, 공백 없이):')
        while True:
            code = input()
            if len(code) == 16:
                break
            else:
                print('코드 길이가 안맞습니다!')

        print(self.get_freeupgrade_code(code))

if __name__ == "__main__":
    burger_king = TellBurgerkingKr()
    burger_king.do_cli()
