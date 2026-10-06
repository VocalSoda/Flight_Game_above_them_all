import math
import os
import random
import time

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

DIFFICULTIES = {
    1: ("Easy", 60, 1),
    2: ("Medium", 40, 3),
    3: ("Hard", 30, 5),
}

pygame.init()
pygame.mixer.init()
explosion_sound = pygame.mixer.Sound("./src/resources/sounds/explosion.wav")
wrong_sound = pygame.mixer.Sound("./src/resources/sounds/wrong.wav")
correct_sound = pygame.mixer.Sound("./src/resources/sounds/correct.wav")
select_sound = pygame.mixer.Sound("./src/resources/sounds/select.wav")
win_sound = pygame.mixer.Sound("./src/resources/sounds/win.wav")
lose_sound = pygame.mixer.Sound("./src/resources/sounds/lose.wav")
time_warning_sound = pygame.mixer.Sound("./src/resources/sounds/time_warning.wav")
screen = pygame.display.set_mode((1920, 1080), pygame.RESIZABLE)
clock = pygame.time.Clock()

base_map = pygame.image.load("./src/resources/images/mercator.png").convert()
font = pygame.font.Font("./src/resources/fonts/Space_Mono/SpaceMono-Regular.ttf", 30)

def connect():
    return mysql.connector.connect(
        host=os.getenv("HOST"),
        user=os.getenv("USER"),
        password=os.getenv("PASS"),
        database=os.getenv("DB"),
    )


def load_airports():
    connection = connect()

    cursor = connection.cursor()

    cursor.execute(
        "SELECT ident, name, latitude_deg, longitude_deg FROM airport "
        "WHERE name REGEXP '^[A-Za-z0-9 .-]+$' "
        "AND ident REGEXP '^[A-Za-z0-9 .-]+$' "
        "ORDER BY RAND() LIMIT 7"
    )

    rows = cursor.fetchall()
    connection.close()

    return rows


def load_high_scores():
    connection = connect()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT name, score, time FROM save_files ORDER BY score DESC, time ASC LIMIT 10"
    )

    rows = cursor.fetchall()
    connection.close()

    return rows


def save_score(name, score, seconds):
    connection = connect()

    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO save_files (name, score, time, did_win) VALUES (%s, %s, %s, 1)",
        (name, score, round(seconds, 1)),
    )

    connection.commit()
    connection.close()


def lat_lon_to_pixels(lat, lon):
    lat = max(min(lat, 85.051129), -85.051129)

    x = (lon + 180.0) * (MAP_W / 360.0)

    merc = math.log(math.tan(math.pi / 4 + math.radians(lat) / 2))

    y = MAP_H / 2 - MAP_W * merc / (2 * math.pi)

    return x, y


def update_positions():
    for airport in airports:
        airport["pos"] = lat_lon_to_pixels(airport["lat"], airport["lon"])

    spread_airports()


def spread_airports():
    for _ in range(20):
        moved = False
        for i in range(len(airports)):
            for j in range(i + 1, len(airports)):
                ax, ay = airports[i]["pos"]
                bx, by = airports[j]["pos"]

                dx, dy = bx - ax, by - ay

                dist = math.hypot(dx, dy)

                if 0 < dist < 90:
                    push = (90 - dist) / 2

                    ux, uy = dx / dist, dy / dist

                    airports[i]["pos"] = (ax - ux * push, ay - uy * push)
                    airports[j]["pos"] = (bx + ux * push, by + uy * push)

                    moved = True

        if not moved:
            break


def resize():
    global world_map, MAP_W, MAP_H

    h = screen.get_height()
    scale = h / base_map.get_height()

    world_map = pygame.transform.scale_by(base_map, scale)

    MAP_W, MAP_H = world_map.get_size()

    update_positions()


def start_game(difficulty):
    global airports, active, text, feedback, state, start_time, time_limit, score

    airports = [
        {
            "icao": icao,
            "name": name,
            "lat": lat,
            "lon": lon,
            "infected": False,
            "destroyed": False,
        }
        for icao, name, lat, lon in load_airports()
    ]

    _, time_limit, num_infected = DIFFICULTIES[difficulty]

    for airport in random.sample(airports, num_infected):
        airport["infected"] = True

    update_positions()
    active = None
    text = ""
    feedback = ""
    score = 0
    time_warning_played = False
    start_time = time.perf_counter()
    state = "playing"
    


