import pygame
import random, sys
from pygame.locals import *

# class for buttons
class button():
    def __init__(self, color, x,y,width,height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text


    def draw(self,win,outline=None):
        #Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x-2,self.y-2,self.width+4,self.height+4),0)

        pygame.draw.rect(win, self.color, (self.x,self.y,self.width,self.height),0)

        if self.text != '':
            font = pygame.font.SysFont('comicsans', 60)
            text = font.render(self.text, 1, (0,0,0))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))


    def isOver(self, pos):
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False


class Score():
    def __init__(self):
        self.score = 0


def create_enemy_car():

    car_color_list = [1, 2, 3, 4]
    random_car_color = random.choice(car_color_list)
    if random_car_color ==  1:
        enemy_car = blue_car
    elif random_car_color == 2:
        enemy_car = yellow_car
    elif random_car_color == 3:
        enemy_car = green_car
    elif random_car_color == 4:
        enemy_car = red_car

    random_car_pos = random.choice(car_pos_list)
    enemy_car_rect = enemy_car.get_rect(midtop = (random_car_pos,-100))
    return enemy_car_rect, enemy_car


def move_enemy(enemy_cars, vel):
	for car_rect, enemy_car in enemy_cars:
		car_rect.centery += vel
	return enemy_cars


def draw_enemy_cars(enemy_cars):
    for car_rect, enemy_car in enemy_cars:
        win.blit(enemy_car,car_rect)
        #pygame.draw.rect(win, (255,255,255), car_rect, 2)


def check_collision(enemy_cars):
	for car_rect, enemy_car in enemy_cars:
		if my_car_rect.colliderect(car_rect):
			hit_effect.play()
			return False
	return True


def draw_my_car():
    win.blit(my_car, my_car_rect)
    #pygame.draw.rect(win, (255,255,255), my_car_rect, 2)


def draw_lives(lives):
    if lives == 3:
        win.blit(lives3, (20,80))
    elif lives == 2:
        win.blit(lives2, (20,80))
    elif lives == 1:
        win.blit(lives1, (20,80))


def start_menu(win, fullscreen_flag):

    my_car_rect.centery = 640

    #button(color, x,y,width,height, text='')
    start_game = button((255,0,0), 350,200, 450, 50,'START NEW GAME')
    exit_game = button((255,0,0), 400,400, 350, 50,'EXIT THE GAME')
    intro = True
    while intro:
        win.blit(bg1, (0,0))
        #exit from the game
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                intro = False
                pygame.quit()
                sys.exit()
                #quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_game.isOver(pos):
                    #print('start game')
                    intro = False
                if exit_game.isOver(pos):
                    #print('exit game')
                    intro = False
                    pygame.quit()
                    sys.exit()
                    #quit()

            if event.type == pygame.MOUSEMOTION:
                if start_game.isOver(pos):
                    start_game.color = (0,255,0)
                else:
                    start_game.color = (255, 0, 0)

                if exit_game.isOver(pos):
                    exit_game.color = (0,255,0)
                else:
                    exit_game.color = (255, 0, 0)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_f]:
            if not fullscreen_flag:
                win = pygame.display.set_mode((1100,750), pygame.FULLSCREEN)
                fullscreen_flag = not fullscreen_flag
            else:
                win = pygame.display.set_mode((1100,750))
                fullscreen_flag = not fullscreen_flag

        start_game.draw(win, (255,255,255))
        exit_game.draw(win, (255,255,255))
        #update the screen
        pygame.display.update()


def pause_menu(win,fullscreen_flag):

    countinue_game = button((255,0,0), 350,200, 400, 50,'COUNTINUE')
    end_game = button((255,0,0), 350,400, 400, 50,'END THE GAME')
    puase = True
    while puase:
        win.blit(bg1, (0,0))
        draw_enemy_cars(enemy_car_list)
        draw_my_car()
        #exit from the game
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                intro = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if countinue_game.isOver(pos):
                    #print('start game')
                    puase = False
                if end_game.isOver(pos):
                    #print('exit game')
                    puase = False
                    score.score = 0
                    enemy_car_list.clear()
                    start_menu()

            if event.type == pygame.MOUSEMOTION:
                if countinue_game.isOver(pos):
                    countinue_game.color = (0,255,0)
                else:
                    countinue_game.color = (255, 0, 0)

                if end_game.isOver(pos):
                    end_game.color = (0,255,0)
                else:
                    end_game.color = (255, 0, 0)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_f]:
            if not fullscreen_flag:
                win = pygame.display.set_mode((1100,750), pygame.FULLSCREEN)
                fullscreen_flag = not fullscreen_flag
            else:
                win = pygame.display.set_mode((1100,750))
                fullscreen_flag = not fullscreen_flag

        countinue_game.draw(win, (255,255,255))
        end_game.draw(win, (255,255,255))
        #update the screen
        pygame.display.update()


def print_score(int_score, hi_score, velocity):
    #prints score to game screen
    score_surface = font.render('Score: '+str(int(int_score)),True,(0,0,0))
    win.blit(score_surface, (20,20))
    #prints high scre to game screen
    hi_score_surface = font.render('High score: '+str(int(hi_score)),True,(0,0,0))
    win.blit(hi_score_surface,(20,40))
    #prints speed
    speed = font.render('Speed: '+str(int(velocity)),True,(0,0,0))
    win.blit(speed,(20,60))


