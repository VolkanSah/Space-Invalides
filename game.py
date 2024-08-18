import pygame
import random
import math
import webbrowser

# Initialize Pygame
pygame.init()

# Screen dimensions
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('img/background.png')

# Title and Icon
pygame.display.set_caption("Monochromer Flugsimulator")
icon = pygame.image.load('img/icon.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('img/player.png')
playerX = 370
playerY = 480
playerX_change = 0

# Obstacles (Enemies)
obstacleImg = []
obstacleX = []
obstacleY = []
obstacleX_change = []
obstacleY_change = []
num_of_obstacles = 2  # Start mit 1-2 Hindernissen

for i in range(num_of_obstacles):
    obstacleImg.append(pygame.image.load(f'img/obstacle_{i % 5 + 1}.png'))  # 5 verschiedene Hindernisse
    obstacleX.append(random.randint(0, 735))
    obstacleY.append(random.randint(-100, -50))  # Starten außerhalb des Bildschirms
    obstacleX_change.append(0)  # Bewegung nur vertikal
    obstacleY_change.append(2)  # Langsamer Start, wird später schneller

# Bullet
bulletImg = pygame.image.load('img/bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# Score and Level
score_value = 0
level = 1
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# Game Over Text
over_font = pygame.font.Font('freesansbold.ttf', 64)

# Pause Text
pause_font = pygame.font.Font('freesansbold.ttf', 64)

# Buttons
button_font = pygame.font.Font('freesansbold.ttf', 32)

# Pause Status
paused = False

# Game Over Status
game_over = False

# Granatenstatus
grenades = 1

# Multiplikator für die Punkte
multiplier = 1

def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def show_level(x, y):
    level_text = font.render("Level : " + str(level), True, (255, 255, 255))
    screen.blit(level_text, (x, y))

def show_grenades(x, y):
    grenade_text = font.render("Grenades : " + str(grenades), True, (255, 255, 255))
    screen.blit(grenade_text, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

def pause_text():
    pause_text = pause_font.render("PAUSED", True, (255, 255, 255))
    screen.blit(pause_text, (250, 250))

def player(x, y):
    screen.blit(playerImg, (x, y))

def obstacle(x, y, i):
    screen.blit(obstacleImg[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

def isCollision(obstacleX, obstacleY, bulletX, bulletY):
    distance = math.sqrt((math.pow(obstacleX - bulletX, 2)) + (math.pow(obstacleY - bulletY, 2)))
    return distance < 27

def player_collision(obstacleX, obstacleY, playerX, playerY):
    distance = math.sqrt((math.pow(obstacleX - playerX, 2)) + (math.pow(obstacleY - playerY, 2)))
    return distance < 50  # Größere Toleranz für Kollision

def button(msg, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, ac, (x, y, w, h))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(screen, ic, (x, y, w, h))

    text = button_font.render(msg, True, (0, 0, 0))
    screen.blit(text, (x + (w / 2 - text.get_width() / 2), y + (h / 2 - text.get_height() / 2)))

def restart_game():
    global game_over, score_value, playerX, playerY, bulletY, bullet_state, obstacleX, obstacleY, multiplier, grenades, level, num_of_obstacles
    game_over = False
    score_value = 0
    level = 1
    grenades = 1
    playerX = 370
    playerY = 480
    bulletY = 480
    bullet_state = "ready"
    multiplier = 1
    num_of_obstacles = 2  # Zurücksetzen auf den Startwert
    for i in range(num_of_obstacles):
        obstacleX[i] = random.randint(0, 735)
        obstacleY[i] = random.randint(-100, -50)

def quit_game():
    pygame.quit()
    quit()

def open_donation():
    webbrowser.open('https://www.paypal.com/donate?hosted_button_id=YOUR_PAYPAL_BUTTON_ID')

def use_grenade():
    global score_value, grenades, multiplier
    if grenades > 0:
        score_value += int(2 * multiplier * num_of_obstacles)
        grenades -= 1
        for i in range(num_of_obstacles):
            obstacleX[i] = random.randint(0, 735)
            obstacleY[i] = random.randint(-100, -50)
        show_grenade_text()

def show_grenade_text():
    text = font.render("Granate used +100 % Points!", True, (255, 255, 0))
    screen.blit(text, (200, 300))
    pygame.display.update()
    pygame.time.wait(1000)  # Zeige den Text für 1 Sekunde an

# Main game loop
running = True
while running:
    screen.fill((0, 0, 0))  # Dark background
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:  # 'P' key for pause
                paused = not paused  # Toggle pause status

            if not paused and not game_over:
                if event.key == pygame.K_LEFT:
                    playerX_change = -5
                if event.key == pygame.K_RIGHT:
                    playerX_change = 5
                if event.key == pygame.K_SPACE:
                    if bullet_state == "ready":
                        bulletX = playerX
                        fire_bullet(bulletX, bulletY)
                if event.key == pygame.K_g:  # 'G' key for grenade
                    use_grenade()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    if not paused and not game_over:
        playerX += playerX_change
        playerX = max(0, min(playerX, 736))

        # Hindernisse bewegen
        for i in range(num_of_obstacles):
            if obstacleY[i] > 600:  # Hindernis verpasst
                if score_value <= 0:
                    game_over = True
                else:
                    score_value -= 1
                    obstacleY[i] = random.randint(-100, -50)
                    obstacleX[i] = random.randint(0, 735)

            obstacleY[i] += obstacleY_change[i]

            # Überprüfe Kollision mit Spieler
            if player_collision(obstacleX[i], obstacleY[i], playerX, playerY):
                if score_value > 0:
                    score_value -= 5  # Punkteabzug bei Kollision
                    obstacleY[i] = random.randint(-100, -50)
                    obstacleX[i] = random.randint(0, 735)
                else:
                    game_over = True

            # Überprüfe Kollision mit Kugel
            collision = isCollision(obstacleX[i], obstacleY[i], bulletX, bulletY)
            if collision:
                bulletY = 480
                bullet_state = "ready"
                score_value += int(1 * multiplier)
                obstacleX[i] = random.randint(0, 735)
                obstacleY[i] = random.randint(-100, -50)
                multiplier += 0.1  # Erhöht den Multiplikator bei Abschüssen

            obstacle(obstacleX[i], obstacleY[i], i)

        # Kugelbewegung
        if bulletY <= 0:
            bulletY = 480
            bullet_state = "ready"

        if bullet_state == "fire":
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change

        # Level-Up Logik
        if score_value > 0 and score_value // 10 >= level:
            level += 1
            num_of_obstacles += 1
            obstacleImg.append(pygame.image.load(f'img/obstacle_{len(obstacleImg) % 5 + 1}.png'))
            obstacleX.append(random.randint(0, 735))
            obstacleY.append(random.randint(-100, -50))
            obstacleY_change.append(2 + level * 0.5)  # Hindernisse werden schneller

        show_score(textX, textY)
        show_level(textX, textY + 40)
        show_grenades(textX, textY + 80)

    player(playerX, playerY)

    if paused:
        pause_text()

    if game_over:
        game_over_text()
        button("Restart", 150, 350, 150, 50, (255, 255, 255), (200, 200, 200), restart_game)
        button("Quit", 500, 350, 150, 50, (255, 255, 255), (200, 200, 200), quit_game)
        button("Donate", 325, 450, 150, 50, (255, 255, 255), (200, 200, 200), open_donation)

    pygame.display.update()
