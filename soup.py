import requests, datetime, tweepy, time
from bs4 import BeautifulSoup

def determine_ingredient(str):
    ingreds = {"beef":"🐄", 
               "pork":"🐖", 
               "ham":"🐖", 
               "chicken":"🐓",
               "wicked thai":"🐓", 
               "turkey":"🦃",
               "bacon":"🥓",
               "shrimp":"🦐",
               "mushroom":"🍄", 
               "tomato":"🍅", 
               "corn":"🌽",
               "carrot":"🥕",
               "potato":"🥔",
               "broccoli":"🥦",
               "cheese":"🧀",
               "cheddar":"🧀",
               "cheesy":"🧀",
               "peanut":"🥜",
               "rice":"🍚",
               "curry":"🍛",
               "chili":"🌶️",
               "breakfast":" 🍳🍳🍳",
               "vegan":"🍀"}
    
    string = " "
    for key, value in ingreds.items():
        if key in str.lower():
            string = string + value
    return string

def is_vegetarian(str):
    meats = ["ham", "pork", "beef", "chicken", "turkey", "bacon","wicked thai", "shrimp", "breakfast", "hot and sour"]
    veg = "🌿"
    if "vegan" in str.lower():
        return ""
    for key in meats:
        if key in str.lower():
            return ""
    return veg
    
    
def get_soup():    
    #parsing the webpage
    url = "https://www.uvic.ca/services/food/what/soups/index.php"
    r = requests.get(url)

    soup = BeautifulSoup(r.content, "html.parser")
    potentialSoups = soup.find_all("div", {"class":"expand-collapse"})
    places = ["Arts Place","Court Cafe","Halftime","Mac's", "Commons Kitchen", "Mystic Market", "Nibbles and Bytes","Sci Cafe", "Village Greens"]
    soups = potentialSoups[0].text
    #print(soups)
    
    #cleaning up string 
    newsoups = []
    allsoups = soups.split("\n")
    first = allsoups[0].replace('Close allOpen all', '')
    temp_soups = [first] + allsoups[1:]
    #print(temp_soups)
    
    for i in range(len(temp_soups)):
        temp = temp_soups[i]
        is_place = False
        
        for place in places:
            temp = temp.replace(place, "\n"+place+"\n") 
            is_place = True
        
        if is_place:
            #if a place has no soups it will concatonate with the next place, so we need to separate each string
            temp = temp.split("\n")
            newsoups = newsoups + temp
        else:
            newsoups.append(temp)
        
   # print(newsoups)

    menu = list(filter(None, newsoups))
    #print(menu)

    #making the tweet
    time.ctime()
    str = 'Soups for ' + time.strftime('%A %b%e %Y') + ':\n'
    for i in range(len(menu)):
        if menu[i] in places:
            if i+1 < len(menu):
                if menu[i+1] in places:
                    continue
                elif menu[i+1] == "Not Available":
                    continue
            elif menu[i] in places:
                continue
            str = str + "\n" + menu[i] + "\n"
        else: 
            if menu[i] == "Not Available":
                    continue
            indicator = determine_ingredient(menu[i])
            veg = is_vegetarian(menu[i])
            str = str + "• " + menu[i] + indicator + veg
            str = str + "\n"    
    
    #To-do: validate that webpage has been updated before tweeting
    #today = soup.find_all("p", {"class":"article-data feed-data"})
    #print(today[0].text)
    
    #str1 = today[0].text
    #str2 = time.strftime('%b%e, %Y')
    #print(str1)
    #print(str2)
    #if str1 == str2:
    #    print("same day")
    
    #To-do: if string is longer than the 280 character limit, break it up to <280 character chunks and tweet a thread
    
    return str
    
print(get_soup())
