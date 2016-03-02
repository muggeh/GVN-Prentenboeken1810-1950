# Script to create categories on Wikimedia Commons,
# as children of the (parent)cat https://commons.wikimedia.org/wiki/Category:Picture_books_from_Koninklijke_Bibliotheek

# LET OP: Dubbele titels uit de XML/JSON halen, ander gaat het mis tijdens het schrijven van de categorieen (bv. "A is een Aapje" of "Asschepoeter")

#import os, os.path
#import json
import requests
#from bs4 import BeautifulSoup


#Login to the MediaWiki API to write categories to Commons - Code from https://www.mediawiki.org/wiki/API:Edit/Editing_with_Python

username = 'OlafJanssen'
password = '5tgb6yhn'
baseurl = 'https://test.wikipedia.org/w/'

# Login request
payload = {'action': 'query', 'format': 'json', 'utf8': '', 'meta': 'tokens', 'type': 'login'}
r1 = requests.post(baseurl + 'api.php', data=payload)

# login confirm
login_token = r1.json()['query']['tokens']['logintoken']
payload = {'action': 'login', 'format': 'json', 'utf8': '', 'lgname': username, 'lgpassword': password, 'lgtoken': login_token}
r2 = requests.post(baseurl + 'api.php', data=payload, cookies=r1.cookies)

# get edit token2
params3 = '?format=json&action=query&meta=tokens&continue='
r3 = requests.get(baseurl + 'api.php' + params3, cookies=r2.cookies)
edit_token = r3.json()['query']['tokens']['csrftoken']

edit_cookie = r2.cookies.copy()
edit_cookie.update(r3.cookies)

# save action



message1 = 'This is a category that will hold images from Childbook3 [[Category:ParentBookCat]]'
message2 = 'This is a category that will hold images from Childbook2 [[Category:ParentBookCat]]'
message3 = 'This is a category that will hold images from Childbook3 [[Category:ParentBookCat]]'

title1 = "Category:ChildBook1"
title2 = "Category:ChildBook2"
title3 = "Category:ChildBook3"

summary1 = 'Creating Childbook1 category'
summary2 = 'Creating Childbook2 category'
summary3 = 'Creating Childbook3 category'

payload = {'action': 'edit', 'assert': 'user', 'format': 'json', 'utf8': '', 'appendtext': message1,'summary': summary1, 'title': title1, 'token': edit_token}
r4 = requests.post(baseurl + 'api.php', data=payload, cookies=edit_cookie)
print (r4.text)

payload = {'action': 'edit', 'assert': 'user', 'format': 'json', 'utf8': '', 'appendtext': message2,'summary': summary2, 'title': title2, 'token': edit_token}
r4 = requests.post(baseurl + 'api.php', data=payload, cookies=edit_cookie)
print (r4.text)

payload = {'action': 'edit', 'assert': 'user', 'format': 'json', 'utf8': '', 'appendtext': message3,'summary': summary3, 'title': title3, 'token': edit_token}
r4 = requests.post(baseurl + 'api.php', data=payload, cookies=edit_cookie)
print (r4.text)