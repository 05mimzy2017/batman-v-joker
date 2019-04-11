# Imports
import pygame
import random
import xbox360_controller 

# Initialize game engine
pygame.init()


# Window
WIDTH = 1600
HEIGHT = 900
SIZE = (WIDTH, HEIGHT)
TITLE = "Batman v. Joker"
screen = pygame.display.set_mode(SIZE, pygame.FULLSCREEN)
pygame.display.set_caption(TITLE)


# Timer
clock = pygame.time.Clock()
refresh_rate = 60


# Colors
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (100, 255, 100)

# Controllers
my_controller = xbox360_controller.Controller(0)

# Fonts
FONT_SM = pygame.font.Font("assets/fonts/HOMOARAK.ttf", 24)
FONT_MD = pygame.font.Font("assets/fonts/HOMOARAK.ttf", 32)
FONT_LG = pygame.font.Font("assets/fonts/HOMOARAK.ttf", 64)
FONT_XL = pygame.font.Font("assets/fonts/HOMOARAK.ttf", 96)


# Images
#ship_img = pygame.image.load('assets/images/player.png').convert_alpha()
laser_img = pygame.image.load('assets/images/batarang2.png').convert_alpha()
joker_img = pygame.image.load('assets/images/joker.png').convert_alpha()
quinn_img = pygame.image.load('assets/images/quinn.png').convert_alpha()
bomb_img = pygame.image.load('assets/images/card.png').convert_alpha()
#bomb2_img = pygame.image.load('assets/images/mallet.png').convert_alpha()
batman_img = pygame.image.load('assets/images/bat.png').convert_alpha()
city_img = pygame.image.load('assets/images/background/city.png').convert_alpha()
riddler_img = pygame.image.load('assets/images/riddler.png').convert_alpha()
boom_img = pygame.image.load('assets/images/explosion.png').convert_alpha()
robin_img = pygame.image.load('assets/images/robin.png').convert_alpha()
shield_img = pygame.image.load('assets/images/shield.png').convert_alpha()
penguin_img = pygame.image.load('assets/images/penguin2.png').convert_alpha()
restore_img = pygame.image.load('assets/images/restore.png').convert_alpha()



# Sounds
EXPLOSION = pygame.mixer.Sound('assets/sounds/explosion.ogg')
#SHOOT = pygame.mixer.Sound('assets/sounds/shoot.wav')
HIT = pygame.mixer.Sound('assets/sounds/hit.wav')
DRUMS = pygame.mixer.Sound('assets/sounds/drums_of_mordon.ogg')
SHOOT = pygame.mixer.Sound('assets/sounds/knife.wav')
pygame.mixer.music.load('assets/sounds/dark.ogg')
pygame.mixer.music.play(-1)


# Stages
START = 0
PLAYING = 1
END = 2
PAUSE = 3
WIN = 4
LOSE = 5


