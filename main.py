import pygame
import os
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Hi, my game!!")
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255, 0, 0)
FPS = 60
VELOCITY = 8
LASER_VELOCITY = 10
MAX_NUM_LASERS = 4
BORDER = pygame.Rect(WIDTH//2 - 3, 0, 6, HEIGHT)
HEALTH_FONT = pygame.font.SysFont('Chalkduster', 20)
WINNER_FONT = pygame.font.SysFont('Jokerman', 60)
LASER_FIRE_SOUND = pygame.mixer.Sound(os.path.join('laser_sound.mp3'))
LASER_HIT_SOUND = pygame.mixer.Sound(os.path.join('hit_sound.mp3'))
BACKGROUND_MUSIC = pygame.mixer.Sound(os.path.join('background_music.mp3'))

Character_1_WIDTH = 40
Character_1_HEIGHT = 60
Character_2_WIDTH = 55
Character_2_HEIGHT = 40
Chara1_lasers = []
Chara2_lasers = []
Character_1_HIT = pygame.USEREVENT + 1
Character_2_HIT = pygame.USEREVENT + 2



Character_1 = pygame.image.load(os.path.join('PikPng.com_8-bit-characters-png_4097335.png'))
Character_1 = pygame.transform.flip(pygame.transform.scale(Character_1, (Character_1_WIDTH,Character_1_HEIGHT)), True, False)
Character_2 = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
Character_2 = pygame.transform.rotate(pygame.transform.scale(Character_2, (Character_2_WIDTH,Character_2_HEIGHT)), -90)
background = pygame.transform.scale(pygame.image.load(os.path.join('Spaceship_game_background1.jpeg')), (WIDTH,HEIGHT))
heart = pygame.transform.scale(pygame.image.load(os.path.join('heart1.png')), (30,30))


def draw_window(Chara1, Chara2, Chara1_lasers, Chara2_lasers, Character_1_HEALTH, Character_2_HEALTH):
    WIN.blit(background, (0,0))
    pygame.draw.rect(WIN, WHITE, BORDER)
    WIN.blit(Character_1, (Chara1.x, Chara1.y))
    WIN.blit(Character_2, (Chara2.x, Chara2.y))

    health_text = HEALTH_FONT.render("HEALTH: ", 1, WHITE)
    WIN.blit(health_text, (10, 10))
    WIN.blit(health_text, ((WIDTH - health_text.get_width() - 160), 10))
    for i in range(0, Character_1_HEALTH):
        WIN.blit(heart, ((10 + health_text.get_width() + (30*i), 5)))
    for i in range(0, Character_2_HEALTH):
        WIN.blit(heart, (((WIDTH - health_text.get_width() - 160) + health_text.get_width() + (30*i), 5)))
    for laser in Chara1_lasers:
        pygame.draw.rect(WIN, RED, laser)
    for laser in Chara2_lasers:
        pygame.draw.rect(WIN, RED, laser)
    pygame.display.update()

def reset_characters(Chara1, Chara2, CharacterString):
    Chara1.x = 100
    Chara1.y = 300
    Chara2.x = 700
    Chara2.y = 300
    Chara1_lasers.clear()
    Chara2_lasers.clear()
    Death = HEALTH_FONT.render(CharacterString + " LOST A LIFE", 1, RED)
    WIN.blit(Death, (WIDTH//2 - (Death.get_width()/2), HEIGHT//2 - (Death.get_height()//2 )))
    pygame.display.update()
    pygame.time.delay(1000)


def draw_winner(winner_message):
    winning_text = WINNER_FONT.render(winner_message, 1, WHITE)
    WIN.blit(winning_text, (WIDTH//2 - (winning_text.get_width()//2), HEIGHT//2 - (winning_text.get_height()//2)))
    pygame.display.update()
    pygame.time.delay(2000)

def Chara1_movement(controls, Chara1):
    if controls[pygame.K_a] and (Chara1.x - VELOCITY)>0:
        Chara1.x -= VELOCITY
    if controls[pygame.K_d] and (Chara1.x + VELOCITY + Character_1_WIDTH - 3)<BORDER.x:
        Chara1.x += VELOCITY
    if controls[pygame.K_w] and (Chara1.y - VELOCITY + 3)>0:
        Chara1.y -= VELOCITY
    if controls[pygame.K_s] and (Chara1.y + VELOCITY + Character_1_HEIGHT - 4)<HEIGHT:
        Chara1.y += VELOCITY

def Chara2_movement(controls, Chara2):
    if controls[pygame.K_LEFT] and (Chara2.x - VELOCITY)>(BORDER.x+6):
        Chara2.x -= VELOCITY
    if controls[pygame.K_RIGHT] and (Chara2.x + VELOCITY + Character_2_WIDTH - 20)<WIDTH:
        Chara2.x += VELOCITY
    if controls[pygame.K_UP] and (Chara2.y - VELOCITY + 1.7)>0:
        Chara2.y -= VELOCITY
    if controls[pygame.K_DOWN] and (Chara2.y + VELOCITY + Character_2_HEIGHT + 12.5)<HEIGHT:
        Chara2.y += VELOCITY
def laser_movement(Chara1_lasers, Chara2_lasers, Chara1, Chara2):
    for laser in Chara1_lasers:
        laser.x += LASER_VELOCITY
        if Chara2.colliderect(laser):
            pygame.event.post(pygame.event.Event(Character_2_HIT))
            Chara1_lasers.remove(laser)
        elif laser.x >= WIDTH:
            Chara1_lasers.remove(laser)
    for laser in Chara2_lasers:
        laser.x -= LASER_VELOCITY
        if Chara1.colliderect(laser):
            pygame.event.post(pygame.event.Event(Character_1_HIT))
            Chara2_lasers.remove(laser)
        elif  laser.x <= 0:
            Chara2_lasers.remove(laser)


def main():
    Chara1 = pygame.Rect(100, 300, Character_1_WIDTH, Character_1_HEIGHT)
    Chara2 = pygame.Rect(700, 300, Character_2_WIDTH, Character_2_HEIGHT)
    clock = pygame.time.Clock()
    Character_1_HEALTH = 5
    Character_2_HEALTH = 5
    run = True
    BACKGROUND_MUSIC.set_volume(0.3)
    BACKGROUND_MUSIC.play(-1, 0, 0)
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f and len(Chara1_lasers) <= MAX_NUM_LASERS:
                    laser = pygame.Rect((Chara1.x + Character_1_WIDTH - 1), (Chara1.y + Character_1_HEIGHT//2 - 1), 10, 5)
                    Chara1_lasers.append(laser)
                    LASER_FIRE_SOUND.play()
                if event.key == pygame.K_RALT and len(Chara2_lasers) <= MAX_NUM_LASERS:
                    laser = pygame.Rect((Chara2.x + 1), (Chara2.y + Character_2_HEIGHT//2 - 1), 10, 5) 
                    Chara2_lasers.append(laser)
                    LASER_FIRE_SOUND.play()
            if event.type == Character_1_HIT:
                Character_1_HEALTH -= 1
                LASER_HIT_SOUND.play()
                reset_characters(Chara1, Chara2, "HUMAN")
            if event.type == Character_2_HIT:
                Character_2_HEALTH -= 1
                LASER_HIT_SOUND.play()
                reset_characters(Chara1, Chara2, "ALIEN")

            
        winner_message = ""
        if Character_1_HEALTH <= 0:
            winner_message = "ALIENS WINS!!"
        if Character_2_HEALTH <= 0:
            winner_message = "HUMANS WINS!!"
        controls = pygame.key.get_pressed() 
        Chara1_movement(controls, Chara1)
        Chara2_movement(controls, Chara2)
        laser_movement(Chara1_lasers, Chara2_lasers, Chara1, Chara2)
        draw_window(Chara1, Chara2, Chara1_lasers, Chara2_lasers, Character_1_HEALTH, Character_2_HEALTH)
        if winner_message != "":
            draw_winner(winner_message)
            break
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                pygame.mixer.pause()
                BACKGROUND_MUSIC.set_volume(0)
                main()
    
if __name__ == "__main__":
    main()