def select_by_icao(text):
    for airport in airports:
        if not airport["destroyed"] and airport["icao"].lower() == text.lower():
            select_sound.play()
            return airport

    return None


def best_icao_match(text):
    if not text:
        return []

    best = []
    best_len = -1
    typed = text.lower()

    for airport in airports:
        if airport["destroyed"]:
            continue

        icao = airport["icao"].lower()
        n = 0

        while n < len(typed) and n < len(icao) and icao[n] == typed[n]:
            n += 1
        if n > best_len:
            best = [airport]
            best_len = n
        elif n == best_len and n > 0:
            best.append(airport)

    return best


def submit(active, text):
    if text.strip().lower() != active["name"].lower():
        wrong_sound.play()
        return active, "", "Wrong name.", False
    if not active["infected"]:
        return active, "", "Not infected.", False

    active["destroyed"] = True
    correct_sound.play()
    explosion_sound.play()
    return None, "", "Destroyed!", True


def render_boxed_text(content, color, center, midleft=False):
    surface = font.render(content, True, color)
    rect = surface.get_rect(midleft=center) if midleft else surface.get_rect(center=center)

    bg_rect = rect.inflate(10, 6)
    bg_rect.clamp_ip(screen.get_rect())

    rect.clamp_ip(bg_rect)

    pygame.draw.rect(screen, DARK, bg_rect, border_radius=6)

    screen.blit(surface, rect)


def render_match_text(target, typed, center):
    total = font.render(target, True, WHITE)

    rect = total.get_rect(center=center)

    bg_rect = rect.inflate(10, 6)
    bg_rect.clamp_ip(screen.get_rect())

    pygame.draw.rect(screen, DARK, bg_rect, border_radius=6)

    x = rect.left

    for i, ch in enumerate(target):
        if i < len(typed):
            color = GREEN if typed[i].lower() == ch.lower() else RED
        else:
            color = WHITE

        char = font.render(ch, True, color)
        screen.blit(char, (x, rect.top))

        x += char.get_width()


def render_airports():
    best_list = best_icao_match(text) if active is None else []

    for airport in airports:
        if airport["destroyed"]:
            continue

        x, y = airport["pos"]

        if airport is active:
            pygame.draw.circle(screen, WHITE, (x, y), 15, 3)
        pygame.draw.circle(screen, RED if airport["infected"] else BLUE, (x, y), 15)

        if active is None and airport in best_list:
            render_match_text(airport["icao"], text, (x, y + 25))
        else:
            render_boxed_text(airport["icao"], WHITE, (x, y + 25))

    if active is not None:
        x, y = active["pos"]

        render_boxed_text(active["name"], WHITE, (x, y - 35), midleft=True)
        render_boxed_text(text, ORANGE, (x, y - 70), midleft=True)


def render_menu():
    cx = screen.get_width() // 2
    title = font.render("Airport Hunter", True, WHITE)
    rect = title.get_rect(center=(cx, 200))
    bg_rect = rect.inflate(screen.get_width()/5, screen.get_height()/3)
    bg_rect.top = rect.top
    pygame.draw.rect(screen, DARK, bg_rect,border_radius=10)
    pygame.draw.rect(screen, (255, 255, 255), bg_rect, width=5, border_radius=10)
    screen.blit(title, rect)
    y = 350

    for key, (name, seconds, infected) in DIFFICULTIES.items():
        line = font.render(f"{key}. {name}: {infected} infected, {seconds}s", True, GREEN)
        screen.blit(line, line.get_rect(center=(cx, y)))

        y += 60


def render_high_scores():
    x = MAP_W + 30

    header = font.render("HIGH SCORES", True, ORANGE)
    screen.blit(header, (x, 30))

    y = 90

    for rank, (name, score_value, seconds) in enumerate(high_scores, 1):
        line = font.render(f"{rank}. {name or '???'} {score_value}pts {seconds}s", True, WHITE)
        screen.blit(line, (x, y))

        y += 40


