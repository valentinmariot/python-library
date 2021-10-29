# ////////////////////////////////////////////////// #

# Bonjour Monsieur, 

# Ce binôme est composé de Madame Carine Grisot et de moi-même.
# Afin de contextualiser, n'ayant eu l'occasion de travailler avec cet outil auparavent, cet exercice fût notre première approche du language Python. 

# N'ayant pas encore pris en main toutes les subtilités de ce dernier, notre rendu sera majoritairement commenté afin de vous détailler au mieux notre approche ainsi que la logique que nous avions choisi d'appliquer dans ce TD. 
# Voici donc notre devoir : 


# Notre roadmap se voulait telle que :

# -- SOURCE DE DONNÉES --
# 1- Retrait des sauts de ligne au sein de 'fichierSource.csv':
#     • Définir une variable globale data=[] qui réceptionnera de futures informations,
#     • Ovrir le fichier 'fichierSource.csv' en mode lecture/écriture 'r+',
#     • Concaténer les données à l'aide de .join(),
#     • Utiliser la fonction isspace() afin de détecter les lignes constituées d'un espace,
#     • Si une ligne est un whitespace alors on la supprime,
#     • Passer les informations à notre variable data=[] afin de les stocker,
#     • Fermer le fichier.

# 2- Réécriture du fichier avec le bon format de données : 
#     • Réouvrir le fichier en mode écriture 'w',
#     • Réinjecter les données contenues dans data=[] afin d'obtenir le bon format.

# 3- BONUS - Vérifier que les ISBN sont conformes :
#     Il est possible de vérifier l'authenticité d'une ISBN à l'aide d'un simple calcul. En effet, il suffit d'additionner chaque chiffre par la valeur de sa place en décrémentant de gauche à droit (premier caractère x10 + second caractère x9 + troisième caractère x8 + ... ). Dans le cas où un ISBN se termine par un 'X', il nous faut remplacer celui-ci par un 10 (le X représentant un chiffre romain qui ne pourrait être écrit 10 sinon l'ISBN serait composé de 11 caractères). Le résultat de cette addition doit ensuite être divisé par 11. Si le modulo renvoie 0 alors l'ISBN est bon. Mais tout ça, on se doute que vous le savez déjà ! 
#     Avant d'effectuer ce calcul, nous aurions utilisé une RegEx afin de vérifier sa conformité. L'expression régulière en question se présenterait de la sorte : ' ^\d{9}[\d|X]$ '
    
#     Cette vérification aurait été faite après la vérification des whitespace dans la première boucle de notre code afin d'éviter les répétitions inutiles de fonctions.


# -- APPELS API -- 
# 1- Appel des API :
#     Nous ayant fournis cette partie du code, nous avons analysé celui-ci afin de comprendre comment naviguer dans les fichiers JSON et sélectionner les keys pour en extraire les valeurs qui seraient placées dans des variables. Pour cette partie, nous avions retenu cette idée :
#     • Récuperer la valeur de chaque informations désirées dans toutes les API, 
#     • Tester si certaines informations sont bien renseignées à l'aide d'un `try: except: else:` (ex: il n'y a pas systématiquement de subtitle),
#     • Si une valeur n'existe pas alors on attribue " " à la place,
#     • Passer ces valeurs dans un tableau, à 2 niveaux, du nom de l'information (ex : titres=[[titregoogle1, titreopenlib1, titrebnf1],[titregoogle2, titreopenlib2, titrebnf2],[...]] | autheurs=[[...],[...]] ),
#     • Compter le nombre d'occurence dans chaque tableau de tableau via la méthode collections.counter(),
#     • Recuperer la valeur avec le plus grand nombre d'occurence et le mettre dans un objet Livre,
#     • Injecter chaque Livre dans le tableau Livres.

