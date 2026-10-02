
import pygame
import random
from inputimeout import inputimeout, TimeoutOccurred
import time
import math
import os
from dotenv import load_dotenv
import mysql.connector
import sys
load_dotenv()

pygame.font.init()
pygame.init()

screen = pygame.display.set_mode((1920, 1080))
clock = pygame.time.Clock()
running = True

world_map_image = pygame.image.load('src/resources/images/mercator.png')
font1 = pygame.font.SysFont('./resources/fonts/Space_Mono/SpaceMono-Regular.ttf', 30)   
x, y = screen.get_size()

scalar = screen.get_height() / world_map_image.get_height()
world_map_image = pygame.transform.scale_by(world_map_image, scalar)

map_height = world_map_image.get_height()
map_width = world_map_image.get_width()




rand_range = [2, 3, 4, 5, 6, 7, 8]


connection = mysql.connector.connect(
    host = os.getenv("HOST"),
    user = os.getenv("USER"),
    password = os.getenv("PASS"),
    database = os.getenv("DB")
)

def render_map():
    screen.blit(world_map_image, (0,0))

db_fetch_result = []

sql = "SELECT * FROM airport order by RAND() limit 3;"
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
        

    
def render_text(content: str, x, y):
    text1 = font1.render(content, True, (0, 255, 0))
    textRect1 = text1.get_rect()
    
    textRect1.center = x, y

    screen.blit(text1, textRect1)
    
    
def render_circle(x, y):
   circle =  pygame.draw.circle(screen, (0, 255, 0), (x, y),  10, 10,)
   return circle

        
    
def coordinates_to_pixels(lat, lon):
    lat = max(min(lat, 85.051129), -85.051129)
    
    x = (lon + 180.0) * (map_width / 360.0)
  
    lat_rad = math.radians(lat)
    merc_n = math.log(math.tan((math.pi / 4) + (lat_rad / 2)))

    y = (map_height / 2) - (map_width * merc_n / (2 * math.pi))
    
    return (x,y)



cords_on_map = []

cords_list = []
for item in db_fetch_result:
    cords_list.append([item[4], item[5]])





for item in cords_list:

    pixel_coordinates = coordinates_to_pixels(item[0], item[1])       
    # if rand_num():
    #     print(rand_num())
    cords_on_map.append([pixel_coordinates[0], pixel_coordinates[1]])
        


name_list = []

for item in db_fetch_result:
    name_list.append(item[3])

print(name_list)




while running:
    screen.fill((0, 0, 0))
    mouse_pos = pygame.mouse.get_pos()
    mouse_buttons = pygame.mouse.get_pressed()  
    render_map()
    
    for name, (x, y) in zip(name_list, cords_on_map):
        
      
        circle = render_circle(x, y)
        if circle.collidepoint(mouse_pos):
            render_text(name, x, y+20)
            if mouse_buttons[0]:
                running = False
            
                
     
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    pygame.display.update()    