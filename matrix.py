import pygame, sys, os
from pygame.locals import *

print 'starting game...'

class Grid(pygame.sprite.Sprite):
    def make_grid(self, loc):
        self.x = loc[0]
        self.y = loc[1]
        r = ""
        for i in range(0,6):
            for j in range(0,10):
                if(i==self.y and j==self.x):
                    r += "%"
                else:
                    r += "+"
        return r

class A(pygame.sprite.Sprite):
    def __init__(self):
        self.pos = [5,5]
    def move(self, direction):
        if(direction=='n'):
            self.pos[1] -= 1
        elif(direction=='s'):
            self.pos[1] += 1
        elif(direction=='e'):
            self.pos[0] += 1
        elif(direction=='w'):
            self.pos[0] -= 1
        return self.pos
    
pygame.init()
screen = pygame.display.set_mode((500, 500))
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((250, 250, 250))

#init objs
grid = Grid()
av = A()
clock = pygame.time.Clock()

while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            pygame.quit()
            sys.exit
        elif event.type == KEYDOWN and event.key == K_UP:
            av.move('n')
        elif event.type == KEYDOWN and event.key == K_DOWN:
            av.move('s')
        elif event.type == KEYDOWN and event.key == K_RIGHT:
            av.move('e')
        elif event.type == KEYDOWN and event.key == K_LEFT:
            av.move('w')
    if pygame.font:
        font = pygame.font.Font(None, 36)
        gridText = grid.make_grid(av.pos)
        for i in range(0,60,10):
            start = i
            end = i+10
            text = font.render(gridText[start:end], 1, (10, 10, 10))
            textpos = (10, i*2)
            background.blit(text, textpos)
    screen.blit(background, (0,0))
    pygame.display.flip()
    background.fill((250, 250, 250))
