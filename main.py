import pygame
import random
import math
from pygame import mixer

# INITIALIZE THE GAME
pygame.init()

# CREATE THE SCREEN
screen = pygame.display.set_mode((800, 600))

# BACKGROUND
background = pygame.image.load('background.png') # IMPORT IMAGE

# BACKGROUND MUSIC
#mixer.music.load('songname.wav')
#mixer.music.play(-1)

# TITLE AND ICON
pygame.display.set_caption("Space Invaders") # ADD NAME TO TITLEBAR
icon = pygame.image.load('ufo.png') # IMPORT IMAGE
pygame.display.set_icon(icon) # ADDS ICON TO THE TITLEBAR

# PLAYER
playerImg = pygame.image.load('player.png')
playerX = 370 # SET PLAYER X AXIS
playerY = 480 # SET PLAYER Y AXIS
playerX_change = 0

# ENEMY
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
  enemyImg.append(pygame.image.load('enemy.png'))
  enemyX.append(random.randint(0, 735)) # SET RANDOMISED ENEMY X AXIS
  enemyY.append(random.randint(50, 150)) # SET RANDOMISED ENEMY Y AXIS
  enemyX_change.append(4)
  enemyY_change.append(40)

# BULLET
bulletImg = pygame.image.load('bullet.png')
bulletX = 0 # BULLET X AXIS
bulletY = 480 # BULLET Y AXIS
bulletX_change = 0
bulletY_change = 20
bullet_state = 'ready' # THE STATE - READY MEANS IT CANT BE SEEN, WHEN MOVING THE STATE WILL BE 'FIRE'

# SCORE
score_value = 0
font = pygame.font.Font('PressStart2P-Regular.ttf', 32)

textX = 10
textY = 10

# GAME OVER TEXT
over_font = pygame.font.Font('PressStart2P-Regular.ttf', 64)

def show_score(x,y):
  score = font.render("Score:" + str(score_value), True, (255,255,255))
  screen.blit(score, (x, y))

def game_over_text():
  over_text = over_font.render("Game Over", True, (255,255,255))
  screen.blit(over_text, (120, 250))

def player(x,y):
  screen.blit(playerImg, (x, y)) # DRAWS PLAYER TO SCREEN

def enemy(x,y,i):
  screen.blit(enemyImg[i], (x, y)) # DRAWS ENEMY TO SCREEN

def fire_bullet(x,y):
  global bullet_state
  bullet_state = 'fire'
  screen.blit(bulletImg, (x + 16, y + 10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
  distance = math.sqrt((math.pow(enemyX - bulletX,2)) + (math.pow(enemyY - bulletY,2)))
  if distance < 27:
    return True
  else:
    return False

# GAME LOOP
running = True
while running:
  # SET THE COLOUR OF THE SCREEN WITH RGB 0>255
  screen.fill((0,0,0))
  screen.blit(background, (0,0)) # SETS THE BACKGROUND IMAGE

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False

  # CHECK IF KEYSTROKE IS LEFT OR RIGHT PRESS
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_LEFT:
        playerX_change = -7
      if event.key == pygame.K_RIGHT:
        playerX_change = 7
      if event.key == pygame.K_SPACE:
        if bullet_state is 'ready':
          bullet_sound = mixer.Sound('laser.wav')
          bullet_sound.play()
          # SETS THE CURRENT SPACESHIP COORDS IN BULLETX VARIABLE
          bulletX = playerX
          fire_bullet(bulletX, bulletY)

    if event.type == pygame.KEYUP:
      if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
        playerX_change = 0

  # BOUNDARY CHECK FOR PLAYER MOVEMENT
  playerX += playerX_change

  if playerX <= 0:
    playerX = 0
  elif playerX >= 736:
    playerX = 736

  # BOUNDARY CHECK FOR ENEMY MOVEMENT
  for i in range(num_of_enemies):

    # GAME OVER CONDITIONS
    if enemyY[i] > 440:
      for j in range(num_of_enemies):
        enemyY[j] = 2000
      game_over_text()
      break

    enemyX[i] += enemyX_change[i]

    if enemyX[i] <= 0:
      enemyX_change[i] = 4
      enemyY[i] += enemyY_change[i]
    elif enemyX[i] >= 736:
      enemyX_change[i] = -4
      enemyY[i] += enemyY_change[i]
    
    # COLLISION
    collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
    if collision:
      explosion_sound = mixer.Sound('explosion.wav')
      explosion_sound.play()
      bulletY = 480
      bullet_state = 'ready'
      score_value += 2
      enemyX[i] = random.randint(0,735) # SET RANDOMISED ENEMY X AXIS
      enemyY[i] = random.randint(50,150) # SET RANDOMISED ENEMY Y AXIS

    enemy(enemyX[i], enemyY[i], i) # PLAYER IS CALLED HERE TO MAKE IT APPEAR ABOVE BACKGROUND

  # BULLET MOVEMENT
  if bulletY <= 0:
    bulletY = 480
    bullet_state = 'ready'

  if bullet_state is 'fire':
    fire_bullet(bulletX, bulletY)
    bulletY -= bulletY_change

  player(playerX, playerY) # PLAYER IS CALLED HERE TO MAKE IT APPEAR ABOVE BACKGROUND
  show_score(textX, textY)
  pygame.display.update()