# Game classes
class Ship(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.delay = 0
        self.shield = 5
        self.speed = 3
        self.shoots_double = False
        
    def move_left(self):
        self.rect.x -= self.speed
    
    def move_right(self):
        self.rect.x += self.speed

    def move_down(self):
        self.rect.y += self.speed

    def move_up(self):
        self.rect.y -= self.speed

    def shoot(self):
        if self.delay == 0:
            pygame.mixer.Sound.play(SHOOT)
            
            laser = Laser(laser_img)
            laser.rect.centerx = self.rect.centerx
            laser.rect.centery = self.rect.top
            lasers.add(laser)
            self.delay = 0
        
    def update(self):
        global stage
        '''check screen edges'''
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.delay > 0:
            self.delay -= 1
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        elif self.rect.top < 0:
            self.rect.top = 0

        ''' check powerups '''
        hit_list = pygame.sprite.spritecollide(self, powerups, True,
                                               pygame.sprite.collide_mask)

        if len(hit_list) > 0:
            for hit in hit_list:
                hit.apply(self)
                
        ''' check bombs'''
        hit_list = pygame.sprite.spritecollide(self, bombs, True,
                                               pygame.sprite.collide_mask)

        if len(hit_list) > 0:
            if self.shield > 0:
                self.shield -= 1
                HIT.play()
            elif self.shield == 0:
                self.kill()
                stage = END

        if self.shield == 0:
            self.image = robin_img

class Laser(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        
        self.speed = 5
        
    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()

class Mob(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.shield = 3
        self.speed = 3
        
    def drop_bomb(self):
            pygame.mixer.Sound.play(HIT)
            
            bomb = Bomb(bomb_img)
            self.mask = pygame.mask.from_surface(self.image)
            bomb.rect.centerx = self.rect.centerx
            bomb.rect.centery = self.rect.bottom
            bombs.add(bomb)
            

    def update(self):
        global score
        hit_list = pygame.sprite.spritecollide(self, lasers, True,
                                               pygame.sprite.collide_mask)

        if len(hit_list) > 0:
            if self.shield > 0:
                self.shield -= 1
                EXPLOSION.play()
            elif self.shield == 0:
                self.kill()
                score += 1
                fleet.speed += 1

        if self.shield == 0:
            self.image = penguin_img
            
            
class Bomb(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.speed = 3
        
    def update(self):
        self.rect.y += self.speed
        
        if self.rect.top > HEIGHT:
            self.kill()

            
class Powerup(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.speed = 5
        self.rect.x = x
        self.rect.y = y

    def apply(self, ship):
        ship.shield = 5
        self.kill()
        
    def update(self):
        self.rect.y += self.speed

        if self.rect.top > HEIGHT:
            self.kill()

        
class Fleet():
    def __init__(self, mobs):
        self.mobs = mobs
        self.speed = 5
        self.moving_right = True
        self.drop_speed = 20
        self.bomb_rate = 60 # lower is faster

    def move(self):
        hits_edge = False
        
        for m in mobs:
            if self.moving_right:
                m.rect.x += self.speed

                if m.rect.right >= WIDTH:
                    hits_edge = True
            else:
                m.rect.x -= self.speed

                if m.rect.left <= 0:
                    hits_edge = True

        if hits_edge:
            self.reverse()
            #self.move_down()
            
    def reverse(self):
        self.moving_right = not self.moving_right

    def move_down(self):
        for m in mobs:
            m.rect.y += self.drop_speed
            
    def choose_bomber(self):
        rand = random.randrange(self.bomb_rate)
        mob_list = mobs.sprites()

        if len(mob_list) > 0 and rand == 0:
            bomber = random.choice(mob_list)
            bomber.drop_bomb()
        
    
    def update(self):
        self.move()
        self.choose_bomber()


class UFO(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint (-2000, -1000)
        self.rect.y = 350
        self.speed = 5

    def move(self):
        self.rect.x += self.speed

    def update(self):
        self.move()
        global score
        
        hit_list = pygame.sprite.spritecollide(self, lasers, True,
                                               pygame.sprite.collide_mask)

        if len(hit_list) > 0:
            self.kill()
            score += 20

    

# Game helper functions
def show_title_screen():
    title_text = FONT_XL.render("Batman v Joker!", 1, WHITE)
    screen.blit(title_text, [128, 404])

def show_pause():
    title_text = FONT_XL.render("Paused", 1, WHITE)
    screen.blit(title_text, [128, 404])

def show_end():
    if stage == END: 
        title_text = FONT_XL.render("GAME OVER!", 1, WHITE)
        screen.blit(title_text, [128, 404])
        
        ship_list = player.sprites()

        if len(ship_list) == 0:
            title_text = FONT_LG.render("You Lose!", 1, WHITE)
            screen.blit(title_text, [128, 504])
        else:
            title_text = FONT_LG.render("You Won!", 1, WHITE)
            screen.blit(title_text, [128, 504])

def show_stats(player):
    title_text = FONT_LG.render(str(score), 1, WHITE)
    text_width = title_text.get_width()
    screen.blit(title_text, [WIDTH - (text_width + 10), 10])
    shield_text = FONT_LG.render(str(ship.shield), 1, WHITE)
    screen.blit(shield_text,[0, 850])
    

def draw_timer():
    title_text = FONT_LG.render(time, 1, WHITE)
    screen.blit(title_text, [10, 10])

def setup():
    global stage, done
    global player, ship, lasers, mobs, fleet, bombs, bomb2, ufos, powerups
    global ticks, seconds, minutes, time
    global score
     
    ''' Make game objects '''
    ship = Ship(batman_img)
    ship.rect.centerx = WIDTH / 2
    ship.rect.bottom = HEIGHT - 30

    ''' Make sprite groups '''
    player = pygame.sprite.GroupSingle()
    player.add(ship)

    lasers = pygame.sprite.Group()
    bombs = pygame.sprite.Group()

    #Row 1
    mob1 = Mob(100, 100, joker_img)
    mob2 = Mob(300, 100, joker_img)
    mob3 = Mob(500, 100, joker_img)
    mob4 = Mob(700, 100, joker_img)
    mob5 = Mob(900, 100, joker_img)
    mob6 = Mob(1100, 100, joker_img)
    mob7 = Mob(1300, 100, joker_img)

    #Row 2
    mob8 = Mob(100, 250, quinn_img)
    mob9 = Mob(300, 250, quinn_img)
    mob10 = Mob(500, 250, quinn_img)
    mob11 = Mob(700, 250, quinn_img)
    mob12 = Mob(900, 250, quinn_img)
    mob13 = Mob(1100, 250, quinn_img)
    mob14 = Mob(1300, 250, quinn_img)
    
    mobs = pygame.sprite.Group()
    mobs.add(mob1, mob2, mob3, mob4, mob5, mob6, mob7, mob8, mob9, mob10, mob11,
             mob12, mob13, mob14)

    fleet = Fleet(mobs)

    powerup1 = Powerup(200, -2000, restore_img)
    powerups = pygame.sprite.Group()
    powerups.add(powerup1)

    ufo = UFO(riddler_img)

    ufos = pygame.sprite.GroupSingle()

    ufos.add(ufo)

    #pygame.mixer.music.play(-1)
    
    ''' set stage '''
    stage = START
    done = False

    ticks = 0
    seconds = 0
    minutes = 0
    time = ""

    score = 0

    
# Game loop
setup()

while not done:
    # Input handling (React to key presses, mouse clicks, etc.)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True
            if stage == START:
                if event.key == pygame.K_SPACE:
                    stage = PLAYING
            elif stage == PLAYING:
                if event.key == pygame.K_p:
                    stage = PAUSE
            elif stage == PAUSE:
                if event.key == pygame.K_p:
                    stage = PLAYING

            elif stage == END:
                if event.key == pygame.K_SPACE:
                    setup()

        
        if event.type == pygame.JOYBUTTONDOWN:
            if event.button == xbox360_controller.START:
                if stage == START:
                    stage = PLAYING
            elif event.button == xbox360_controller.B:
                if stage == PLAYING:
                    stage = PAUSE
                elif stage == PAUSE:
                    stage = PLAYING
            elif event.button == xbox360_controller.A:
                if stage == PLAYING:
                    ship.shoot()
            elif event.button == xbox360_controller.Y:
                if stage == END:
                    setup()
                    
        
    pressed = pygame.key.get_pressed()

   #Keyboard 
    if stage == PLAYING:
        if pressed[pygame.K_LEFT]:
            ship.move_left()
        elif pressed[pygame.K_RIGHT]:
            ship.move_right()
        if pressed[pygame.K_SPACE]:
            ship.shoot()

        #Controller        
        left_x, left_y = my_controller.get_left_stick()
        if left_x >= .5:
            ship.move_right()
        elif left_x <= -.5:
            ship.move_left()
        if left_y >= .5:
            ship.move_down()
        elif left_y <= -.5:
            ship.move_up()

            
        powerup_spawn = random.randint(1, 100)
        if powerup_spawn == 512:
            powerup = Powerup()
            power.rect.x = random.randrange(1, 1000)
            powerup.rect.bottom = 0
            powerups.add(powerup)
      
            
    # Game logic (Check for collisions, update points, etc.)
    if stage == PLAYING:
        player.update()
        lasers.update()
        bombs.update()
        fleet.update()
        mobs.update()
        ufos.update()
        powerups.update()
        ticks += 1
        
        mob_list = mobs.sprites()
        if len(mob_list) == 0:
            stage = END

        if ticks == 60:
            seconds += 1
            ticks = 0
        if seconds == 60:
            minutes += 1
            seconds = 0
        if seconds < 10:
            time = str(minutes) + ": 0" + str(seconds)
        else:
            time = str(minutes) + ": " + str(seconds)
            
    '''if stage == END:
        pygame.mixer.music.stop()
        if not sound_played:
            pygame.mixer.Sound.play(victory_sound)
            sound_played = True '''
     
   # Drawing code (Describe the picture. It isn't actually drawn yet.)
    screen.blit(city_img,[0,0])
    lasers.draw(screen)
    bombs.draw(screen)
    player.draw(screen)
    mobs.draw(screen)
    ufos.draw(screen)
    powerups.draw(screen)
    draw_timer()
    show_stats(player)
    show_end()
    
    if stage == START:
        show_title_screen()
    elif stage == PAUSE:
        show_pause()

        
    # Update screen (Actually draw the picture in the window.)
    pygame.display.flip()


    # Limit refresh rate of game loop 
    clock.tick(refresh_rate)


# Close window and quit
pygame.quit()
