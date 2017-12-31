import praw
import regex as re
from pprint import pprint
import json
import requests



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

auth0 = credentials('C:\\Users\\inzon_000\\Documents\\python\\apiSecrets\\wallart.txt.')
reddit = createReddit(auth0)

#subreddit = reddit.subreddit('Showerthoughts')

#NSFW Results?

r = requests.get(r'http://reddit.com/user/ravigoku/comments/.json') # response object
data = r.json()
print data.keys()
print r.text
