import urllib.request
import json

dtu_url = "http://www.fysik.dtu.dk/Om-DTU-Fysik/Medarbejdere/Alle_medarbejdere?dtulistid=INSTLIST10&fr=1&mr=1000&orgid=10&qt=DtuPersonQuery&types=employee,guest"
trello_url = "https://trello.com/b/1YiAyafj.json"

with urllib.request.urlopen(dtu_url) as response:
   page = bytes.decode(response.read())

with urllib.request.urlopen(trello_url) as response:
    trello_page = bytes.decode(response.read())

start_word = '</svg>'
end_word = '</a>'

names = []

n = 0
while n > -1:
    n = page.find(start_word, n+1)
    m = page.find(end_word, n)
    names.append(page[n + len(start_word)+1:m])
names.pop()

trello = json.loads(trello_page)

amu_row_id = trello['lists'][0]['id']

trello_members = []
for card in trello['cards']:
    if not (card['idList'] == amu_row_id):
        trello_members.append(card['name'])

for name in names:
    if not (name in trello_members):
        print(name + ' is not in Trello')

print('-------------------')

for name in trello_members:
    if not (name in names):
        print(name + ' is not on web page')
