import csv
import requests
import requests
from isbnlib import meta
from isbnlib.registry import bibformatters

path = './data_file.csv'

class monModelLivre:

    # def sesPropriétés
    # Titre
    # Image
    # Description

monTableauDeLivres = []

def getGoogleInfo(isbn):
    query = 'isbn : '+isbn
    params = {'q' : query}
    url = r'https://www.googleapis.com/books/v1/volumes'
    response = requests.get(url, params=params)
    return response.json()

def getBnfInfo(isbn):
    SERVICE = 'bnf'
    bibtext = bibformatters['bibtext']
    print(bibtext(meta(isbn, SERVICE)))
   
def getOpenLibrary(isbn):
    url = 'https://openlibrary.org/api/books?bibkeys=ISBN:'+isbn+'&callback=mycallback'
    payload = {}
    headers = {}
    response = requests.request('GET', url, headers=headers, data=payload)
    return response.text

with open(path, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        print(getGoogleInfo(row['ISBN13']))
        print(getOpenLibrary(row['ISBN13']))
        try:
            getBnfInfo(row['ISBN13'])
        except AttributeError:
            print('Nothing found from BNF')

        #Faire le travail de comparaison en fonction des résultats
        #Créer l'objet livre