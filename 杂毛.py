'''
BY:YourAhTzu
自己内置Cookie和X-CSRF-TOKEN
'''
import requests
url = 'https://www.lkdns.top/home'
headers = {
    'Host': 'www.lkdns.top',
    'Connection': 'keep-alive',
    'Content-Length': '12',
    'Accept': '*/*',
    'X-CSRF-TOKEN': '',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 12; RMX3562 Build/SP1A.210812.016) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.98 Mobile Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'https://www.lkdns.top',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://www.lkdns.top/home',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cookie': ''
}

payload = {'action': 'sign'}

response = requests.post(url, headers=headers, data=payload)

data = response.json()

if data['status'] == 0:
    print("签到成功")
elif data['status'] == -1:
    print("已签到")