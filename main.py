import pygame
from pygame.locals import *
from time import *
import random
size=40

class apple :
    def __init__(self,parent_screen):
        self.image=pygame.image.load('apple.jpg').convert()
        self.parent_screen=parent_screen
        self.y=size*3
        self.x=size*3
    def draw(self):

        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()
    def move(self):
        self.x=random.randint(1,20)*size
        self.y=random.randint(1,15)*size





class Snake:
    def __init__(self,parent_screen,length):
        self.length=length
        self.parent_screen=parent_screen
        self.block = pygame.image.load("block.jpg").convert()
        self.x = [40]
        self.y = [40]
        self.direction='right '

    def increase_len(self):
        self.length+=1
        self.x.append(-1)
        self.y.append(-1)
    def draw(self):

        for i in range(self.length):
         self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()
    def move_up(self):
        self.direction='up'

    def move_down(self):
        self.direction='down'

    def move_left(self):
        self.direction='left'
    def move_right(self):
        self.direction='right'
    def walk(self):
        for i in range(self.length-1,0,-1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]


        if self.direction=='up':
            self.y[0]-=size

        if self.direction=='down':
            self.y[0]+=size

        if self.direction=='left':
            self.x[0]-=size

        if self.direction=='right':
            self.x[0]+=size
        self.draw()



class Game:
    def __init__(self):

        pygame.init()
        pygame.mixer.init()
        self.surface = pygame.display.set_mode((1000, 800))
        self.background()
        self.play_bckground()
        self.snake=Snake(self.surface,1)
        self.snake.draw()
        self.apple=apple(self.surface)
        self.apple.draw()
    def background(self):
        bg=pygame.image.load("background.jpg").convert()
        self.surface.blit(bg,(0,0))
    def reset(self):
        self.snake=Snake(self.surface,1)
        self.apple=apple(self.surface)
    def is_collide(self,x1,y1,x2,y2):
        if x1>=x2 and x1<size+x2:
            if y1>=y2 and y1<y2+size :
                return True

        return False
    def play_bckground(self):
        pygame.mixer.music.load("bg.mp3")
        pygame.mixer.music.play(-1,0)
    def display_score(self):
        self.font=pygame.font.SysFont('arial',30)
        score=self.font.render(f"score:{self.snake.length}",True,(245,245,245))
        self.surface.blit(score,(850,10))
    def play_sound(self,sound):
        sound = pygame.mixer.Sound(f"{sound}.mp3")
        pygame.mixer.Sound.play(sound)



    def play(self):
         self.background()
         self.snake.walk()
         self.apple.draw()
         self.display_score()

         pygame.display.flip()
         #snake_collide_with_apple
         if  self.is_collide(self.snake.x[0],self.snake.y[0],self.apple.x,self.apple.y):
             self.apple.move()
             self.play_sound("ding")


             self.snake.increase_len()
         #snake_collide_with_itself
         for i in range(2, self.snake.length):
            if self.is_collide(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound('crash')
                raise
         if self.snake.x[0]==0 or self.snake.y[0]==0 or self.snake.y[0]==800 or self.snake.x[0]==1000:
                self.play_sound('crash')
                raise
    def  show_game_over(self):
        bg = pygame.image.load("bg_image.jpg").convert()
        self.surface.blit(bg, (0, 0))
        pygame.mixer.music.pause()
        line1=self.font.render(f"GAME OVER! YOUR SCORE {self.snake.length}",True,(245,245,245))
        self.surface.blit(line1, (300, 350))
        line2=self.font.render(f"PRESS ENTER TO ",True,(200,230,245))

        self.surface.blit(line2, (300, 400))
        pygame.display.flip()

    def run(self):
        running = True
        pause=False
        while running:

            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key==K_RETURN:
                         pygame.mixer.music.unpause()
                         pause=False
                    if not pause :
                       if event.key == K_UP:
                        self.snake.move_up()
                       elif event.key == K_DOWN:
                        self.snake.move_down()
                       elif event.key == K_LEFT:
                        self.snake.move_left()
                       elif event.key == K_RIGHT:
                        self.snake.move_right()

                elif event.type == QUIT:
                    running = False
            try:
               if not pause :
                self.play()
            except Exception as e:
                self.show_game_over()
                pause =True
                self.reset()
            sleep(0.2)

if __name__=="__main__":

    game=Game()
    game.run()


    pygame.display.flip()


