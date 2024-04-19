from pygame import *
from pygame import draw as py_draw
from random import randint
from time import sleep

font.init()
font1 = font.Font(None, 36)
bigfont = font.Font(None, 60)
player_1_score = 0
player_2_score = 0
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
    def __init__(self, player_image,player_speed, player_x = w/2, player_y= h/2, w = 50, h = 50, pause = 0):
        self.image = transform.scale(image.load(player_image).convert_alpha(), (w, h))
        self.player_speed_x = player_speed
        self.player_speed_y = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.pause = pause

    def update(self, player_x = w/2, player_y = h/2):
        if self.rect.y < 0 or self.rect.y > h- 50:
            self.player_speed_y = 0 - self.player_speed_y
        self.rect.x += self.player_speed_x
        self.rect.y += self.player_speed_y
        global player_1_score, player_2_score, cont
        
        if self.rect.x < 0:
            window.blit(cont, (200, h/2))
            if self.pause == 0:
                player_2_score += 1
                self.pause = 1
                
            for e in event.get():
                if e.type == KEYDOWN:
                    if e.key == K_SPACE:
                        self.rect.x = player_x
                        self.rect.y = player_y
                        self.pause = 0
                        self.player_speed_x = 5
                        self.player_speed_y = 5
                        
        if self.rect.x > w:
            window.blit(cont, (200, h/2))
            if self.pause == 0:
                player_1_score += 1
                self.pause = 1

            for e in event.get():
                if e.type == KEYDOWN:
                    if e.key == K_SPACE:
                        self.rect.x = player_x
                        self.rect.y = player_y
                        self.pause = 0
                        self.player_speed_x = 5
                        self.player_speed_y = 5
                        
    def rocket_c(self):
        self.player_speed_x = 0 - self.player_speed_x

    def faster(self):
        self.player_speed_x = self.player_speed_x * 1.001
        self.player_speed_y = self.player_speed_y * 1.001




background = transform.scale(image.load('table.jpg'), (w, h))


#mixer.init()
#mixer.music.load('space.ogg')
#mixer.music.set_volume(0.5)
#mixer.music.play()
#kick = mixer.Sound('fire.ogg')
#shotsound = mixer.Sound('shot.ogg')

left_lox = Hero('rocket.png', 50, h/2 , 10, 80, 100, 'left')
right_lox = Hero('rocket.png', w - 125, h/2 , 10, 80, 100, 'right')
ball = Ball('ball.png', 2)


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
        cont = bigfont.render('Нажмите ПРОБЕЛ чтобы продолжить', True, (255, 0, 0))
        score = font1.render(f'счёт: {player_1_score} : {player_2_score}', True, (255, 0, 0))
        window.blit(score, (0, 0))
        left_lox.update()
        left_lox.reset()
        right_lox.update()
        right_lox.reset()
        ball.reset()
        ball.update()
        if sprite.collide_rect(left_lox, ball) or sprite.collide_rect(right_lox, ball):
            ball.rocket_c()

        
        ball.faster()


        
            
            
            
        ticks += 1
    display.update()
        
    clock.tick(60)
