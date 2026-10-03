import math
import os
import random

import mysql.connector
import pygame
from dotenv import load_dotenv

load_dotenv()

RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
ORANGE = (247, 130, 0)
DARK = (20, 20, 20)

pygame.init()

screen = pygame.display.set_mode((1920, 1080))
clock = pygame.time.Clock()

world_map = pygame.image.load("./src/resources/images/mercator.png")
font = pygame.font.Font("./src/resources/fonts/Space_Mono/SpaceMono-Regular.ttf", 30)

scale        = screen.get_height() / world_map.get_height()
world_map    = pygame.transform.scale_by(world_map, scale)
MAP_W, MAP_H = world_map.get_size()


def load_airports():
    connection = mysql.connector.connect(
        host=os.getenv("HOST"),
        user=os.getenv("USER"),
        password=os.getenv("PASS"),
        database=os.getenv("DB"),
    )
    
    cursor = connection.cursor()
    
    # NOTE: We exclude stuff like cyrillics cause not everyone can type them. -v 3rd oct 2026
    cursor.execute(
        "SELECT name, latitude_deg, longitude_deg FROM airport "
        "WHERE name REGEXP '^[A-Za-z0-9 .-]+$' "
        "ORDER BY RAND() LIMIT 7"
    )
    
    rows = cursor.fetchall()
    connection.close()
    
    return rows

# Convert's lat-lon into mercator projection coordinates.
def lat_lon_to_pixels(lat, lon):
    lat = max(min(lat, 85.051129), -85.051129)
    
    x = (lon + 180.0) * (MAP_W / 360.0)
    
    merc = math.log(math.tan(math.pi / 4 + math.radians(lat) / 2))
    
    y = MAP_H / 2 - MAP_W * merc / (2 * math.pi)
    
    return x, y

airports = [
    {
        "name": name,
        "pos": lat_lon_to_pixels(lat, lon),
        "infected": random.random() < 0.4,
        "destroyed": False,
    }
    
    for name, lat, lon in load_airports()
]

def airport_at(pos):
    for airport in airports:
        if airport["destroyed"]:
            continue
        x, y = airport["pos"]

        if pygame.Rect(x - 10, y - 10, 20, 20).collidepoint(pos):
            return airport
    return None


def submit(active, text):
    if text.strip().lower() != active["name"].lower():
        return None, "", "Wrong name."
    if not active["infected"]:
        return None, "", "Not infected."
    
    active["destroyed"] = True
    
    return None, "", "Destroyed!"

active = None
text = ""
feedback = ""
running = True

def render_boxed_text(content, color, center):
    surface = font.render(content, True, color)
    rect = surface.get_rect(center=center)
    
    bg_rect = rect.inflate(10, 6)
    bg_rect.clamp_ip(screen.get_rect())
    
    rect.clamp_ip(bg_rect)
    
    pygame.draw.rect(screen, DARK, bg_rect, border_radius=6)
    
    screen.blit(surface, rect)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            active = airport_at(event.pos)
            text, feedback = "", ""
        elif event.type == pygame.KEYDOWN and active is not None:
            if event.key == pygame.K_RETURN:
                active, text, feedback = submit(active, text)
            elif event.key == pygame.K_BACKSPACE:
                text = text[:-1]
            else:
                text += event.unicode

    screen.fill((0, 0, 0))
    screen.blit(world_map, (0, 0))

    mouse_pos = pygame.mouse.get_pos()
    
    for airport in airports:
        if airport["destroyed"]:
            continue
    
        x, y = airport["pos"]
    
        pygame.draw.circle(screen, RED if airport["infected"] else BLUE, (x, y), 10)
    
        if airport is active or pygame.Rect(x - 10, y - 10, 20, 20).collidepoint(mouse_pos):
            render_boxed_text(airport["name"], WHITE, (x, y - 35))

    if active is not None:
        x, y = active["pos"]
    
        render_boxed_text(text, ORANGE, (x, y - 70))
    
        if feedback:
            render_boxed_text(feedback, WHITE, (x, y + 35))

    destroyed = sum(a["infected"] and a["destroyed"] for a in airports)
    total_infected = sum(a["infected"] for a in airports)
    
    counter = font.render(
        f"{destroyed}/{total_infected} infected destroyed", True, WHITE
    )
    
    screen.blit(counter, (20, 20))

    if total_infected and destroyed == total_infected:
        win = font.render("YOU WIN! Close the window to quit.", True, GREEN)
    
        screen.blit(
            win, win.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        )

    pygame.display.update()
    clock.tick(60)