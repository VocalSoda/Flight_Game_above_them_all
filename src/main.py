
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
) #AI enerated test data to be deleted

fetch_to_list=list(db_fetch_result) #converting tuple into a list as SQL db output is a tuple



index_list = []
#index list keeps track of used/available indexes
for index, item in enumerate(fetch_to_list):
    index_list.append(index)


#core game list function, previously was made into 2 separate loops. Now can be called from inside the loop main loop.
# 7 items are best to show imo as it seems to be ideal range where you can see whole list, without needing to scroll

def generate_fetch_result():
    fetch_result = [] #main list used for printing data and data comparison

    while len(fetch_result) < 7:
        rand_index = random.choice(index_list)
        index_list.remove(rand_index)

        fetch_result.append(fetch_to_list[rand_index])

   
    for item in fetch_result:
        item.append(random.randrange(1, 4) % 2 == 0)

    #random item is going to be set true if previous rand range did not work, does happen for some reason
    if not any(item[2]==True for item in fetch_result):
        rand_index = random.randint(0, len(fetch_result)-1)
        fetch_result[rand_index][2] = True

    return fetch_result

fetch_result = generate_fetch_result()

#core game variables
round_count = 1
player_score = 1


while True:  
    
    name_list = [] #list used for value comparison 

            
    for row in fetch_result:
        print(f"ICAO code : {row[0]} country: {row[1]}  {'x' if row[2] == True else ' ' }") #Main print, sql query would need to have name as first, country code as second from country table
      
    for item in fetch_result:
        if  item[2] == True:
            icao_list.append(item[0])
    
   
    start_time = time.perf_counter() #score count timer using time plugin
    try:
        usr_input = inputimeout(prompt = "Please type in ICAO code: ", timeout = 10) #time out, we might add modes where for instance hard mode would have less time
    except TimeoutOccurred:
        print("Your time is up")
        break
    
    elapsed_time = time.perf_counter() - start_time
    
    if usr_input in icao_list: #string comparrison if statement, string comparison is case sensitive by default, I think it also coul be adjusted like, normal mode = capitalize all, hard = do nothing and it is case sensitive
        
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
        fetch_result = generate_fetch_result() #core function call to regenerate main game list


        
         
    
    if round_count == 6: 
        print("Victory"+'\n')
        print(f"Your total score is: {player_score}")
        break