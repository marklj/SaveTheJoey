import pygame, sys, os, random
from pygame.locals import *

print 'starting game...'
spriteClock = pygame.time.Clock()

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
        self.image, self.rect = load_image('ball.png', 1)
        self.pos = [5,7]
        self.original = self.image
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        
    def resetPos(self):
        self.pos = [5,7]
        #decrease life or score
        
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
        hitbox = self.rect.inflate(-10,0)
        for i in range(0, len(cars)):
            if(hitbox.colliderect(cars[i].rect) and self.rect != cars[i].rect):
                self.resetPos()
        screenPos = (((self.pos[0]*100)+10),((self.pos[1]*100)+10))
        self.rect.left = screenPos[0]
        self.rect.top = screenPos[1]
        

class Car(pygame.sprite.Sprite):
    def __init__(self, lane = None, speed = None):
        self.wait = random.randrange(400)
        if lane != None:
            if lane > 3:
                self.lane = 3
            else:
                self.lane = lane
        else:
            self.lane = random.randrange(3)
        if speed != None:
            self.speed = speed
        else:
            self.speed = (self.lane+2)*2
        pygame.sprite.Sprite.__init__(self) #call sprite initializer
        self.image, self.rect = load_image('ball.png', -1)
        self.original = self.image
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.laneOffset = 710 - (self.lane*100)
        newpos = self.rect.move((-100, self.laneOffset))
        self.rect = newpos

    def resetPos(self, obj = None):
        if obj == None:
            obj = self
        obj.rect.left = -250
        #print 'moved'
        
    def update(self):
        if(self.wait > 0):
            newpos = self.rect.move((0, 0))
            self.wait -= 1
            self.rect = newpos
        elif (self.rect.right > self.area.right+200):
            newpos = self.rect.move((-1250, 0))
            self.wait = random.randrange(900)
            self.rect = newpos
        elif(self.rect.left > 10 and self.rect.left < 25):
            hitbox = self.rect.inflate(100, 0)
            newpos = self.rect.move((self.speed, 0))
            for i in range(0, len(cars)):
                if(hitbox.colliderect(cars[i].rect) and self.rect != cars[i].rect):
                    self.resetPos(cars[i])
                    cars[i].wait = random.randrange(200)
                else:
                    self.rect = newpos
        else:
            newpos = self.rect.move((self.speed, 0))
            self.rect = newpos
        
        
pygame.init()

bg, bgRect = load_image('bg.bmp')
screen = pygame.display.set_mode((1000, 800))
modes = pygame.display.list_modes(32)
if not modes:
    print '16 bit not supported'
else:
    print 'found resolution:', modes[0]
    #screen = pygame.display.set_mode(modes[0], FULLSCREEN, 32)
    
background = pygame.Surface(screen.get_size())
background = background.convert()
background.blit(bg, (0,0))

#init objs
av = A()
cars = []
allObj = [av]
for i in range(0,30):
    cars.append(Car(random.randrange(1,4)))
allObj.extend(cars)
allsprites = pygame.sprite.RenderPlain(allObj)
print allsprites
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

    screen.blit(background, (0,0))
    allsprites.draw(screen)
    av.update()
    for i in range(0,len(cars)):
        cars[i].update()
    pygame.display.flip()
    background.blit(bg, (0,0))