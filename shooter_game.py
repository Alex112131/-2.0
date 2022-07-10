#Створи власний Шутер!

from pygame import *
from random import randint
from time import time as timer


mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
"""mixer.music.set_volum(0.5)"""
fire_sound = mixer.Sound('fire.ogg')

time_one = timer()
time_run = 5

win_width = 1080
win_height = 700
window = display.set_mode((win_width, win_height))
display.set_caption('Space RobotoShooter')  
background = transform.scale(image.load('1625176070_57-kartinkin-com-p-stalker-fon-krasivie-foni-65.jpg'), (win_width, win_height))

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 80:
            self.rect.y += self.speed
    def fire(self):
        bullet = Bullet('bullets_PNG.png', self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed, lives):
        super().__init__(player_image, player_x, player_y, size_x, size_y, player_speed)
        self.lives = lives
    def update(self):
        self.rect.y += randint(-3,3)
        self.rect.x += self.speed
        global lost, fire_voron, last_timeVorona, score
        if self.rect.x > 980:
            self.rect.y = randint(50,800)
            self.rect.x = 0
            lost += 1
        if fire_voron:
            fire_sound.play()
            am_list = monsters.sprites()
            b = am_list[randint(0, len(am_list) - 1)]
            bullet = Bullet('Steel-Silver.png', b.rect.x, b.rect.y, 35, 20, 15)
            bulletsV.add(bullet)
            fire_voron = False
            last_timeVorona = timer()
        if self.lives <= 0:
            score += 10
            self.rect.x = 0
            self.rect.y = randint(50, 650)
            self.lives = 2
            
#        if  now_timeVorona - last_timeVorona > 5:
#            rand = randint(0, 6)
#            bulletV = Bullet('bullets_PNG.png', self.rect.centerx, self.rect.top, 15, 20, 15)
#            bulletV.add(bulletsV)


            
class Bullet(GameSprite):
    def update(self):
        self.rect.x += self.speed
        if self.rect.x < 0:
            self.kill()
        elif self.rect.x > 1080:
            self.kill()

class Asteroid(GameSprite):
    def update(self):
        self.rect.x += self.speed
        if self.rect.x > 980:
            self.rect.y = randint(50,800)
            self.rect.x = 0

asteroids = sprite.Group()
for i in range(1, 3):
    asteroid = Asteroid('asteroid.png', 0, randint(50, 650), 80 , 50, randint(2,6))
    asteroids.add(asteroid)

monstersB = sprite.Group()
for i in range(1, 3):
    monsterB = Enemy('Raven-Flying-PNG-HD.png', 0, randint(50, 650), 200, 100, randint(2,4), 2)
    monstersB.add(monsterB)

monsters = sprite.Group()
for i in range(1,8):
    monster = Enemy('Raven-Flying-PNG-HD.png', 0, randint(50, 650), 80, 50, randint(3,5), 2)
    monsters.add(monster)

bulletsV = sprite.Group()

bullets = sprite.Group()

font.init()
font1 = font.SysFont('Arial', 36)


lost = 0
score = 0

rel_time = False

rel_timeV = False

num_fire = 0

life_monster = 1

life = 3

fire_voron = False

last_timeVorona = timer()


ship = Player('stalker_PNG10.png', 950, win_height - 120, 100, 100, 18)
finish = False
run = True
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 30 and rel_time == False:
                    num_fire += 1
                    fire_sound.play()
                    ship.fire()
                if num_fire >= 30 and rel_time == False:
                    last_time = timer()
                    rel_time = True 

            
    if not finish:
        window.blit(background, (0,0))
        text = font1.render('Счет: ' + str(score), 1, (255,255,255))
        window.blit(text, (10,20))
        text_lose = font1.render('Пропущено: ' + str(lost), 1, (255,255,255))
        window.blit(text_lose, (10,50))
        ship.update()
        monstersB.update()
        monsters.update()
        bulletsV.update()
        bullets.update()
#        asteroids.update()
        ship.reset()
#        for i in range(0, 7):
#            monsters[i].update()
#            monsters[i].reset()
        monsters.draw(window)
        monstersB.draw(window)
        bulletsV.draw(window)        
        bullets.draw(window)





#        asteroids.draw(window)
#        for i in range(1, 3):
#            if sprite.spritecollide(monstersB[i], bullets, True):
#                life_monster -= 1
#                if life_monster == 0:
#                    score = score + 1
#                    monstersB[i].rect.x = 0
#                    monstersB[i].recy.y = randint(50,650)
#            if sprite.collide_rect(monstersB[i], ship):
#                life -= 1
#                monstersB[i].rect.x = 0
#                monstersB[i].rect.y = randint(50, 650) 
       

#        for i in range(0, 7):
#            if sprite.spritecollide(monsters[i], bullets, True):
#                score = score + 1
#                monsters[i].rect.x = 0
#                monsters[i].rect.y = randint(50, 650)
#            if sprite.collide_rect(monsters[i], ship):
#                life -= 1
#                monsters[i].rect.x = 0
#                monsters[i].rect.y = randint(50, 650)         

        collides = sprite.groupcollide(monstersB, bullets, False, True)
        for c in collides:
            c.lives -= 1       

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score + 1
            monster = Enemy('Raven-Flying-PNG-HD.png', 0, randint(50, 650), 80, 50, randint(3,5), 2)
            monsters.add(monster)
        if score >= 60:
            finish = True
            win = font1.render('YOU WIN!', True, (255, 255, 255))
            window.blit(win, (500, 300))

        if sprite.spritecollide(ship, bulletsV, False) or sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, monstersB, False):
            sprite.spritecollide(ship, bulletsV, True)
            sprite.spritecollide(ship, monsters, True)
            sprite.spritecollide(ship, monstersB, True)
            life = life - 1
        now_time_voron = timer()

        if now_time_voron - last_timeVorona > 2:
            fire_voron = True

        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 3:
                reload = font1.render('идет перезарядка', 1, (150, 0, 0))
                window.blit(reload, (500, 200))
            else:
                num_fire = 0
                rel_time = False
        if life == 0 or lost >= 3:
            finish = True
            lose = font1.render('YOU LOSE!', True, (180, 0, 0))
            window.blit(lose, (500, 300))
        if life == 3:
            life_color = (0, 150, 0)
        if life == 2:
            life_color = (150, 150, 0)
        if life == 1:
            life_color = (150, 0, 0)
        text_life = font1.render(str(life), 1, life_color)
        window.blit(text_life, (1000, 20))
        display.update()
    time.delay(5)

