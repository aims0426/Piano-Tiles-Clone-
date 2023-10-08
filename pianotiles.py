#Piano Tiles
import json
import pygame
import random
from threading import Thread
from tile import TILE
from button import Button
pygame.init()
pygame.font.init()
font_path = "Press_Start_2P/PressStart2P-Regular.ttf"
font = pygame.font.Font(None, 36)  # Choose your font and size
score_color = (255, 255, 255)
SCREEN=WIDTH, HEIGHT = 300,500 #Size of window screen we want 
pygame.display.set_caption("Piano Tiles")
screen_size= pygame.display.Info() #to get the user's screen size
width= screen_size.current_w #to get the width of the user's screen
height= screen_size.current_h #to get the height of the user's screen
t_wid= WIDTH//4
t_height= HEIGHT//4
if width>= height : #user is using a desktop screen
    window = pygame.display.set_mode(SCREEN, pygame.NOFRAME)
else : #user is on a mobile device
    window= pygame,display.set_mode(SCREEN, pygame.NOFRAME | pygame.SCALED | pygame.FULLSCREEN)
    #pygame. display. set_mode((width, height), flags, depth)-{parameters of the function}
clock= pygame.time.Clock()
FPS= 30 #frames per second
bgimg= pygame.image.load('Resources/bg.png')
bgimg= pygame.transform.scale(bgimg, (WIDTH, HEIGHT)) #transforms the image to fit the screensiz
    #[takes two parameters- the bg image and the size we want to resize it to]
#function for exiting the game
startimg= pygame.image.load('Resources/play.jpeg')
startimg= pygame.transform.scale(startimg,(120,40))
start_rect= startimg.get_rect(center=(WIDTH//2, HEIGHT-180))
endm= pygame.mixer.Sound('Sounds/endmusic.wav')
e_xit= pygame.image.load('Resources/exit.jpeg')
replay=pygame.image.load('Resources/replay.jpeg')
exit_btn= Button(e_xit, (141,42), WIDTH//2-69, HEIGHT//2+80)
replay_btn=Button(replay, (141,43), WIDTH//2-69, HEIGHT//2+10)
highest_score = 0
try:
    with open('highest_score.txt', 'r') as file:
        highest_score = int(file.read())
except FileNotFoundError:
    pass

t= TILE(10,10,window)
tile_group= pygame.sprite.Group()#for multiple tiles

def get_speed(score):
    reutrn (200+5*score)
def play_notes(notepath):
    pygame.mixer.Sound(notepath).play()
def display_score(screen, score):
    font = pygame.font.Font(font_path, 20)
    score_text = font.render(f'SCORE:{score}', True, (0, 0, 0))
    text_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
    screen.blit(score_text, text_rect)
    font = pygame.font.Font(font_path, 13)
    highest_score_text = font.render(f'HIGHEST SCORE: {highest_score}', True, (0,0,0))
    #text_rect = highest_score_text.get_rect(center=(WIDTH // 2, HEIGHT // 8))
    screen.blit(highest_score_text, (50, 170)) 

with open('notes.json') as file:
    notes_dict= json.load(file)
#index= random.randint(1,len(notes_dict))
#notes_list = notes_dict[str(index)] 
notes_list= notes_dict['1']
notes_count=0
pygame.mixer.set_num_channels(len(notes_list))
num_tile=1
scrolling=0
#high_score=0
hp= True
gp= False
overlay_index=0
score=0
speed=2
pos= None
game_over= False
sounds= {note: pygame.mixer.Sound(f'Sounds/{note}.ogg')for note in notes_list}
running = True
while running :
    window.blit(bgimg, (0,0)) #showing an image on a game window
    #takes two parameters- the image and the position where you want to display it
    # 0,0 denotes the top left corner
    score_text = font.render(f'Score: {score}', True, score_color)
    window.blit(score_text, (10, 10))
    for event in pygame.event.get(): #event controls all the events happening in the game
          if event.type== pygame.QUIT: #close button
               running= False
          if event.type == pygame.KEYDOWN:#to detect a key being pressed 
              if event.type == pygame.K_ESCAPE :#if escape key is pressed 
                    running = False
          if event.type == pygame.MOUSEBUTTONDOWN:
               pos= event.pos
               
    if hp:
        window.blit(startimg, start_rect)
        notes_list= notes_dict['1']
        notes_count=0
        pygame.mixer.set_num_channels(len(notes_list))
        if pos and start_rect.collidepoint(pos):
            hp= False
            gp= True
            x= random.randint(0,3)
            t=TILE(x*t_wid, -t_height, window)
            tile_group.add(t)
            pos= None
    if gp:
        for tile in tile_group:
           tile.update(speed)
           score_text = font.render(f'Score: {score}', True, score_color)
           window.blit(score_text, (10, 10))
           if pos:
               if tile.rect.collidepoint(pos):
                 if tile.alive:
                   tile.alive=False
                   score +=1
                   #if score>=high_score:
                       #high_score=score
                   if score > highest_score:
                           highest_score = score

                   #note=notes_list[notes_count]
                   note=notes_list[notes_count].strip()
                   sounds[note].play()
                   #th = Thread(target=play_notes,args=(f'Sounds/{note}.ogg',))
                   #th.start()
                   #pygame.mixer.Sound(f'Sounds/{note}.ogg').play()
                   notes_count=(notes_count + 1)% len(notes_list)
                   #th.join()
                  
           if tile.rect.bottom >= HEIGHT and tile.alive:
               if not game_over:
                endm.play()
                game_over= True
           with open('highest_score.txt', 'w') as file:
                  file.write(str(highest_score))
        if len(tile_group)>0:
                       t=tile_group.sprites()[-1]#returns all sprites in tile group in a list
                       if t.rect.top + speed>=0:
                           x= random.randint(0,3)
                           y= -t_height- (0 - t.rect.top)
                           t=TILE(x*t_wid, -t_height, window)
                       tile_group.add(t)
                       num_tile+=1
    pos=None
    scrolling +=speed
    if game_over:
        
        if overlay_index>20:
            speed=0
            window.blit(bgimg, (0,0))
            display_score(window, score)
            if exit_btn.draw(window):
                running= False

            if replay_btn.draw(window):
                notes_list= notes_dict['1']
                notes_count=0
                pygame.mixer.set_num_channels(len(notes_list))
                tile_group.empty()
                score=0
                speed=2
                overlay_index=0
                game_over= False
                x= random.randint(0,3)
                t= TILE(x* t_wid, -t_height, window)
                tile_group.add(t)
                score_text = font.render(f'Score: {score}', True, score_color)
                window.blit(score_text, (10, 10))
                pygame.display.update()
                
        else:
            overlay_index +=1
            if overlay_index %3 ==0 :
                window.blit(bgimg, (0,0))
    clock.tick(FPS)# number of milliseconds have passed since the previous call
    pygame.display.update()
        
pygame.quit()
