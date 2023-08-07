# conversion of code in p5 to OOPs ie code with classes and objects
import time
import pygame
import math
from pygame.locals import *
import random

size=32 #size of one snake block
#initial of length of snake is passed 2
background_color=(0,255,0)


class Apple:
  def __init__(self,parent_screen):
     self.parent_screen=parent_screen
     self.apple_x=size*3
     self.apple_y=size*3  #initially at some position and multiple of size because of size of block of snake and apple are equal and this is essential for their allignment
     self.apple=pygame.image.load("food.png").convert() 
  def draw(self):
     #only once appleis drawn (after that randomly to new location) so no need to clear screen
     self.parent_screen.blit(self.apple,(self.apple_x,self.apple_y)) 
     pygame.display.update()
  def move(self):
     self.apple_x=random.randint(0,25)*size  #1000/32=31.25  ie can move this many places horizontally
     self.apple_y=random.randint(0,15)*size  #800/32=25 #this way number remains between 1000 and 800


class Snake:
  def __init__(self,parent_screen,length): #its a CONSTRUCTOR  # as we need a screen to draw the snake and that screen is present in another class so take it as an argument from there
     self.parent_screen=parent_screen #to create a parent_screen member of the class snake
     self.length=length #in order tomake a snake (right noew snake length is one ie only one block)# now eg length=5 then there are 5 x,y coordinates corresponding to each edge(list)
     self.block_x=[size]*length #ie size of one block x number of blocks 
     self.block_y=[size]*length
     #self.block_x=0
     #self.block_y=0
     self.block=pygame.image.load("square.png").convert()
     self.direction=""
  def draw(self):
    self.parent_screen.fill(background_color) # to clear screen and remove previous blocks
    # (for one block) self.parent_screen.blit(self.block,(self.block_x,self.block_y)) # to display block on the screen
    for i in range(self.length): #for more than one blocks
       self.parent_screen.blit(self.block,(self.block_x[i],self.block_y[i])) 
    pygame.display.update()
   
  def move_left(self): #self is an instance of classes in python used to access its members
   # self.block_x-=10 no need to write this here now as they are defined in walk function
    self.direction="left"
    
  
  def move_right(self): 
    self.direction="right"
   

  def move_up(self): 
    self.direction="up"


  def move_down(self): 
    self.direction="down"
 
 
  def walk(self): 

    for i in range(self.length-1,0,-1):
        self.block_x[i]=self.block_x[i-1]
        self.block_y[i]=self.block_y[i-1]

    if self.direction=="up":
      self.block_y[0]-=size #as the size of one block is 32 so we need to keep them 32 much apart to avoid overlap # head moves in the same way for other blocks 2nd block takes position of first and 3rd of 2nd and so on use a reverse for loop

    if self.direction=="down": # here only[0] as we need to move just the head the rest of the blocks just need to take position of the previous block
      self.block_y[0]+=size
     
    if self.direction=="left":
      self.block_x[0]-=size
    
    if self.direction=="right":
      self.block_x[0]+=size

    self.draw()
  
  def increase_length(self):
        self.length+=1
        self.block_x.append(-1)
        self.block_y.append(-1) #any random value just to add new length
  
  #def snake_speed(self):
   #     if self.length>2:
    #     time.sleep(0.3)
     #  if self.length>4:
     #     time.sleep(0.2)
      #  if self.length>6:
       #    time.sleep(0.1) 
     

