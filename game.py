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
pygame.display.set_caption("Space Invalides")
icon = pygame.image.load('img/icon.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('img/player.png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('img/enemy.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

# Bullet
bulletImg = pygame.image.load('img/bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# Score
score_value = 0
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

def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

def pause_text():
    pause_text = pause_font.render("PAUSED", True, (255, 255, 255))
    screen.blit(pause_text, (250, 250))

def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    return distance < 27

def button(msg, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, ac, (x, y, w, h))
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(screen, ic, (x, y, w, h))

    text = button_font.render(msg, True, (0, 0, 0))
    screen.blit(text, (x + (w / 2 - text.get_width() / 2), y + (h / 2 - text.get_height() / 2)))

def restart_game():
    global game_over, score_value, playerX, playerY, bulletY, bullet_state, enemyX, enemyY
    game_over = False
    score_value = 0
    playerX = 370
    playerY = 480
    bulletY = 480
    bullet_state = "ready"
    for i in range(num_of_enemies):
        enemyX[i] = random.randint(0, 735)
        enemyY[i] = random.randint(50, 150)

def quit_game():
    pygame.quit()
    quit()

def open_donation():
    webbrowser.open('https://www.paypal.com/donate?hosted_button_id=YOUR_PAYPAL_BUTTON_ID')

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

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    if not paused and not game_over:
        playerX += playerX_change
        playerX = max(0, min(playerX, 736))

        for i in range(num_of_enemies):
            if enemyY[i] > 440:
                game_over = True

            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0:
                enemyX_change[i] = 4
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 736:
                enemyX_change[i] = -4
                enemyY[i] += enemyY_change[i]

            collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
            if collision:
                bulletY = 480
                bullet_state = "ready"
                score_value += 1
                enemyX[i] = random.randint(0, 735)
                enemyY[i] = random.randint(50, 150)

            enemy(enemyX[i], enemyY[i], i)

        if bulletY <= 0:
            bulletY = 480
            bullet_state = "ready"

        if bullet_state == "fire":
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)

    if paused:
        pause_text()

    if game_over:
        game_over_text()
        button("Restart", 150, 350, 150, 50, (255, 255, 255), (200, 200, 200), restart_game)
        button("Quit", 500, 350, 150, 50, (255, 255, 255), (200, 200, 200), quit_game)
        button("Donate", 325, 450, 150, 50, (255, 255, 255), (200, 200, 200), open_donation)

    pygame.display.update()
