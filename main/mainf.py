import pygame
import random
import math


pygame.init()

screen = pygame.display.set_mode((500, 800))

#Title and icon
pygame.display.set_caption("Skier")
icon = pygame.image.load('snowboard.png')
pygame.display.set_icon(icon)


# Player
playerImg = pygame.image.load('player.png')
ski_right = pygame.image.load('player_right.png')
ski_left = pygame.image.load('player_left.png')
ski_front = pygame.image.load('player.png')

playerX = 370
playerY = 100
playerX_change = 0
player_speed = 0.5


def player(x, y):
    screen.blit(playerImg, (x, y))


# Pine
pineImg = []
pineX = []
pineY = []
num_of_pine = 10
pineY_change = 0.5

for i in range(num_of_pine):
    pineImg.append(pygame.image.load('pine.png'))
    pineX.append(random.randint(100, 400))
    pineY.append(random.randint(900, 2000))


def pine(x, y, i):
    screen.blit(pineImg[i], (x, y))


# Flag
flagImg = pygame.image.load('flag.png')
flagX = random.randint(100, 300)
flagY = random.randint(800, 900)
flagY_change = 0.5


def flag(x, y):
    screen.blit(flagImg, (x, y))
    screen.blit(flagImg, (x+152, y))


# Colision pine
def isCollision(playerX, playerY, pineX, pineY):
    distance = math.sqrt(math.pow(playerX-pineX, 2)+math.pow(playerY-pineY, 2))
    if distance < 27:
        return True
    else:
        return False


# Colision flag
def isCollision_flag(playerX, playerY, flagX, flagY):
    distance_left = math.sqrt(
        math.pow(playerX-flagX, 2)+math.pow(playerY-flagY, 2))
    distance_right = math.sqrt(
        math.pow(playerX-(flagX+122), 2)+math.pow(playerY-flagY, 2))
    if (distance_left < 27) or (distance_right < 27):
        return True
    else:
        return False





# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 15)
textX = 10
textY = 10


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 0, 0))
    screen.blit(score, (x, y))




# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)

def game_over_text():
    over_text = over_font.render("GAME OVER" , True, (255, 0, 0))
    screen.blit(over_text, (50, 400))

# Winner
winner_font = pygame.font.Font('freesansbold.ttf', 64)

def winner_text():
    winner_text = winner_font.render("WINNER !" , True, (255, 0, 0))
    screen.blit(winner_text, (50, 400))


# Game Loop
running = True
while running:

    screen.fill((255, 250, 250))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Key pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -player_speed
                playerImg = ski_left
            if event.key == pygame.K_RIGHT:
                playerX_change = player_speed
                playerImg = ski_right
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
                playerImg = ski_front

    
    flagY -= flagY_change

    # Boundaries player
    if playerX <= 0:
        playerX = 0
        playerImg = ski_front
    elif playerX >= 436:
        playerX = 436
        playerImg = ski_front
           

    # Boundaries flag
    if flagY < -60:
        flagX = random.randint(100, 280)
        flagY = random.randint(900, 1050)
        for i in range(num_of_pine):
            if (flagX-100 < pineX[i] < flagX + 252) and (flagY - 100 < pineY[i] < flagY +100):
                pineX[i] += 200
    # Boundaries pine
    for i in range(num_of_pine):
        pineY[i] += -pineY_change
        if pineY[i]  < -60:
            pineX[i] = random.randint(100, 400)
            pineY[i] = random.randint(900, 2000)
            if (flagX-100 < pineX[i] < flagX + 252) and (flagY - 100 < pineY[i] < flagY +100):
                pineX[i] -= 200
        collision_pine = isCollision(playerX, playerY, pineX[i], pineY[i])
        if collision_pine:
            running = False
            #game_over_text()
        pine(pineX[i], pineY[i], i)
        

    # Collision flag
    collision_flag = isCollision_flag(playerX, playerY, flagX, flagY)
    if collision_flag:
        running = False
        #game_over_text()
        

            

    # pass flag
    if playerX > flagX and playerX < flagX + 152 and playerY == flagY:
        score_value += 1
        if score_value == 10:
            running = False
            #winner_text()
        
        

    playerX += playerX_change
    player(playerX, playerY)
    flag(flagX, flagY)
    show_score(textX, textY)
    pygame.display.update()
