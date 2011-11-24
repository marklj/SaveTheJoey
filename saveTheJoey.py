import pygame, sys, os, random
from pygame.locals import *

print 'starting game...'
spriteClock = pygame.time.Clock()

level = 0


def load_image(name, colorkey=None, alpha = False):
    fullname = os.path.join('data/img', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', name
        raise SystemExit, message
    if alpha:
        image = image.convert_alpha()
    else:
        image = image.convert(32)
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey,RLEACCEL)
    return image, image.get_rect()
def load_sound(name):
    class NoneSound:
        def play(self): pass
    if not pygame.mixer:
        return NoneSound
    fullname = os.path.join('data/sound', name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error, message:
        print 'Cannot load sound file:', name
        raise SystemExit, message
    return sound
def resetGame(diff = 0):
    if diff == 1:
        stat.lives = 3
        stat.carNum = 10
        stat.logNum = 15
        stat.active = True
    elif diff == 2:
        stat.lives = 2
        stat.carNum = 30
        stat.logNum = 15
        stat.active = True
    elif diff == 3:
        stat.lives = 1
        stat.carNum = 50
        stat.logNum = 5
        stat.active = True
    else:
        stat.lives = 3
        stat.carNum = 0
        stat.logNum = 0
        stat.active = False
    stat.score = 0
    
class Stat():
    def __init__(self, startLives=3):
        self.lives = startLives
        self.level = 1
        self.score = 0
        self.carNum = 10
        self.logNum = 15
        self.active = True
        
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
        self.image, self.rect = load_image('joey.png', -1, True)
        self.trans, self.trasRect = load_image('trans.png', -1, True)
        self.image_orig = self.image
        self.pos = [5,7]
        self.original = self.image
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.offLog = 0
        
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
        self.image = self.image_orig
        hitbox = self.rect.inflate(-10,0)
        #if object hits another car...
        for i in range(0, len(cars)):
            if(hitbox.colliderect(cars[i].rect) and self.rect != cars[i].rect):
                self.resetPos()
                stat.lives -= 1
                stat.score -= 250
            else:
                screenPos = (((self.pos[0]*100)+10),((self.pos[1]*100)+10))
                self.rect.left = screenPos[0]
                self.rect.top = screenPos[1]
        for i in range(len(logs)):
            logs[i].removeJoey()
        if self.pos[1] == 1 or self.pos[1] == 2:
            self.image = self.trans
            hitbox = self.rect.inflate(10,0)
            if self.rect.collidelist(logs) != -1:
                i = self.rect.collidelist(logs)
                self.pos[0] = (logs[i].rect.left + (logs[i].rect.left % 100))/100
                self.rect = self.rect.fit(logs[i].rect)
                logs[i].addJoey()
            else:
                self.resetPos()
                stat.lives -= 1
                stat.score -= 250
                        
        elif self.pos[1] == 0:
            stat.score += 1000*level
            print stat.score
            self.resetPos()
            self.offLog = 0

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
        num = random.randrange(5)+1
        self.image, self.rect = load_image('car'+ str(num) + '.png', -1, True)
        self.original = self.image
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.laneOffset = 710 - (self.lane*100)
        newpos = self.rect.move((-650, self.laneOffset))
        self.rect = newpos

    def resetPos(self, obj = None):
        if obj == None:
            obj = self
        obj.rect.left = -650
        
    def update(self):
        if(self.wait > 0):
            newpos = self.rect.move((0, 0))
            self.wait -= 1
            self.rect = newpos
        elif (self.rect.right > self.area.right+200):
            #newpos = self.rect.move((-1250, 0))
            self.resetPos(self)
            self.wait = random.randrange(900)
            #self.rect = newpos
        elif(self.rect.left > -400 and self.rect.left < -200):
            hitbox = self.rect.inflate(100, 0)
            newpos = self.rect.move((self.speed, 0))
            collideInd = hitbox.collidelistall(cars)
            if((collideInd != []) and self.rect != cars[collideInd[0]]):
                for i in range(0, len(cars)-1):
                    #print i
                    if i in collideInd:
                        #check if is same car as self
                        if self.rect != cars[i].rect:
                            cars[i].wait = random.randrange(200)
                            self.resetPos(cars[i])
                        
                
            else:
                self.rect = newpos
        else:
            #waiting...
            newpos = self.rect.move((self.speed, 0))
            self.rect = newpos
        
        

class Log(pygame.sprite.Sprite):
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
        self.image, self.rect = load_image('log.png', -1, True)
        self.filled, self.filledRect = load_image('logFilled.png', -1, True)
        self.original = self.image
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.laneOffset = 210 - (self.lane*100)
        newpos = self.rect.move((1250, self.laneOffset))
        self.rect = newpos
    def addJoey(self):
        self.image = self.filled
    def removeJoey(self):
        self.image = self.original
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
        elif (self.rect.left < self.area.left-200):
            newpos = self.rect.move((1250, 0))
            self.wait = random.randrange(900)
            self.rect = newpos
        elif(self.rect.left > 900 and self.rect.left < 1000):
            hitbox = self.rect.inflate(100, 0)
            newpos = self.rect.move((self.speed*-1, 0))
            for i in range(0, len(logs)-1):
                #print i
                if(hitbox.colliderect(logs[i].rect) and self.rect != logs[i].rect):
                    self.resetPos(logs[i])
                    logs[i].wait = random.randrange(100)
                else:
                    self.rect = newpos
        else:
            newpos = self.rect.move((self.speed*-1, 0))
            self.rect = newpos
            
        return self.speed
        
while True:      
    pygame.init()
    #pygame.mouse.set_visible(0)


    bg, bgRect = load_image('bg.bmp')
    screen = pygame.display.set_mode((1000, 800))
    modes = pygame.display.list_modes(32)
    splash, splashRect = load_image('splash.png', -1, True)
    
    if not modes:
        False
        #print '16 bit not supported'
    else:
        #print 'found resolution:', modes[0]
        #screen = pygame.display.set_mode(modes[0], FULLSCREEN, 32)
        False
        
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.blit(bg, (0,0))
    
    
    #init objs
    stat = Stat()
    resetGame(level)

    av = A()
    cars = []
    logs = []
    allObj = [av]
    for i in range(0, stat.carNum):
        cars.append(Car(random.randrange(1,4)))
    for i in range(0, stat.logNum):
        logs.append(Log(random.randrange(0,2)))
    allObj.extend(cars)
    allObj.extend(logs)
    allsprites = pygame.sprite.RenderPlain(allObj)

        
        
    clock = pygame.time.Clock()
    gameClock = pygame.time.Clock()
    time = 0
    topscore = open('topscore', 'r')
    highscore = topscore.read()
    topscore.close()
    print highscore
    fileWrite = False;
    highScoreTxt = ""

    go = 1
    while go == 1:
        clock.tick(60)
        if stat.active:
            gameClock.tick(60)
            time += gameClock.get_time()
        bounce_sound = load_sound('bounce.wav')
        for event in pygame.event.get():
            #print av.pos
            if event.type == QUIT:
                pygame.quit()
                sys.exit
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                sys.exit
            elif event.type == KEYDOWN and event.key == K_RETURN:
                level = 0
                resetGame()
                go = 0
            elif event.type == KEYDOWN and event.key == K_1:
                level = 1
                resetGame(1)
                print 1
                go = 0
            elif event.type == KEYDOWN and event.key == K_2:
                level = 2
                print level
                resetGame(2)
                go = 0
            elif event.type == KEYDOWN and event.key == K_3:
                level = 3
                resetGame(3)
                go = 0
            elif event.type == KEYDOWN and event.key == K_UP and stat.active == True and time > 3000:
                #bounce_sound.play()
                av.move('n')
            elif event.type == KEYDOWN and event.key == K_DOWN and stat.active == True and time > 3000:
                av.move('s')
            elif event.type == KEYDOWN and event.key == K_RIGHT and stat.active == True and time > 3000:
                av.move('e')
            elif event.type == KEYDOWN and event.key == K_LEFT and stat.active == True and time > 3000:
                av.move('w')

        screen.blit(background, (0,0))
        allsprites.draw(screen)
        
        av.update()
        for i in range(0,len(cars)):
            cars[i].update()
        for i in  range(0,len(logs)):
            logs[i].update()
        pygame.display.flip()
        background.blit(bg, (0,0))
        if pygame.font:
            font = pygame.font.Font(None, 48)
            statsTxt = font.render("Lives: " + str(stat.lives), 1, (10, 10, 10))
            background.blit(statsTxt, (15, 725))
            statsTxt = font.render("Score: " + str(stat.score), 1, (10, 10, 10))
            background.blit(statsTxt, (15, 755))

        if stat.lives < 1:
            stat.active = False
            
            if not fileWrite:
                #compare score to top score
                if highscore != "" and int(highscore) < stat.score:
                    topscore = open('topscore', 'w')
                    topscore.write(str(stat.score))
                    topscore.close()
                    highScoreTxt =  "New high score: " + str(stat.score)
                elif highscore == "":
                    topscore = open('topscore', 'w')
                    topscore.write(str(stat.score))
                    topscore.close()
                    highScoreTxt = "New high score: " + str(stat.score)
                else:
                    highScoreTxt = "You did not break the high score!"
                fileWrite = True
                topscore.close()
            
            if pygame.font:
                font = pygame.font.Font(None, 72)
                loseTxt = font.render("Game Over!", 1, (10, 10, 10))
                textpos = loseTxt.get_rect(centerx=background.get_width()/2)
                background.blit(loseTxt, (textpos.left, 20))
                font = pygame.font.Font(None, 55)
                loseTxt = font.render(highScoreTxt, 1, (10, 10, 10))
                textpos = loseTxt.get_rect(centerx=background.get_width()/2)
                background.blit(loseTxt, (textpos.left, 60))
                

        #blit the game countdown
        if pygame.font and stat.active and time < 5000:
            font = pygame.font.Font(None, 72)
            if time > 3000 and time < 5000:
                countTxt = font.render("Go!", 1, (77, 140, 38))
            elif time > 2000:
                countTxt = font.render("1", 1, (255, 10, 10))
            elif time > 1000:
                countTxt = font.render("2", 1, (255, 10, 10))
            elif time > 0 and time < 999 :
                countTxt = font.render("3", 1, (255, 10, 10))
            else:
                countTxt = font.render("", 1, (10, 10, 10))
            textpos = countTxt.get_rect(centerx=background.get_width()/2)
            background.blit(countTxt, (textpos.left, 20))
                
        if not stat.active:
            background.blit(splash, (200,100))
