#Database handling to be added through .env
#Import dotenv and os modules
import pygame
import random
from inputimeout import inputimeout, TimeoutOccurred
import time
import math
import os
from dotenv import load_dotenv
import mysql.connector
pygame.font.init()
pygame.init()

screen = pygame.display.set_mode()
clock = pygame.time.Clock()
running = True

world_map_image = pygame.image.load('src/resources/images/world.png')

x, y = screen.get_size()
print(x, y)
world_map_image = pygame.transform.scale_by(world_map_image, 0.5)

font1 = pygame.font.SysFont('./resources/fonts/Space_Mono/SpaceMono-Regular.ttf', 50)   

def render_text(content: str, position):
    text1 = font1.render(content, True, (0, 255, 0))
    textRect1 = text1.get_rect()
    
    textRect1.topleft = position
    #textRect1.center = (0, 250)

    screen.blit(text1, textRect1)


def render_map():
    screen.blit(world_map_image, (0,0))





load_dotenv()
#Remember to have same key names in your .env file
connection = mysql.connector.connect(
    host = os.getenv("HOST"),
    user = os.getenv("USER"),
    password = os.getenv("PASS"),
    database = os.getenv("DB")
)

db_fetch_result = []

sql = "SELECT * FROM airport LIMIT 10;"
try:
    cursor = connection.cursor()
    cursor.execute(sql)
    db_fetch_result = cursor.fetchall()
except:

    if cursor.rowcount == 0:
        print("Check SQL command")
    elif connection.cursor != True:
        print("Check db credentials, they must match the names used in the .env file")
        quit()

fetch_to_list = []
for item in db_fetch_result:
     fetch_to_list.append(list(item))



index_list = []
#index list keeps track of used/available indexes
for index, item in enumerate(db_fetch_result):
    index_list.append(index)



mode_map = {
    "1": (1, 50),   # Easy:   1 correct answer,  50 seconds per round
    "2": (3, 40),   # Medium: 3 correct answers, 40 seconds per round
    "3": (5, 30),   # Hard:   5 correct answers, 30 seconds per round
}

print("Choose a game mode:")
print("1 - Easy   (1 correct answer,  50 seconds per round)")
print("2 - Medium (3 correct answers, 40 seconds per round)")
print("3 - Hard   (5 correct answers, 30 seconds per round)")

while True:
    mode_choice = input("Enter mode (1/2/3): ").strip()
    if mode_choice in mode_map:
        num_true, round_time_limit = mode_map[mode_choice]
        break
    print("Please enter 1, 2 or 3.")



#core game list function, previously was made into 2 separate loops. Now can be called from inside the loop main loop.
# 7 items are best to show imo as it seems to be ideal range where you can see whole list, without needing to scroll

# ===== NEW: split the "mark one correct answer" logic into its own function =====
# This function randomly picks one airport that is NOT yet marked True, and marks it True.
# If everything is already True, it does nothing (avoids random.choice on an empty list).
def mark_one_correct(fetch_result):
    unmarked = [i for i, item in enumerate(fetch_result) if item[2] == False]
    if unmarked:
        chosen = random.choice(unmarked)
        fetch_result[chosen][2] = True
# ===== END NEW =====

def generate_fetch_result(num_true):
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

    # Initialize everything as False first
    for item in fetch_result:
        item.append(False)

    # ===== NEW: call mark_one_correct num_true times =====
    # mode 1 -> called once, mode 2 -> called 3 times, mode 3 -> called 5 times
    for _ in range(num_true):
        mark_one_correct(fetch_result)
    # ===== END NEW =====

    return fetch_result

fetch_result = generate_fetch_result(num_true)

#core game variables
round_count = 1
player_score = 0
game_start = time.perf_counter()

while True:

    for row in fetch_result:
        print(f"Airport name:   {row[0]} : country: {row[1]}  {'x' if row[2] == True else ' ' }") #Main print, sql query would need to have name as first, country code as second from country table

    # ===== NEW: correct answers list is taken from the AIRPORT NAME column (item[0]), order preserved =====
    # Using a list (not a set) so duplicate names are allowed
    answer_list = [item[0] for item in fetch_result if item[2] == True]
    # ===== END NEW =====

    correct_count = 0   # counts correct answers this round
    missed = []          # country codes the player got wrong / missed
    lost_on_timeout = False
    round_start = time.perf_counter()

    # ===== NEW: ask one question at a time, do NOT stop early on a wrong answer =====
    for i, correct_answer in enumerate(answer_list):
        # ===== NEW: remaining time = round limit minus time already spent this round =====
        time_used_so_far = time.perf_counter() - round_start
        time_left = round_time_limit - time_used_so_far

        if time_left <= 0:
            print("Your time is up")
            lost_on_timeout = True
            break
        # ===== END NEW =====

        try:
            usr_input = inputimeout(
                prompt=f"({i+1}/{len(answer_list)}) Type the full airport name ({time_left:.0f}s left): ",
                timeout=time_left
            )
        except TimeoutOccurred:
            print("Your time is up")
            lost_on_timeout = True
            break

        if usr_input.strip().lower() == correct_answer.strip().lower():
            print("Correct!\n")
            correct_count += 1
        else:
            print("Wrong.\n")
            missed.append(correct_answer)
    # ===== END NEW =====

    elapsed_time = time.perf_counter() - round_start

    if lost_on_timeout:
        game_time = time.perf_counter() - game_start
        print(f"Your total score is: {player_score}")
        print(f"Total game time: {game_time:.2f}"+'\n')
        break

    # ===== NEW: add points based on how many were correct, report what was missed =====
    player_score = player_score + correct_count
    print(f"This round you got {correct_count}/{len(answer_list)} correct.")
    if missed:
        print(f"You missed: {', '.join(missed)}")
    print(f"Current total score: {player_score}\n")
    print(f"How long did answer take in seconds: {elapsed_time:.2f}"+'\n')
    # ===== END NEW =====

    round_count = round_count + 1

    # Round is over, so generate a brand new set of 7 airports for the next round
    fetch_result = generate_fetch_result(num_true)

    if round_count == 6:
        print("Victory"+'\n')
        game_time =  time.perf_counter() - game_start
        print(f"Your total score is: {player_score}")
        print(f"Total game time: {game_time:.2f}"+'\n')
        break