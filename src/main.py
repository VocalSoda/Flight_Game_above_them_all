import random

fetch_result1 = (["aAa", "fi"], ["bbb", "de"], ["ccC", "fi"], ["DDD", "de"], ["565", "fi"], ["343", "de"])
fetch_result=list(fetch_result1)

for item in fetch_result:
    if random.randrange(1, 4) % 2 == 0:
        item.append(True)
    else:
         item.append(False)

round_count = 1
player_score = 1


while True:
    
    icao_list = [] 
    
    
    for row in fetch_result:
        if fetch_result == []:
            print("Empty list")
            break
        print(f"ICAO code : {row[0]} country: {row[1]}  {'x' if row[2] == True else ' ' }")
      
    for item in fetch_result:
        if  item[2] == True:
            icao_list.append(item[0])
    
    # print(icao_list)  
    # print(fetch_result)
    usr_input = input("Please type in ICAO code: ")

    
    if usr_input in icao_list:
        print(f'\n'+"That was correct!"+'\n')
        print(f"Your score is: {player_score}"+'\n')
        for item in fetch_result:
            if item[0] == usr_input:
               index_check = fetch_result.index(item)
               fetch_result.pop(index_check)
        player_score = player_score+1
        round_count = round_count +1                   
        
            
    else:
        print("Game Over")
        break
           
    icao_list = []

    for item in fetch_result:
        if item[2] == True:
            icao_list.append(item[0])    
    
    
    if len(icao_list) == 0 or round_count == 5:
        print("Victory")
        break