
#Database handling to be added through .env   
#Import dotenv and os modules

import random
from inputimeout import inputimeout, TimeoutOccurred
import time
import math
import os
from dotenv import load_dotenv
import mysql.connector

load_dotenv()
#Remember to have same kay namees in your .env file
connection = mysql.connector.connect(
    host = os.getenv("HOST"),
    user = os.getenv("USER"),
    password = os.getenv("PASS"),
    database = os.getenv("DB")
)

db_fetch_result = []

sql = "SELECT name, iso_country FROM airport"
try:
    cursor = connection.cursor()
    cursor.execute(sql)
    db_fetch_result = cursor.fetchall()
except:
    
    if cursor.rowcount == 0:
        print("check SQL command")
    elif connection.cursor != True:
        print("check db credentials, if they are in the .env under the same names as in connection script")
        quit()

fetch_to_list = []
for item in db_fetch_result:
     fetch_to_list.append(list(item))



index_list = []
#index list keeps track of used/available indexes
for index, item in enumerate(db_fetch_result):
    index_list.append(index)


#core game list function, previously was made into 2 separate loops. Now can be called from inside the loop main loop.
# 7 items are best to show imo as it seems to be ideal range where you can see whole list, without needing to scroll

def generate_fetch_result():
    fetch_result = [] #main list used for printing data and data comparison

    while len(fetch_result) < 7:
        try:
            rand_index = random.choice(index_list)
            index_list.remove(rand_index)
        except:
            print("Empty sequence")
            break
        try:
            fetch_result.append(fetch_to_list[rand_index])
        except:
            pass
   
    for item in fetch_result:
        item.append(random.randrange(1, 8) % 4 == 0)

    #random item is going to be set true if previous rand range did not work, does happen for some reason
    if not any(item[2]==True for item in fetch_result):
        rand_index = random.randint(0, len(fetch_result)-1)
        fetch_result[rand_index][2] = True

    return fetch_result

fetch_result = generate_fetch_result()

#core game variables
round_count = 1
player_score = 1
game_start = time.perf_counter()

while True:  
    
    name_list = [] #list used for value comparison 
   
     
    for row in fetch_result:
        print(f"Airport name:   {row[0]} : country: {row[1]}  {'x' if row[2] == True else ' ' }") #Main print, sql query would need to have name as first, country code as second from country table
      
    for item in fetch_result:
        if  item[2] == True:
            name_list.append(item[0])
    
   
    start_time = time.perf_counter() #score count timer using time plugin
    try:
        usr_input = inputimeout(prompt = "Please type in ICAO code: ", timeout = 100) #time out, we might add modes where for instance hard mode would have less time
    except TimeoutOccurred:
        print("Your time is up")
        break
    
    elapsed_time = time.perf_counter() - start_time
    
    if usr_input in name_list: #string comparrison if statement, string comparison is case sensitive by default, I think it also coul be adjusted like, normal mode = capitalize all, hard = do nothing and it is case sensitive
        
        print(f'\n'+"That was correct!"+'\n')
        print(f"Your score is: {player_score}"+'\n')
        
        for item in fetch_result:
            if item[0] == usr_input:
               index_check = fetch_result.index(item)
               fetch_result.pop(index_check)
        name_list = [item[0] for item in fetch_result if item[2]]
               
        print(f"How long did answer take in seconds: {elapsed_time:.2f}"+'\n')
        player_score = player_score + math.floor(elapsed_time)        
        round_count = round_count +1                   
    else:
        print('\n'+"Game Over"+'\n')
        game_time =  time.perf_counter() - game_start 
        print(f"Your total score is: {player_score}")
        print(f"Total game time: {game_time:.2f}"+'\n')
        break
           
    # print(fetch_result)
    # print(icao_list)
    
    if len(name_list) == 0:
        fetch_result = generate_fetch_result() #core function call to regenerate main game list


   
         
    
    if round_count == 6: 
        print("Victory"+'\n')
        game_time =  time.perf_counter() - game_start 
        print(f"Your total score is: {player_score}")
        print(f"Total game time: {game_time:.2f}"+'\n')
        break