def render_hud():
    destroyed = sum(a["destroyed"] for a in airports)
    total = sum(a["infected"] for a in airports)
    time_left = max(0, time_limit - (time.perf_counter() - start_time))

    counter = font.render(
        f"{destroyed}/{total} infected destroyed   {time_left:.0f}s left", True, WHITE
    )

    screen.blit(counter, (20, 20))

    if active is None:
        prompt = "Type ICAO to select an airport, Enter to confirm"
    else:
        prompt = f"Type the name of {active['icao']}"

    render_boxed_text(prompt, GREEN, (screen.get_width() // 2, 30))

    if feedback:
        render_boxed_text(feedback, WHITE, (screen.get_width() // 2, 70))


def render_game_over():
    cx, cy = screen.get_width() // 2, screen.get_height() // 2

    if state == "won":
        title = font.render(f"YOU WIN! Score: {score}  Time: {elapsed:.1f}s", True, GREEN)
    else:
        title = font.render(f"TIME'S UP! Score: {score}", True, RED)

    screen.blit(title, title.get_rect(center=(cx, cy - 40)))
    hint = font.render("Press Enter to return to menu", True, WHITE)

    screen.blit(hint, hint.get_rect(center=(cx, cy + 20)))


def render_name_entry():
    cx, cy = screen.get_width() // 2, screen.get_height() // 2

    title = font.render(f"YOU WIN! Score: {score}  Time: {elapsed:.1f}s", True, GREEN)
    screen.blit(title, title.get_rect(center=(cx, cy - 80)))

    prompt = font.render("Enter your name:", True, WHITE)
    screen.blit(prompt, prompt.get_rect(center=(cx, cy)))

    name = player_name or "_"
    name_surface = font.render(name, True, ORANGE)

    screen.blit(name_surface, name_surface.get_rect(center=(cx, cy + 50)))

    hint = font.render("Type name, then press Enter", True, WHITE)

    screen.blit(hint, hint.get_rect(center=(cx, cy + 100)))


airports = []
active = None
text = ""
feedback = ""
state = "menu"
time_warning_played = False
player_name = ""
score = 0
elapsed = 0
start_time = 0
time_limit = 0
resize()
high_scores = load_high_scores()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.VIDEORESIZE:
            resize()

        elif event.type == pygame.KEYDOWN:
            if state == "menu":
                if event.key in (pygame.K_1, pygame.K_2, pygame.K_3):
                    start_game(event.key - pygame.K_0)

            elif state == "name_entry":
                if event.key == pygame.K_RETURN:
                    save_score(player_name, score, elapsed)
                    high_scores = load_high_scores()
                    state = "menu"

                elif event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]

                elif event.unicode.isalnum() and len(player_name) < 3:
                    player_name += event.unicode.upper()

            elif state in ("won", "lost"):
                if event.key == pygame.K_RETURN:
                    state = "menu"
                    high_scores = load_high_scores()

            elif state == "playing":
                if event.key == pygame.K_ESCAPE:
                    active = None
                    text = ""
                    feedback = ""

                elif event.key == pygame.K_RETURN:
                    if active is None:
                        selected = select_by_icao(text)

                        if selected is not None:
                            active = selected
                            text = ""
                            feedback = ""

                        else:
                            text = ""
                            feedback = "Unknown ICAO"

                    else:
                        active, text, feedback, destroyed = submit(active, text)

                        score += destroyed

                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]

                else:
                    text += event.unicode

    if state == "playing":
        elapsed = time.perf_counter() - start_time
        if time_limit - elapsed <= 10 and not time_warning_played: 
            time_warning_sound.play()
            time_warning_played = True
        destroyed = sum(a["destroyed"] for a in airports)
        total_infected = sum(a["infected"] for a in airports)

        if destroyed == total_infected:
            win_sound.play()
            state = "name_entry"
            player_name = ""
        elif elapsed >= time_limit:
            lose_sound.play()
            state = "lost"

    screen.fill((0, 0, 0))
    screen.blit(world_map, (0, 0))
    render_high_scores()

    if state == "menu":
        render_menu()
    elif state == "playing":
        render_airports()
        render_hud()
    elif state == "name_entry":
        render_airports()
        render_name_entry()
    else:
        render_airports()
        render_game_over()

    pygame.display.update()
    clock.tick(60)