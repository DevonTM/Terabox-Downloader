import requests
import json
import os
import re
import subprocess

currentFile = __file__
realPath = os.path.realpath(currentFile)
dirPath = os.path.dirname(realPath)
dirName = os.path.basename(dirPath)
aria2c = dirPath + "/binaries/aria2c.exe"
cookies_file = dirPath + '/cookies.txt'


def parseCookieFile(cookiefile):
    cookies = {}
    with open(cookies_file, 'r') as fp:
        for line in fp:
            if not re.match(r'^\#', line):
                lineFields = line.strip().split('\t')
                cookies[lineFields[5]] = lineFields[6]
    return cookies


cookies = parseCookieFile('cookies.txt')
print('Cookies Parsed')


inp = input('Enter the Link: ')
dom = inp.split("/")[2]
typ = inp.split("/")[-1].split("?")[0]
fxl = inp.split("=")

if typ == "link":
    key = fxl[-1]
    URL = f'https://{dom}/share/list?app_id=250528&shorturl={key}&root=1'
elif typ == "videoPlay":
    key = fxl[1].split("&")[0]
    dir = fxl[2].split("&")[0]
    name = fxl[4]
    URL = f'https://{dom}/share/list?app_id=250528&shorturl={key}&path={dir}%2F{name}&root=1'

header = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': f'https://{dom}/sharing/{typ}?surl={key}',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:110.0) AppleWebKit/605.1.15 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/605.1.15'
}

resp = requests.get(url=URL, headers=header, cookies=cookies).json()['list'][0]
filename = resp['server_filename']
dlink = resp['dlink']
    
subprocess.run([aria2c,'-o' + filename, '--console-log-level=warn', '-x 16',
               '-s 16', '-j 16', '-k 1M', '--file-allocation=none', dlink])
