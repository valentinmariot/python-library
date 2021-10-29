import requests
titleGoogle = []
print("Google Books")
query = 'isbn:'+isbn
params = {"q": query}
url = r'https://www.googleapis.com/books/v1/volumes'
response = requests.get(url, params=params)
# print(response.text)
# data = json.load(response.json())
# print(titleGoogle)

googleTitle = response.json()['items'][0]['volumeInfo']['title']
googleAuthors = response.json()['items'][0]['volumeInfo']['authors']
googleDescription = response.json()['items'][0]['volumeInfo']['description']
googlePublisher = response.json()['items'][0]['volumeInfo']['publisher']
googleLanguage = response.json()['items'][0]['volumeInfo']['language']
googleSubtitle = response.json()['items'][0]['volumeInfo']['subtitle']

googleBook =[]

try:
    googleTitle
    googleSubtitle
    googleAuthors
    googleDescription
    googlePublisher
    googleLanguage
except NameError:
    googleTitle = False
    googleSubtitle = False
    googleAuthors = False
    googleDescription = False
    googlePublisher = False
    googleLanguage = False
else:
    googleTitle = True
    googleSubtitle = True
    googleAuthors = True
    googleDescription = True
    googlePublisher = True
    googleLanguage = True

title = googleTitle
subtitle = googleSubtitle
authors = googleAuthors
description = googleDescription
publisher = googlePublisher
language = googleLanguage

googleBook.append({
    'isbn': isbn,
    'title': title,
    'subtitle': subtitle,
    'authors': authors,
    'description': description,
    'publisher': publisher,
    'language': language 
})

print(googleBook)
