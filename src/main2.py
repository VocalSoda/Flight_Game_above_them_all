
import pygame
import random
from inputimeout import inputimeout, TimeoutOccurred
import time
import math
import os
from dotenv import load_dotenv
import mysql.connector

load_dotenv()

pygame.font.init()
pygame.init()

screen = pygame.display.set_mode()
clock = pygame.time.Clock()
running = True

world_map_image = pygame.image.load('src/resources/images/mercator.png')
font1 = pygame.font.SysFont('./resources/fonts/Space_Mono/SpaceMono-Regular.ttf', 50)   
x, y = screen.get_size()

scalar = screen.get_height() / world_map_image.get_height()
world_map_image = pygame.transform.scale_by(world_map_image, scalar)

map_height = world_map_image.get_height()
map_width = world_map_image.get_width()




def rand_num():
    rand = None
    for num in range(2, 8):
        if num % 2 == 0:
            return True
        else:
            return False




connection = mysql.connector.connect(
    host = os.getenv("HOST"),
    user = os.getenv("USER"),
    password = os.getenv("PASS"),
    database = os.getenv("DB")
)

def render_map():
    screen.blit(world_map_image, (0,0))

db_fetch_result = []

sql = "SELECT * FROM airport LIMIT 2;"
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
        
print(db_fetch_result)


cords_on_map = []

cords_list = []
for item in db_fetch_result:
    cords_list.append([item[4], item[5]])
    

print(cords_list)
    
    
    
def render_text(content: str, position):
    text1 = font1.render(content, True, (0, 255, 0))
    textRect1 = text1.get_rect()
    
    textRect1.topleft = position

    screen.blit(text1, textRect1)
    
    
def render_circle(x, y):
    circle =  pygame.draw.circle(screen, (0, 255, 0), (x, y),  10, 10,)

    
def coordinates_to_pixels(lat, lon):
    lat = max(min(lat, 85.051129), -85.051129)
    
    x = (lon + 180.0) * (map_width / 360.0)
  
    lat_rad = math.radians(lat)
    merc_n = math.log(math.tan((math.pi / 4) + (lat_rad / 2)))

    y = (map_height / 2) - (map_width * merc_n / (2 * math.pi))
    
    return (x,y)

for item in cords_list:

    pixel_coordinates = coordinates_to_pixels(item[0], item[1])    
    cords_on_map.append([pixel_coordinates[0], pixel_coordinates[1]])
    

print(cords_on_map)

while running:
    screen.fill((255, 0, 0))
    render_map()
    
    for item in cords_on_map:
        
        render_circle(item[0], item[1])
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    pygame.display.update()    