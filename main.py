import requests
import re
from bs4 import BeautifulSoup

baseUrl = "https://www.news.maiden-lotb.com/n3/character-en/"
characterBase = requests.post(baseUrl)
characterList = BeautifulSoup(characterBase.text, 'html.parser').find_all(
    'div', attrs={'class': 'ch-icon'})
characterUrlList = [character.a.get('href') for character in characterList]
awakenableCharacterUrlList = []
print(len(characterUrlList))

i = 0
for characterUrl in characterUrlList:

  print('\n======================================\n\n')
  i += 1
  if i == 5:
    break

  response = requests.post(characterUrl, data={})
  data = BeautifulSoup(response.text, 'html.parser')
  character = BeautifulSoup(str(data.find(id='content')), 'html.parser')

  awakenableUrl = character.find('a', attrs={'class': 'awakenable-url'})

  awakenableCharacterUrlList.append(
      awakenableUrl.get('href')) if awakenableUrl else None

  characterName = character.find('h1').text

  print('va')
  characterType = 'Eddie' if (characterName.find('Eddie') or ['Ed Hunter', 'Frankedstein'].index(characterName) >= 0) else 'Ally'

  print("Name: ", characterName)
  print("Class: ", character.find('p', attrs={ 'class': 'disable' }).text)
  print("Style: ", character.find('div', attrs={ 'class': 'ch-description' }).text)
  stats = character.find_all('div', attrs={ 'class': 'ch-max-stat-row' })
  for stat in stats:
      print(stat.find('div', attrs={ 'class': 'max-stat-name' }).text, ": ", stat.find('div', attrs={ 'class': 'max-stat-num' }).text)
  talismanPattern = re.compile("slot_")
  talismanList = character.find_all('img', attrs={ 'src': talismanPattern })
  talismans = ""
  for talisman in talismanList:
    talismans += ("" if talismans == "" else " | ") + str(talisman['src']).replace(".png", "").split('slot_')[1]
  print("Tal slots: ", talismans)
  '''
  skillList = character.find_all('tr', attrs={ 'class': 'skill-table-border-top' })
  for skill in skillList:
    skillName = skill.find_all('p')
    print(skillName[0].text, ": ", skillName[1].text)
  '''