import pygame, sys, os
from pygame.locals import *

print 'starting game...'

def load_image(name, colorkey=None):
    fullname = os.path.join('data/img', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', name
        raise SystemExit, message
    image = image.convert(32)
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey,RLEACCEL)
    return image, image.get_rect()

class Grid(pygame.sprite.Sprite):
    def make_grid(self, loc):
        self.x = loc[0]
        self.y = loc[1]
        r = ""
        for i in range(0,8):
            for j in range(0,10):
                if(i==self.y and j==self.x):
                    r += "%"
                else:
                    r += "+"
        return r

class A(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        self.image, self.rect = load_image('fist.bmp', -1)
        self.pos = [5,7]
    def move(self, direction):
        if(direction=='n' and self.pos[1] != 0):
            self.pos[1] -= 1
        elif(direction=='s' and self.pos[1] != 7):
            self.pos[1] += 1
        elif(direction=='e' and self.pos[0] != 9):
            self.pos[0] += 1
        elif(direction=='w' and self.pos[0] != 0):
            self.pos[0] -= 1
        return self.pos
    def update(self):
        
pygame.init()

bg, bgRect = load_image('bg.bmp')
screen = pygame.display.set_mode((1000, 800))
background = pygame.Surface(screen.get_size())
background = background.convert()
background.blit(bg, (0,0))

#init objs
grid = Grid()
av = A()
allsprites = pygame.sprite.RenderPlain((av))
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
        font = pygame.font.Font(None, 96)
        gridText = grid.make_grid(av.pos)
        for i in range(0,80,10):
            start = i
            end = i+10
            text = font.render(gridText[start:end], 1, (10, 10, 10))
            textpos = (10, i*10)
            background.blit(text, textpos)
    screen.blit(background, (0,0))
    allsprites.draw(screen)
    pygame.display.flip()
    background.blit(bg, (0,0))
