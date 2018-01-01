import praw
import regex as re
from pprint import pprint
import json
import requests
import time
import random
from _ast import Num
import shutil
import ctypes
import subprocess

def credentials(textfile):
    f = open(textfile)
    words = f.read()
    credRegex= re.compile(r'username = ([a-zA-Z0-9._%+-]+)\npassword = ([a-zA-Z0-9._%+-]+)\nclient_id = ([a-zA-Z0-9._%+-]+)\nclient_secret = ([a-zA-Z0-9._%+-]+)')
    result = credRegex.search(words)
    
    return {'username':result.group(1), 'password':result.group(2), 
            'client_id':result.group(3), 'client_secret':result.group(4)}
   
def createReddit(dictionary):
    reddit = praw.Reddit(client_id = dictionary['client_id'],
            client_secret = dictionary['client_secret'],
            password = dictionary['password'],
            user_agent = 'WallArt by /u/ravigoku',
            username = dictionary['username'])
    
    #print reddit.user.me()
    return reddit  

def pullsubreddit(url):
    r = requests.get(url) # response object
    data = json.loads(r.text)
    
    while 'message' in data.keys():
        time.sleep(2)
        r = requests.get(r'https://www.reddit.com/r/Art/.json') # response object
        data = json.loads(r.text)
    return r
    
wallpapers = list()
auth0 = credentials('C:\\Users\\inzon_000\\Documents\\python\\apiSecrets\\wallart.txt.')
reddit = createReddit(auth0)

#NSFW Results?
r = pullsubreddit(r'https://www.reddit.com/r/Art/.json')
data = json.loads(r.text)
print data.keys()
print r.text
    # we can look through the result using http://jsoneditoronline.org/
    # sometimes error {"message": "Too Many Requests", "error": 429}

for datum in data['data']['children']:
    if (datum['data']['link_flair_text'] == 'Artwork' and 'preview' in datum['data']):
        images = datum['data']['preview']['images']
        width = images[0]['source']['width']
        height = images[0]['source']['height']
        
        if (width > 1024 and float(width)/height > 1.3):
            title = datum['data']['title']
            picture = images[0]['source']['url']
            wallpapers.append({'title':title,'picture':picture})
            print title
            print picture
            print str(float(width)/height)
            print 
            
num = random.randint(0,len(wallpapers)-1)
print "number: " + str(num)

choice = wallpapers[num]
url= choice['picture']

reg = re.compile(r'\.jpg|\.jpeg|\.tiff|\.tif|\.gif|\.bmp|\.png|\.bpg')
extension = reg.search(url)

r = requests.get(url,stream=True)
path = 'C:\\Users\\inzon_000\\Pictures\\temp1'+extension.group()

if r.status_code == 200:
    with open(path,'wb') as f:
        r.raw.decode_content = True
        shutil.copyfileobj(r.raw,f)

check = subprocess.call('C:\\Program Files (x86)\\Easy2Convert Software\\JPG to BMP\\jpg2bmp.exe -i C:\\Users\\inzon_000\\Pictures\\temp1.jpg - o C:\\Users\\inzon_000\\Pictures\\')
SPI_SETDESKWALLPAPER = 20
ctypes.windll.user32.SystemParametersInfoA(SPI_SETDESKWALLPAPER, 0, path, 0)
# only works with bmp files, so we need to find another way to set wallpaper


check = subprocess.call('reg add "HKEY_CURRENT_USER\\Control Panel\\Desktop" /v Wallpaper /t REG_SZ /d C:\\Users\\inzon_000\\Pictures\\temp1.bmp /f')
print("Done with reg add")
time.sleep(1)
check = subprocess.call('rundll32.exe user32.dll, UpdatePerUserSystemParameters')
print("Done with refresh")
# Requirements text link_flair_text: "Artwork "
 
#print data['data']['children'][0]
