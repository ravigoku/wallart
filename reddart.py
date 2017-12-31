import praw
import regex as re

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
    
    print reddit.user    

auth0 = credentials('C:\\Users\\inzon_000\\Documents\\python\\apiSecrets\\wallart.txt.')

createReddit(auth0)