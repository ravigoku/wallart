import praw
import regex as re
from pprint import pprint
import json
import requests
import time

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
        
        if (width > 1024 and float(width)/height > 1.2):
            print datum['data']['title']
            print "width: " + str(width) + " height: " + str(height) + " ratio: " + str(float(width)/height)
            print
        
# Requirements text link_flair_text: "Artwork "

#print data['data']['children'][0]
