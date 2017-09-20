import requests
import json

url = "http://192.168.7.185/cgi-bin/update_app.cgi"
files = {"file":("123.zip", open("d://123/123.zip", "rb"))}
r = requests.post(url=url, files=files)
print r