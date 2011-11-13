import pygame, sys, os
from pygame.locals import *

if not pygame.font:
    print 'Warning: Fonts disabled'
if not pygame.mixer:
    print 'Warning: Sound disabled'
    
def load_image(name, colorkey=None):
    fullname = os.path.join('data/img', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', name
        raise SystemExit, message
    image = image.convert()
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

class Fist(pygame.sprite.Sprite):
    """Moves a clenched fist on the screen, following the mouse"""
    def __init__ (self):
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        self.image, self.rect = load_image('fist.bmp', -1)
        self.punching = False
        
    def update(self):
        "Move the fist based on the mouse position"
        pos = pygame.mouse.get_pos()
        self.rect.midtop = pos
        if self.punching:
            self.rect.move_ip(5, 10)
        
    def punch(self, target):
        "returns true if the fist collides with a target"
        if not self.punching:
            self.punching = True
            hitbox = self.rect.inflate(-5, -5)
            print hitbox.colliderect(target.rect)
            return hitbox.colliderect(target.rect)
        
    def unpunch(self):
        "called to pull the fist back"
        self.punching = False
        
class Car(pygame.sprite.Sprite):
    """moves a monkey critter across the screen. it can spin the monkey when it is punched."""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #call sprite initializer
        self.image, self.rect = load_image('chimp.bmp', -1)
        self.original = self.image
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.move = -9
        self.dizzy = 0
        
    def update(self):
        "Walk or spin, depending on the monkey's state"
        if self.dizzy:
            self._spin()
        else:
            self._walk()
    
    def _walk(self):
        "move monkey across the screen, and turn at the ends"
        newpos = self.rect.move((self.move, 0))
        if not self.area.contains(newpos):
            if self.rect.left < self.area.left-200 or self.rect.right > self.area.right+200:
                #self.move = -self.move
                newpos = self.rect.move((800, 0))
                #self.image = pygame.transform.flip(self.image, 1, 0)
            self.rect = newpos
            
    def _spin(self):
        "spin the monkey image"
        center = self.rect.center
        self.dizzy += 12
        if self.dizzy>= 360:
            self.dizzy = 0
            self.image = self.original
        else:
            rotate = pygame.transform.rotate
            self.image = rotate(self.original, self.dizzy)
        self.rect = self.image.get_rect(center=center)
        
    def punched(self):
        "this will cause the monkey to start spinning"
        if not self.dizzy:
            self.dizzy = 1
            self.orginal = self.image
    
           
pygame.init()
screen = pygame.display.set_mode((468, 78))
pygame.mouse.set_visible(0)

background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((250, 250, 250))

if pygame.font:
    font = pygame.font.Font(None, 36)
    text = font.render("Pummel the Chimp, and Win $$$", 1, (10, 10, 10))
    textpos = text.get_rect(centerx=background.get_width()/2)
    background.blit(text, textpos)
    
screen.blit(background, (0,0))
pygame.display.flip()

whiff_sound = load_sound('whiff.wav')
punch_sound = load_sound('punch.wav')
car = Car()
fist = Fist()
allsprites = pygame.sprite.RenderPlain((fist, car))
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
        elif event.type == MOUSEBUTTONDOWN:
            if fist.punch(car):
                punch_sound.play()
                car.punched()
            else:
                whiff_sound.play()
        elif event.type == MOUSEBUTTONUP:
            fist.unpunch()
    
    allsprites.update()
    
    screen.blit(background, (0, 0))
    allsprites.draw(screen)
    pygame.display.flip()
    
    