# 2- BONUS - Optimiser les appels API en utilisant les codes de retour :
#     Si nous avons bien saisi cette partie, response.status_code nous permet de tester l'API et vérifier que l'on communique bien avec elle (à l'aide d'un code 200) et renvoie une erreur 404 si aucune connexion est possible. Cette vérification aurait donc été une condition, à l'appel d'une API, permettant ou non par la suite le passage des requêtes contenant les ISBN de fichierSource.csv . Là encore, selon nous, un try: aurait pû permettre de répondre au besoin.

# -- MySql --
#     Afin de faire communiquer Python avec un base de données MySql, il faut au préalable installer le module connector via la commande `pip install mysql-connector-python`
#     Proche d'une requête PDO en PHP, Python requiere plusieurs paramètres afin de se connecter à une base de données : l'host, le nom de la base de données, l'identifiant de connexion et son mot de passe.
#     Une fois la connexion faite, on peut passer des requêtes SQL afin de créer les tables, ajouter des informations, en supprimer, etc. 
#     Un autheur pouvant être à l'origine de plusieurs ouvrages, il nous aurait fallu créer une table Livres, une table Autheurs ainsi qu'une table relationnelle qui lierait l'id.autheur à ses id.livre.
#     Pour vérifier qu'un livre est déjà enregistré au sein de la base de données, on pourrait récupérer les ISBN de la BDD afin de les mettre en comparaison avec les ISBN de notre fichier. Si un ISBN est déjà présent, une requête UPDATE-SET où l'ISBN est === à celui passé par la variable est alors instanciée.


# -- Conclusion --
#     Cet exercice fût très intéressant car, bien que nous soyons loin de répondre aux attentes, nous avons appris beaucoup de choses sur ce langage qui nous était alors jusque là inconnu. 

# Voici maintenant notre travail.

#                                                        Carine Grisot & Valentin Mariot
# ////////////////////////////////////////////////// #
# ////////////////////////////////////////////////// #

# La partie deu code que vous nous avez fournis, agrémenté de notre solution de traitement des espaces dans le fichier .csv

import requests
import isbnlib
from isbnlib.registry import bibformatters
from isbnlib import meta

# print(isbnlib.cover(isbn))


path = 'fichierSource.csv'
datas = []
with open(path, 'r+') as file:
        datas = "".join(line for line in file if not line.isspace())
        file.close()

with open(path, 'w') as file:
        file.write(datas)
        file.close()
try:

    with open(path, 'r+') as file:
        for ligne in file:
            cleaned = ligne.rstrip()
            #Open Library
            print("OpenLibrary")
            url = "https://openlibrary.org/api/books?bibkeys=ISBN:"+cleaned+"&callback=mycallback"
            payload = {}
            headers = {}
            response = requests.request("GET", url, headers=headers, data=payload)
            print(response.text)

            #GoogleBooks
            print("Google Books")
            query = 'isbn:'+cleaned
            params = {"q": query}
            url = r'https://www.googleapis.com/books/v1/volumes'
            response = requests.get(url, params=params)
            print(response.text)
            # data = json.load(response.json())
            # print(response.json()['items'][0]['volumeInfo']['title'])
            # print(data)
           
            #AltMetrics
            print("AltMetrics")
            url = "https://api.altmetric.com/v1/isbn/"+cleaned
            payload = {}
            headers = {}
            response = requests.request("GET", url, headers=headers, data=payload)
            print(response.text)

            SERVICE = "bnf"
            print("BNF")
            # now you can use the service
            isbn = cleaned
            try:
                bibtex = bibformatters["bibtex"]
                print(bibtex(meta(isbn, SERVICE)))
            except AttributeError:
                print("erreur BNF")

            print("Worldcat")
            # now you can use the service
            service = "worldcat"
            isbn = cleaned
            try:
                bibtex = bibformatters["bibtex"]
                print(bibtex(meta(isbn, SERVICE)))
            except AttributeError:
                print("erreur Worldcat")


except FileNotFoundError:
    print("Fichier introuvable")
except IOError:
    print("erreur d’ouverture")


# ////////////////////////////////////////////////// # 
# ////////////////////////////////////////////////// # 

# Nos test effectués sur l'API Google (dans un fichier annexe): 

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
