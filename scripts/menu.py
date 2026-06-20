import pygame
import sys
import config

from pygame import mixer
from fase_song1 import fase_song
from scores import fase_score
from creditos import fase_credit
from paths import *
from config import *

#load images
puipui = pygame.image.load(puipui_path)
puipuidark = pygame.image.load(dark_puipui_path)

play = pygame.image.load(play_path)
plays = pygame.image.load(plays_path)

score = pygame.image.load(score_path)
scores = pygame.image.load(scores_path)

credito = pygame.image.load(credito_path)
creditos = pygame.image.load(creditos_path)

def botoes(asset, screen, x, y):
    retangulo = asset.get_rect(center=(x, y))
    screen.blit(asset, retangulo)

def menu_principal():
    #starters
    pygame.init()
    mixer.music.load(song_menu_path)
    mixer.music.play()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pui Pui MENU")
    clock = pygame.time.Clock()
    start_clock = pygame.time.get_ticks()

    #change background
    change_time = 1000
    puipui_time = True
    old_time=0
    
    config.game_state = "MENU"
    while True:
        actual_time = pygame.time.get_ticks() - start_clock
        mouse_position = pygame.mouse.get_pos()

        if config.game_state == "MENU":
            #starters
            screen.fill(black)

            if actual_time - old_time >= change_time:
                puipui_time = not puipui_time
                old_time = actual_time

            screen.blit(puipui, (0, 0)) if puipui_time else screen.blit(puipuidark, (0, 0))

            #play
            rect_play = pygame.Rect(SCREEN_WIDTH // 2-(BUTTON_WIDTH)//2, 380-(BUTTON_HEIGHT//2), BUTTON_WIDTH, BUTTON_HEIGHT)
            play_button = plays if rect_play.collidepoint(mouse_position) else play
            botoes(play_button, screen, SCREEN_WIDTH // 2, 380)

            #score
            rect_score = pygame.Rect(SCREEN_WIDTH // 2-(BUTTON_WIDTH)//2, 470-(BUTTON_HEIGHT//2), BUTTON_WIDTH, BUTTON_HEIGHT)
            score_button = scores if rect_score.collidepoint(mouse_position) else score
            botoes(score_button, screen, SCREEN_WIDTH // 2, 470)

            #creditos
            rect_credit = pygame.Rect(SCREEN_WIDTH // 2-(BUTTON_WIDTH)//2, 540-(BUTTON_HEIGHT//2), BUTTON_WIDTH, BUTTON_HEIGHT)
            credito_button = creditos if rect_credit.collidepoint(mouse_position) else credito
            botoes(credito_button, screen, SCREEN_WIDTH // 2, 540)



            #events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                #mouse click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1: #left moouse click
                        if rect_play.collidepoint(mouse_position):
                            config.game_state = "playing"
                            mixer.music.stop()
                        if rect_score.collidepoint(mouse_position):
                            config.game_state = "score"
                            mixer.music.stop()
                        if rect_credit.collidepoint(mouse_position):
                            config.game_state = "credit"
                            mixer.music.stop()

        elif config.game_state == "playing":
            fase_song()
            if config.game_state == "repeat":
                config.game_state = "playing"
            else:
                config.game_state = "MENU"
            pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
            pygame.display.set_caption("Pui Pui MENU")
            mixer.music.load(song_menu_path)
            mixer.music.play()

        elif config.game_state == "score":
            fase_score()
        
            config.game_state = "MENU"
            pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
            pygame.display.set_caption("Pui Pui MENU")
            mixer.music.load(song_menu_path)
            mixer.music.play()

        elif config.game_state == "credit":
            fase_credit()
        
            config.game_state = "MENU"
            pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
            pygame.display.set_caption("Pui Pui MENU")
            mixer.music.load(song_menu_path)
            mixer.music.play()

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    menu_principal()