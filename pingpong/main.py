from pygame import *
from pygame import draw as py_draw
from random import randint
from time import sleep

font.init()
font1 = font.Font(None, 36)
bigfont = font.Font(None, 60)

h = 600
w = 1200
window = display.set_mode((w, h))
display.set_caption('чиназес')

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, w = 50, h = 50):
        super().__init__()
        self.image = transform.scale(image.load(player_image).convert_alpha(), (w, h))
        self.player_speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Hero(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed, w = 50, h = 50, location = 'left'):
        self.location = location
        self.image = transform.scale(image.load(player_image).convert_alpha(), (w, h))
        self.player_speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    
    def update(self):
        keys = key.get_pressed()
        if self.location == 'left':
            if keys[K_w] and self.rect.y > 5:
                self.rect.y -= self.player_speed
            if keys[K_s] and self.rect.y < (h - 100):
                self.rect.y += self.player_speed

        else:
            if keys[K_UP] and self.rect.y > 5:
                self.rect.y -= self.player_speed
            if keys[K_DOWN] and self.rect.y < (h - 100):
                self.rect.y += self.player_speed



class Boom(sprite.Sprite):
    def __init__(self, ufo_center, boom_sprites, booms, loops_amount = 0) -> None:
        super().__init__() 
        #global booms, boom_sprites 
        self.loops_amount = loops_amount
        self.frames = boom_sprites        
        self.frame_rate = 1   
        self.frame_num = 0
        self.image = boom_sprites[0]
        self.rect = self.image.get_rect()
        self.rect.center = ufo_center
        self.add(booms)
    
    def next_frame(self):
        self.image = self.frames[self.frame_num]
        self.frame_num += 1  
        
    
    def update(self):
        if self.loops_amount == 0:
            self.next_frame()
            if self.frame_num == len(self.frames)-1:
                self.kill()
        else:
            self.rect.y += 2
            if self.rect.y > h:
                self.kill()
            else:
                self.next_frame()
                if self.frame_num == len(self.frames)-1:
                    self.frame_num = 0
                



            
def sprites_load(folder, file_name, size, colorkey):    
    sprites = []
    load = True
    num = 1
    while load:
        try:
            spr = image.load(f'{folder}\\{file_name}{num}.png')
            spr = transform.scale(spr,size)
            if colorkey: spr.set_colorkey((0,0,0))
            sprites.append(spr)
            num += 1
        except:
            load = False
    return sprites

class Ball(GameSprite):
    def __init__(self, player_image,player_speed, player_x = w/2, player_y= h/2, w = 50, h = 50,):
        self.image = transform.scale(image.load(player_image).convert_alpha(), (w, h))
        self.player_speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    
    def update(self):
        self.rect.x += self.player_speed
        self.rect.y += self.player_speed




background = transform.scale(image.load('table.jpg'), (w, h))


#mixer.init()
#mixer.music.load('space.ogg')
#mixer.music.set_volume(0.5)
#mixer.music.play()
#kick = mixer.Sound('fire.ogg')
#shotsound = mixer.Sound('shot.ogg')

left_lox = Hero('rocket.png', 0, h/2 , 10, 80, 100, 'left')
right_lox = Hero('rocket.png', w - 75, h/2 , 10, 80, 100, 'right')
ball = Ball('ball.png', 5)


clock = time.Clock()
ticks = 0
play = True

finish = False
win = False
while play:
    
    for e in event.get():
        if e.type == QUIT:
            play = False

        if e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                play = False
        
        

    
    if not finish:
        window.blit(background, (0, 0))
        left_lox.update()
        left_lox.reset()
        right_lox.update()
        right_lox.reset()


        
            
            
            
        
        display.update()
        ticks += 1
    clock.tick(60)
