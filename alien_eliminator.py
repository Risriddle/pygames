import pygame
import math
import random
from pygame import mixer #to use all sorts of music in code
#initializing pygame
pygame.init()

#setting up the screen
screen=pygame.display.set_mode((800,600))

#background image
background=pygame.image.load("back.jpg")

#background music
mixer.music.load("background.wav") #mixer.music as the background sound is large but for small sounds like  bullet sound just use mixer.sound
mixer.music.play(-1) #-1 to play in loop

#changing title,adding icon logo
pygame.display.set_caption("Space Invaders")
icon=pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

#adding player and its position
playerImg=pygame.image.load("rock.png")
playerX=370
playerY=480
playerX_change=0

#adding enemy and its position,using lists for multiple enemies
enemyImg=[]
enemyX=[]
enemyY=[]
enemyX_change=[]
enemyY_change=[]
num_of_enemies=5
for i in range(num_of_enemies):
 enemyImg.append(pygame.image.load("enemy.png"))
 enemyX.append(random.randint(0,736))
 enemyY.append(random.randint(50,150))
 enemyX_change.append(3)
 enemyY_change.append(10)

#ready=bullet not on screen
#fire=bullet moves on the screen
#adding bullet and its position
bulletImg=pygame.image.load("bullet.png")
bulletX=0
bulletY=480
bulletX_change=0
bulletY_change=1
bullet_state="ready"

#score display 
score_value=0
font=pygame.font.Font("freesansbold.ttf",32) #this font is by default present in pygame to use other fonts download and place here,32 id font size(can use dafont website forloading fonts
textX=10
textY=10

def show_score(x,y):
 score=font.render("Score:" + str(score_value),True,(255,255,255))
 screen.blit(score,(x,y))

#game over display 
over_font=pygame.font.Font("freesansbold.ttf",70)

def game_over_text():
 over_text=over_font.render("GAME OVER",True,(255,255,255))
 screen.blit(over_text,(210,250))



#player function,to draw image of player we use blit function
def player(x,y):
 screen.blit(playerImg,(x,y))

#enemy function,to draw image of enemy we use blit functiondef enemy(x,y):
def enemy(x,y,i):
 screen.blit(enemyImg[i],(x,y))

#bullet function to draw bullets on screen when spacebar is pressed
def fire_bullet(x,y):
 global bullet_state
 bullet_state="fire"
 screen.blit(bulletImg,(x+16,y+10))

#to check the collision of the bullet and the enemy
def isCollision(enemyX,bulletX,enemyY,bulletY):
  distance=math.sqrt((math.pow(enemyX-bulletX,2))+(math.pow(enemyY-bulletY,2)))
  if distance<27:
   return True
  else:
   return False


#game loop
running=True
while running:

 for event in pygame.event.get():
  if event.type==pygame.QUIT:
    running=False

#checks whether key is pressed and then whether right or left and change the position of player accordingly
  if event.type==pygame.KEYDOWN:
    if event.key==pygame.K_LEFT:
      playerX_change= -0.2
    if event.key==pygame.K_RIGHT:
      playerX_change= 0.2
    if event.key==pygame.K_SPACE:
      if bullet_state=="ready":
       bullet_sound=mixer.Sound("laser.wav")
       bullet_sound.play()
       bulletX=playerX #to make the bullet to originate from the rocket but not follow it around
       fire_bullet(bulletX,bulletY)
  if event.type==pygame.KEYUP:
    if event.key==pygame.K_LEFT or  event.key==pygame.K_RIGHT:
      playerX_change= 0

 playerX+=playerX_change
 enemyX+=enemyX_change
#to keep player in boundary
 if playerX<=0:
  playerX=0
 elif playerX>=(800-64):
  playerX=736
 
#to move enemy in boundary
 for i in range(num_of_enemies):
 
  enemyX[i]+=enemyX_change[i]
  if enemyX[i]<=0:
   enemyX_change[i]=0.1
   enemyY[i]+=enemyY_change[i]
  elif enemyX[i]>=(800-64):
   enemyX_change[i]=-0.1
   enemyY[i]+=enemyY_change[i]

#to end game
  if enemyY[i]>=400:
    for j in range(num_of_enemies):
      enemyY[j]=2000
    game_over_text()
    break 

#collision
  collision=isCollision(enemyX[i],enemyY[i],bulletX,bulletY)
  if collision:
   explosion_sound=mixer.Sound("explosion.wav")
   explosion_sound.play()
   bulletY=480
   bullet_state="ready"
   score_value+=1
   print(score_value)
   enemyX[i]=random.randint(0,735)
   enemyY[i]=random.randint(50,150)

  enemy(enemyX[i],enemyY[i],i)



#bullet movement 
 if bullet_state=="fire":
   fire_bullet(bulletX,bulletY)
   bulletY-=bulletY_change
 if bulletY<=0:
   bulletY=480
   bullet_state="ready"

#calling player function in game loop,changing its position by passing values to function
 player(playerX,playerY)
 show_score(textX,textY)
 
#to update the screen constantly, comes in every game code,can use any of the two update or flip just take care of screen.fill right below it or hash it
 pygame.display.update()

#background image
 screen.blit(background,(0,0))
 #pygame.display.flip() 
#to colour the screen rgb values
 #screen.fill((0,0,0))


