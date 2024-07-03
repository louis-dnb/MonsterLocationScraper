import functions
import json

def main():
    name = input("Enter the name of the creature: ")
    creatureName = functions.formatCreatureName(name)
    print(f"Formatted creature name: {creatureName}")
    sectionNumber = functions.findSectionNumber(creatureName)
    print(f"Section number: {sectionNumber}")
    if not sectionNumber:
        print("Section number not found.")
        return
    
    content = functions.infoFromEditPage(creatureName, sectionNumber)
    if not content:
        print("Content not found.")
        return
    
    locationsData = functions.getMonsterLocationData(content)
    if not locationsData:  # Check if locations_data is empty
        print("No location data found.")
    else:
        with open(creatureName + ".json", 'w', encoding='utf-8') as file:
            file.write(json.dumps(locationsData, indent=4))
        
if __name__ == "__main__":
    main()