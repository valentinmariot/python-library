import requests
titleGoogle = []
print("Google Books")
query = 'isbn:'+'2883210322'
params = {"q": query}
url = r'https://www.googleapis.com/books/v1/volumes'
response = requests.get(url, params=params)
# print(response.text)
# data = json.load(response.json())
titleGoogle = response.json()['items'][0]['volumeInfo']['title']
print(titleGoogle)
print(response.json()['items'][0]['volumeInfo']['authors'])
print(response.json()['items'][0]['volumeInfo']['description'])
print(response.json()['items'][0]['volumeInfo']['publisher'])
# print(data)
