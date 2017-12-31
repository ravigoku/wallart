import requests
import shutil
import regex as re

url = 'https://i.redditmedia.com/b3jpbJu_4_bgAfq8GZF4a6imSlafTE5ROQ1BOEJa90Q.jpg?s=3b86cac1fe038cf5fcb60ab40ba84b1e'
reg = re.compile(r'\.jpg|\.jpeg|\.tiff|\.tif|\.gif|\.bmp|\.png|\.bpg')
extension = reg.search(url)

r = requests.get(url,stream=True)
path = 'C:\\Users\\inzon_000\\Pictures\\temp'+extension.group()

if r.status_code == 200:
    with open(path,'wb') as f:
        r.raw.decode_content = True
        shutil.copyfileobj(r.raw,f)
