import requests
import re
from bs4 import BeautifulSoup

baseUrl = "https://www.news.maiden-lotb.com/n3/character-en/"

requestContent = requests.post(baseUrl)
characterList = BeautifulSoup(requestContent.text, 'html.parser').find_all(
    'div', attrs={'class': 'ch-icon'})

characterUrlList = [character.a.get('href') for character in characterList]
awakenableCharacterUrlList = []

listOfEddies = ['Ed Hunter', 'Frankedstein']


for idx, characterUrl in enumerate(characterUrlList):
    print('\n======================================\n')

    if idx >= 3:
        break

    data = BeautifulSoup(requests.post(characterUrl).text, 'html.parser')
    character = BeautifulSoup(str(data.find(id='content')), 'html.parser')
    awakenableUrl = character.find('a', attrs={'class': 'awakenable-url'})

    awakenableCharacterUrlList.append(
        awakenableUrl.get('href')) if awakenableUrl else None

    characterName = character.find('h1').text

    characterType = 'Eddie' if (characterName.__contains__(
        'Eddie') or listOfEddies.__contains__(characterName)) else 'Ally'
    print("Name: ", characterName)
    print("Type: ", characterType)
    star = character.find('div', attrs={'class': 'stars'}).img.get(
        'src').replace('.png', '').split('star0')[1]
    print("Base star: ", star)
    print("Class: ", character.find('p', attrs={'class': 'disable'}).text)
    print("Style: ", character.find(
        'div', attrs={'class': 'ch-description'}).text)

    stats = character.find_all('div', attrs={'class': 'ch-max-stat-row'})
    for stat in stats:
        print(stat.find('div', attrs={'class': 'max-stat-name'}).text,
              ": ", stat.find('div', attrs={'class': 'max-stat-num'}).text)

    talismanPattern = re.compile("slot_")
    talismanList = character.find_all('img', attrs={'src': talismanPattern})
    talismans = ""

    for talisman in talismanList:
        talismans += ("" if talismans == "" else " | ") + \
            str(talisman['src']).replace(".png", "").split('slot_')[1]

    print("Tal slots: ", talismans)
