import requests
s = requests.Session()

proxy = 'socks5://127.0.0.1:1080'
PROXY_DICT = {'http': f'{proxy}', 'https': f'{proxy}'}
header = {"Content-Type": "application/json"}

r = s.get('http://ifcfg.me', proxies=None, headers=header)
print(r.text)
s.close()

