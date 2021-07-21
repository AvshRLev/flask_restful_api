import requests

BASE = "http://127.0.0.1:5000/"

response = requests.put(BASE + "video/1", {"likes": 10})
# response_post = requests.post(BASE + "helloworld")
print(f"{response.json()}")