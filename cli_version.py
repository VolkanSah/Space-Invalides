import os
import time
import random
import keyboard

# Spielfeld-Dimensionen
WIDTH = 40
HEIGHT = 20

# Spieler-Symbol und Position
PLAYER = 'A'
player_pos = WIDTH // 2

# Gegner-Symbol und Positionen
ENEMY = 'V'
enemies = [(x, 0) for x in range(2, WIDTH - 2, 2)]

# Geschoss-Symbol und Position
BULLET = '|'
bullet = None

# Punkte
score = 0

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def draw_screen():
    screen = [[' ' for _ in range(WIDTH)] for _ in range(HEIGHT)]
    
    # Zeichne Spieler
    screen[HEIGHT-1][player_pos] = PLAYER
    
    # Zeichne Gegner
    for x, y in enemies:
        if 0 <= y < HEIGHT:
            screen[y][x] = ENEMY
    
    # Zeichne Geschoss
    if bullet:
        x, y = bullet
        if 0 <= y < HEIGHT:
            screen[y][x] = BULLET
    
    # Ausgabe des Spielfelds
    clear_screen()
    print(f"Score: {score}")
    print('-' * (WIDTH + 2))
    for row in screen:
        print('|' + ''.join(row) + '|')
    print('-' * (WIDTH + 2))

def move_enemies():
    global enemies
    new_enemies = []
    for x, y in enemies:
        new_y = y + 1
        if new_y < HEIGHT:
            new_enemies.append((x, new_y))
    enemies = new_enemies

def move_bullet():
    global bullet, enemies, score
    if bullet:
        x, y = bullet
        new_y = y - 1
        if new_y < 0:
            bullet = None
        else:
            bullet = (x, new_y)
            # Kollisionserkennung
            if (x, new_y) in enemies:
                enemies.remove((x, new_y))
                bullet = None
                score += 10

def game_loop():
    global player_pos, bullet, enemies
    
    while True:
        draw_screen()
        
        if keyboard.is_pressed('left') and player_pos > 0:
            player_pos -= 1
        if keyboard.is_pressed('right') and player_pos < WIDTH - 1:
            player_pos += 1
        if keyboard.is_pressed('space') and not bullet:
            bullet = (player_pos, HEIGHT - 2)
        
        move_enemies()
        move_bullet()
        
        if len(enemies) == 0 or any(y >= HEIGHT-1 for _, y in enemies):
            break
        
        time.sleep(0.1)

    print(f"Game Over! Final Score: {score}")

if __name__ == "__main__":
    game_loop()
