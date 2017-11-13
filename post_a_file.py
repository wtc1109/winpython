import requests
import json

url = "http://192.168.7.19/cgi-bin/download.py"
files = {"filename":("123.zip", open("d://123/123.zip", "rb"))}
r = requests.post(url=url, files=files)
print r