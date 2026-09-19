
#Database handling to be added through .env   
#Import dotenv and os modules

import random
from inputimeout import inputimeout, TimeoutOccurred

db_fetch_result = (["aAa", "fi"], ["bbb", "de"], ["ccC", "fi"], ["DDD", "de"], ["565", "fi"], ["343", "de"], ["2934", "fi"], ["326", "de"], ["944", "fi"], ["4", "de"], ["5", "fi"], ["45345", "de"]) #Example dataset used for basic debugging and testing
fetch_to_list=list(db_fetch_result) #converting tuple into a list as SQL db output is a tuple



index_list = []

for index, item in enumerate(fetch_to_list):
    index_list.append(index)

fetch_result = []

        
while len(fetch_result) < 7:
        rand_index = random.choice(index_list)
        try:
                fetch_result.append(fetch_to_list[rand_index])
                index_list.remove(rand_index)
       
        except:
            pass
        
        
  
for item in fetch_result:
        if random.randrange(1, 4) % 2 == 0:
            item.append(True)
        else:
            item.append(False)


  


#core game variables
round_count = 1
player_score = 1


while True:  
    
    icao_list = [] #list used for value comparison

            
    for row in fetch_result:
        print(f"ICAO code : {row[0]} country: {row[1]}  {'x' if row[2] == True else ' ' }")
      
    for item in fetch_result:
        if  item[2] == True:
            icao_list.append(item[0])
    
   
    
    try:
        usr_input = inputimeout(prompt = "Please type in ICAO code: ", timeout = 10)
    except TimeoutOccurred:
        print("Your time is up")
        break
    
    if usr_input in icao_list:
        
        print(f'\n'+"That was correct!"+'\n')
        print(f"Your score is: {player_score}"+'\n')
        
        for item in fetch_result:
            if item[0] == usr_input:
               index_check = fetch_result.index(item)
               fetch_result.pop(index_check)
        icao_list = [item[0] for item in fetch_result if item[2]]
               
        player_score = player_score+1
        round_count = round_count +1                   
    else:
        print('\n'+"Game Over"+'\n')
        break
           
    # print(fetch_result)
    # print(icao_list)
    
    if len(icao_list) == 0 or round_count == 5:
        print("Victory"+'\n')
        break