class Game:
   def __init__(self): # init has to be included in all classes for pygame library initialization
      pygame.init() #game initialization
      pygame.mixer.init() #mixer module for sound initialized
      self.play_background_music()
      self.surface=pygame.display.set_mode((1000,800)) # making surface member of class game by using self
      self.surface.fill(background_color)
      self.snake=Snake(self.surface,1)  # making object snake of class Snake  as the snake is part of the game so we are making its object inside game class
                                      # constructor of snake takes two parameters so pass those
      self.snake.draw() # to draw the snake
      self.apple=Apple(self.surface) #object of Apple class
      self.apple.draw()

   def play_background_music(self):
      pygame.mixer.music.load("Snake Game - Theme Song.mp3")  #music=long time vs Sound=one time
      pygame.mixer.music.play(loops=-1) #to play music infinitely in a loop


   def play_sound(self,sound):
       sound=pygame.mixer.Sound(f"{sound}.mp3")
       pygame.mixer.Sound.play(sound) # to avoid repetition of lines made a function
    
   def play(self):
       
       self.snake.walk() #for making the snake keep moving once a key is pressed ie keys are only used for changing the direction # this function is too user defined and we use timer in it

       self.apple.draw() #as in walk function draw of snake is called and in  draw of snake we are clearing the screen
       self.display_score()
       pygame.display.update()
        
       #snake colliding with itself
       for i in range(3,self.snake.length): #start from three as head can't collide to 2nd and 3rd part
         if self.is_Collision(self.snake.block_x[0],self.snake.block_y[0],self.snake.block_x[i],self.snake.block_y[i]): #checking the collision of head with rest of the body starting from 3
           self.play_sound("collision")
           # print("game over")
           #exit(0) # this works but instead of this we will use the concept of exception and we will give the player some option to replay the game
           raise "Game over" #raising exception means something unusual happened and we want to go out of the game
       
        #snake colliding with apple
       if self.is_Collision(self.snake.block_x[0],self.snake.block_y[0],self.apple.apple_x,self.apple.apple_y):
          self.play_sound("apple-munch-40169")
          self.snake.increase_length()
          #self.snake_speed() #to increase snake's speed after each collision
          self.apple.move() #ie move the apple to a random location once eaten
       
       # boundary conditions  
       if self.snake.block_x[0]<=0 or self.snake.block_x[0]>=1000 or self.snake.block_y[0]<=0 or self.snake.block_y[0]>=800:
           self.play_sound("collision")
           raise "Game over"

          
   def is_Collision(self,x1,y1,x2,y2): #for when head of snake touches the apple ie snake eats the apple
       
      # distance=math.sqrt((math.pow(x1-x2,2))+(math.pow(y1-y2,2)))
      # if distance<32:
       #  return True
        #else:
         #return False
        if x1>= x2 and x1 <x2+size:
            if y1 >=y2 and y1<y2+size:
                return True
        return False

   def display_score(self):
      font=pygame.font.SysFont("arial",30)
      score=font.render(f"SCORE:{self.snake.length}",True,(0,0,0)) #colour of score
      self.surface.blit(score,(800,10))

   def show_game_over(self):
          self.surface.fill(background_color) #need to clear the screen first and try to use variables when something has to be done again and again
          font=pygame.font.SysFont("arial",25)
          line1=font.render(f"Game is OVER : your score is :{self.snake.length}",True,(0,0,0))
          self.surface.blit(line1,(200,300))
          line1=font.render(f"To play again press ENTER and to exit press ESCAPE",True,(0,0,0))
          self.surface.blit(line1,(200,350))
          
          pygame.mixer.music.pause()
          pygame.display.update()

   def reset(self):
       self.snake=Snake(self.surface,1) #to redraw thw snake with length 1 
       self.apple=Apple(self.surface)


   def run(self):
     running =True
     pause=False
     while running:
       for event in pygame.event.get(): #event loop used in every UI programming waiting for user input
         if event.type==KEYDOWN:
           if event.key==K_ESCAPE: # to exit the game on pressing exit
             running=False
           if event.key==K_RETURN: # to restart the game on pressing enter
              pygame.mixer.music.unpause() #built in function to unpause music when game restarts     
              pause=False
#  to move block up down right left 
           if not pause:
             if event.key==K_UP: 
               self.snake.move_up() 

             if event.key==K_DOWN:
              self.snake.move_down()

             if event.key==K_RIGHT:
              self.snake.move_right() #using function instead of block_x variable to make code readable  # these are not built in methods we need to create them

             if event.key==K_LEFT:
               self.snake.move_left()
      

         elif event.type==QUIT: #for leaving the game or closing the window using cross
             running =False

#outside for loop but inside while
       try: 
        if not pause: #not playing the game if its paused ie exception has occurred # done to display the lost message and stop the game there
          self.play() #to make the snake move and draw the apple
       except Exception as e:
            self.show_game_over()
            pause=True
            self.reset() #to reset the score to 0 after loosing and when game resttarts
        #self.snake.snake_speed()
       time.sleep(0.2)















#code starts executing from here
if __name__=="__main__":
 
 game=Game() #object of class Game
 game.run()
