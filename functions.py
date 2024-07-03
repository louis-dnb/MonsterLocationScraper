import requests
from bs4 import BeautifulSoup

def formatCreatureName(creatureName):
    words = creatureName.split()
    formatted_name = '_'.join([words[0].capitalize()] + [word.lower() for word in words[1:]])
    return formatted_name

def infoFromEditPage(creatureName, sectionNumber):
    url = f"https://runescape.wiki/w/{creatureName}?action=edit&section={sectionNumber}"
    response = requests.get(url)
    if response.status_code != 200:
        print('Failed to retrieve the page. Status code:', response.status_code)
        return None
    
    soup = BeautifulSoup(response.content, 'html.parser')
    textarea = soup.find('textarea', {'id': 'wpTextbox1'})
    if textarea:
        content = textarea.get_text()
        return content
    else:
        return 'Textarea not found.'
    
def findSectionNumber(creatureName):
    url = f'https://runescape.wiki/w/{creatureName}'
    response = requests.get(url)
    if response.status_code != 200:
        print('Failed to retrieve the page. Status code:', response.status_code)
        return None
    
    soup = BeautifulSoup(response.content, 'html.parser')
    a_element = soup.find('a', href='#Locations')
    if a_element:
        li_element = a_element.find_parent('li')
        if li_element:
            classes = li_element.get('class', [])
            for cls in classes:
                if cls.startswith('tocsection-'):
                    tocsection_number = cls.split('-')[-1]
                    return tocsection_number
            print('tocsection number not found in class names.')
        else:
            print('Parent LI element not found.')
    else:
        print('A element with href #Locations not found.')


def cleanLocationName(locationName):
    return locationName.split(']]')[0].split(' {{')[0].strip()

def getMonsterLocationData(content):
    locationData = {}
    lines = content.split('\n')
    currentLocation = None
    currentPlane = 0

    for line in lines:
        if line.startswith('|loc='):
            locationName = cleanLocationName(line.split('=')[1].strip('[]'))
            currentLocation = locationName

            if currentLocation not in locationData:
                locationData[currentLocation] = {"Members": False, "MapId": None, "Coordinates": {0: [], 1: []}}
            currentPlane = 0

        elif line.startswith('|mem='):
            locationData[currentLocation]["Members"] = line.split('=')[1].strip() == 'yes'
        
        elif line.startswith('|mapID='):
            mapIdPart = line.split('=')[1].strip()
            plane = 0
            if '|plane=' in mapIdPart:
                mapIdPart, planePart = mapIdPart.split('|plane=')
                currentPlane = int(planePart.strip())
            try:
                locationData[currentLocation]["MapId"] = int(mapIdPart.strip())
            except ValueError:
                print(f"Error parsing mapID: {mapIdPart.strip()}")

        elif line.startswith('|plane='):
            currentPlane = int(line.split('=')[1].strip())

        elif line.startswith('|npcid:'):
            coords = line.split('|')[1:]
            for coord in coords:
                parts = coord.split(',')
                try:
                    x = int(parts[1].split(':')[1])
                    y = int(parts[2].split(':')[1].split('}')[0])
                    locationData[currentLocation]["Coordinates"][currentPlane].append([x, y])
                except ValueError:
                    print(f"Error parsing coordinates: {coord}")

    for location, data in locationData.items():
        data["Coordinates"] = {k: v for k, v in data["Coordinates"].items() if v}

    return locationData