def update_lives(int_score, lives, flag_for_lives):
    if int_score == 200 and lives < 3 and flag_for_lives == 0:
        lives += 1
        bonus.play()
        flag_for_lives = 1
    elif int_score == 400 and lives < 3 and flag_for_lives == 1:
        lives += 1
        bonus.play()
        flag_for_lives = 2
    elif int_score == 600 and lives < 3 and flag_for_lives == 2:
        lives += 1
        bonus.play()
        flag_for_lives = 3

    return lives, flag_for_lives


pygame.mixer.pre_init(frequency =44100, size =16, channels =1, buffer = 512 )
pygame.init()
#win = pygame.display.set_mode((1100,750), pygame.FULLSCREEN)
win = pygame.display.set_mode((1100,750))
#game name
pygame.display.set_caption('drift cars')
#game icon
programIcon = pygame.image.load('data/game_icon.ico')
pygame.display.set_icon(programIcon)

#game Clock
clock = pygame.time.Clock()

#backwords
bg1  = pygame.image.load('data/bg1.png').convert()
bg2 = pygame.image.load('data/bg2.png').convert()

#my car
my_car = pygame.image.load('data/red1.png').convert_alpha()
my_car_rect = my_car.get_rect(topleft = (950,640))

#enemy cars
blue_car = pygame.image.load('data/blue1.png').convert_alpha()
yellow_car = pygame.image.load('data/yellow1.png').convert_alpha()
green_car = pygame.image.load('data/green1.png').convert_alpha()
red_car = pygame.image.load('data/rede1.png').convert_alpha()


#background music
#music = pygame.mixer.music.load('data/bg_music.mp3')
#pygame.mixer.music.play(-1)

#sound effects
hit_effect = pygame.mixer.Sound('data/car_hit.wav')
bonus = pygame.mixer.Sound('data/bonus.wav')

# lives counter images
lives3 = pygame.image.load('data/lives3.png').convert_alpha()
lives2 = pygame.image.load('data/lives2.png').convert_alpha()
lives1 = pygame.image.load('data/lives1.png').convert_alpha()

#reading the hiset score from the file
with open('data/hi_score.txt', 'r') as f:
    hi_score = int(f.readline())

exp = pygame.image.load('data/exp1.png').convert_alpha()

enemy_car_list = []
SPAWNCAR = pygame.USEREVENT
pygame.time.set_timer(SPAWNCAR,750)
car_pos_list = [720, 800, 860, 930, 1000]

bgy1 = 0
bgy2 = bg1.get_height() * (-1)
font = pygame.font.SysFont('comicsans', 20)
#game variables

score = Score()
int_score = 0
lives = 3
velocity = 10
run = True
game_active = True
fullscreen_flag = False
flag_for_lives = 0
enemy_create_flag = 0


#game loop starts here
start_menu(win, fullscreen_flag)
while run:
    clock.tick(30)
    if velocity <= 22:
        velocity += 0.005

    win.blit(bg1,(0,bgy1))
    win.blit(bg1,(0,bgy2))
    lives, flag_for_lives = update_lives(int_score, lives, flag_for_lives)
    draw_lives(lives)
    print_score(int_score, hi_score, int(velocity))
    score.score +=0.1
    int_score = int(score.score)

    if int(velocity) == 20 and enemy_create_flag == 0:
        pygame.time.set_timer(SPAWNCAR,500)
        enemy_create_flag = 1
    elif int(velocity) == 30 and enemy_create_flag == 1:
        pygame.time.set_timer(SPAWNCAR,400)
        enemy_create_flag = 2

    #checking for collision
    game_active = check_collision(enemy_car_list)
    if game_active:
        move_enemy(enemy_car_list, velocity)
        draw_enemy_cars(enemy_car_list)
        draw_my_car()
    else:
        enemy_car_list.clear()

        my_car_rect.centery = 690
        if lives != 1:
            win.blit(exp, (700,90))
            pygame.display.update()
            pygame.time.delay(500)
            lives -=1
        else:
            game_over ='GAME                                          OVER'
            GO = font.render(game_over, 1, (255,255,255))
            win.blit(GO, (730, 40))
            win.blit(exp, (700,90))
            pygame.display.update()
            pygame.time.delay(1000)
            # update hi score
            if int_score > hi_score:
                hi_score = int_score
                with open('data/hi_score.txt', 'w') as f:
                    hi = str(hi_score)
                    f.write(hi)
            score.score = 0
            velocity = 10
            lives = 3
            start_menu(win, fullscreen_flag)


    for event in pygame.event.get():
        #exit from the game
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            sys.exit()
            #quit()

        #add new enemy cars
        if event.type == SPAWNCAR:
            enemy_car_list.append(create_enemy_car())
            #print(enemy_car_list)

  #get the pressed keys
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and my_car_rect.centerx > 710:
        my_car_rect.centerx -= 10

    elif keys[pygame.K_RIGHT] and my_car_rect.centerx <1020:
        my_car_rect.centerx += 10

    elif keys[pygame.K_UP] and my_car_rect.centery >150:
        my_car_rect.centery -= 10

    elif keys[pygame.K_DOWN] and my_car_rect.centery <690:
        my_car_rect.centery += 10

    elif keys[pygame.K_SPACE]:
        pause_menu(win, fullscreen_flag)

    elif keys[pygame.K_f]:
        if not fullscreen_flag:
            win = pygame.display.set_mode((1100,750), pygame.FULLSCREEN)
            fullscreen_flag = not fullscreen_flag
        else:
            win = pygame.display.set_mode((1100,750))
            fullscreen_flag = not fullscreen_flag

    bgy1 += 5
    bgy2 += 5

    if bgy1 > bg1.get_height():
        bgy1 = bg1.get_height()*(-1)

    if bgy2 > bg1.get_height():
        bgy2 = bg1.get_height() *(-1)

    pygame.display.update()
