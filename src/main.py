
#Database handling to be added through .env   
#Import dotenv and os modules

import random
from inputimeout import inputimeout, TimeoutOccurred
import time
import math

db_fetch_result = (
    ["aAa", "fi"],
    ["bbb", "de"],
    ["ccC", "fi"],
    ["DDD", "de"],
    ["565", "fi"],
    ["343", "de"],
    ["2934", "fi"],
    ["326", "de"],
    ["944", "fi"],
    ["4", "de"],
    ["5", "fi"],
    ["45345", "de"],
    ["ABC1", "se"],
    ["DEF2", "no"],
    ["GHI3", "dk"],
    ["JKL4", "fr"],
    ["MNO5", "es"],
    ["PQR6", "it"],
    ["STU7", "nl"],
    ["VWX8", "pl"],
    ["YZA9", "cz"],
    ["BCD0", "ee"],
    ["EFG1", "lv"],
    ["HIJ2", "lt"],
    ["KLM3", "is"],
    ["NOP4", "ie"],
    ["QRS5", "pt"],
    ["TUV6", "gr"],
    ["WXY7", "ch"],
    ["ZAB8", "at"],
    ["CDE9", "be"],
    ["FGH0", "lu"],
)
fetch_to_list=list(db_fetch_result) #converting tuple into a list as SQL db output is a tuple



index_list = []

for index, item in enumerate(fetch_to_list):
    index_list.append(index)



def generate_fetch_result():
    fetch_result = []

    while len(fetch_result) < 7:
        rand_index = random.choice(index_list)
        index_list.remove(rand_index)

        fetch_result.append(fetch_to_list[rand_index])

   
    for item in fetch_result:
        item.append(random.randrange(1, 4) % 2 == 0)

    
    if not any(item[2]==True for item in fetch_result):
        rand_index = random.randint(0, len(fetch_result)-1)
        fetch_result[rand_index][2] = True

    return fetch_result

fetch_result = generate_fetch_result()

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
    
   
    start_time = time.perf_counter()
    try:
        usr_input = inputimeout(prompt = "Please type in ICAO code: ", timeout = 10)
    except TimeoutOccurred:
        print("Your time is up")
        break
    
    elapsed_time = time.perf_counter() - start_time
    
    if usr_input in icao_list:
        
        print(f'\n'+"That was correct!"+'\n')
        print(f"Your score is: {player_score}"+'\n')
        
        for item in fetch_result:
            if item[0] == usr_input:
               index_check = fetch_result.index(item)
               fetch_result.pop(index_check)
        icao_list = [item[0] for item in fetch_result if item[2]]
               
        print(f"Elapsed time: {elapsed_time}")
        player_score = player_score + math.floor(elapsed_time)        
        round_count = round_count +1                   
    else:
        print('\n'+"Game Over"+'\n')
        break
           
    # print(fetch_result)
    # print(icao_list)
    
    if len(icao_list) == 0:
        fetch_result = generate_fetch_result()


        
         
    
    if round_count == 6:
        print("Victory"+'\n')
        break