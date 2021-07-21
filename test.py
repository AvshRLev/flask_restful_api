import requests

BASE = "http://127.0.0.1:5000/"

data = [
    {"likes": 10, "name": "a clip", "views": 10000},
    {"likes": 11, "name": "a film", "views": 10001},
    {"likes": 12, "name": "a movie", "views": 10002}
]

for i in range(len(data)):
    response = requests.delete(BASE + f"video/{str(i)}")
    print(f"{response.json()}")
input()
# response = requests.delete(BASE + "video/0")
# print(response)
# input()
response = requests.patch(BASE + "video/2", {"views": 1011, "likes": 9})
print(f"{response.json()}")