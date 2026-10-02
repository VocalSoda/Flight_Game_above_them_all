
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

sql = "SELECT * FROM airport order by RAND() limit 7;"
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
        

    
def render_text(content: str, x, y, color):
    text1 = font1.render(content, True, color)
    textRect1 = text1.get_rect()
    
    textRect1.center = x, y

    screen.blit(text1, textRect1)
    
    
def render_text_allign_left(content: str, x, y):
    text1 = font1.render(content, True, (0, 255, 0))
    textRect1 = text1.get_rect()
    
    textRect1.midleft = x, y

    screen.blit(text1, textRect1)



def render_text_w_bg(content: str, x, y, color):
    text1 = font1.render(content, True, color)
    textRect1 = text1.get_rect(center=(x, y))
    bg_rect = textRect1.inflate(5, 5)
    pygame.draw.rect(screen, (255, 255, 255), bg_rect, border_radius=6)
    textRect1.center = x, y

    screen.blit(text1, textRect1)
        
    
def coordinates_to_pixels(lat, lon):
    lat = max(min(lat, 85.051129), -85.051129)
    
    x = (lon + 180.0) * (map_width / 360.0)
  
    lat_rad = math.radians(lat)
    merc_n = math.log(math.tan((math.pi / 4) + (lat_rad / 2)))

    y = (map_height / 2) - (map_width * merc_n / (2 * math.pi))
    
    return (x,y)

text = ""
active_target = None
def input_field(text, x, y):
    
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RETURN:
                print("Submitted:", text)
                text = ""
        elif event.key == pygame.K_BACKSPACE:
                text = text[:-1]
    text_surface = font1.render(text, True, (0, 255, 0))
    input_rect = text_surface.get_rect()            
    input_rect.center = x, y
    screen.blit(text_surface, input_rect)
    


cords_on_map = []

cords_list = []
for item in db_fetch_result:
    cords_list.append([item[4], item[5]])





for item in cords_list:

    pixel_coordinates = coordinates_to_pixels(item[0], item[1])       
    cords_on_map.append([pixel_coordinates[0], pixel_coordinates[1]])
        


name_list = []

for item in db_fetch_result:
    name_list.append(item[3])

print(name_list)


name_check_list = []

color_check = [] 

while len(color_check) < len(cords_on_map):
    if random.choice("1234") == "2":
        color_check.append([255, 0, 0])
    else:
        color_check.append([0, 0, 255])       
    
print(color_check)    
def render_circle(color, x, y):  
   
   circle =  pygame.draw.circle(screen, color, (x, y),  10, 10,)

   return circle

width = screen.get_width()
height = screen.get_height()
                  

while running:
    screen.fill((0, 0, 0))
    render_map()
    mouse_pos = pygame.mouse.get_pos()
    mouse_buttons = pygame.mouse.get_pressed()  
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    active_target = None
                    for name, (x, y) in zip(name_list, cords_on_map):
                        rect = pygame.Rect(x - 10, y - 10, 20, 20)
                        if rect.collidepoint(mouse_pos):
                            active_target = x, y
                            
            elif event.type == pygame.KEYDOWN and active_target is not None:
                if event.key == pygame.K_RETURN:
                    print("Submitted:", text)
                    name_check_list.append(text)
                    if text not in name_list:
                        running = False
                    text = ""
                    print(name_check_list)
                    active_target = None
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode
                    
                    
                                    
    for  color, name, (x, y) in zip( color_check, name_list, cords_on_map):
                if name in name_check_list:
                    color_check.remove(color)
                else:          
                    circle = render_circle(color, x, y)
                    if circle.collidepoint(mouse_pos):
                        render_text_w_bg(name, x, y+20, color)
                        
                        
    if [255, 0, 0] not in color_check:
        print("WIN")
        running = False

        

    if active_target:
        ax, ay = active_target
        text_surface = font1.render(text, True, (247, 130, 0))
        input_rect = text_surface.get_rect(center=(ax, ay - 25))
        bg_rect = input_rect.inflate(50, 16)
        pygame.draw.rect(screen, (20, 20, 20), bg_rect, border_radius=6)
        screen.blit(text_surface, input_rect)
        
    for i, item in enumerate(db_fetch_result):
        offset = 25 * i
        string = f"{item[3]} + Cords: {item[4]} , {item[5]}"
        render_text_allign_left(string, map_width + 20, 500 - offset)          
    
    pygame.display.update()    