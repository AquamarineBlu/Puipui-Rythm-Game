import pygame
import config
from config import *
from paths import *


def fase_score():
    #starters
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    background = pygame.image.load(background_path)
    pygame.display.set_caption('Pui Pui Placar')
    clock = pygame.time.Clock()

    #fonts
    font = pygame.font.Font("assets/stacked_pixel.ttf", 50)
    font_placar = pygame.font.Font("assets/FatPix-SVG.ttf", 70)

    running = True
    while running:
        config.placar.sort(reverse=True)

        screen.fill(black)
        screen.blit(background, (0, 0))

        text = font_placar.render("PLACAR:", False, white)
        screen.blit(text, (SCREEN_WIDTH/2-text.get_width()/2, 50))

        if len(placar)>0:
            score0 = font.render(f"{placar[0]}", False, blue)
            screen.blit(score0, (SCREEN_WIDTH/2-score0.get_width()/2, 180))

        if len(placar)>1:
            score1 = font.render(f"{placar[1]}", False, blue)
            screen.blit(score1, (SCREEN_WIDTH/2-score1.get_width()/2, 250))

        if len(placar)>2:
            score2 = font.render(f"{placar[2]}", False, blue)
            screen.blit(score2, (SCREEN_WIDTH/2-score2.get_width()/2, 320))

        if len(placar)>3:
            score3 = font.render(f"{placar[3]}", False, blue)
            screen.blit(score3, (SCREEN_WIDTH/2-score3.get_width()/2, 390))

        if len(placar)>4:
            score4 = font.render(f"{placar[4]}", False, blue)
            screen.blit(score4, (SCREEN_WIDTH/2-score4.get_width()/2, 460))

        if len(placar)>5:
            score5 = font.render(f"{placar[5]}", False, blue)
            screen.blit(score5, (SCREEN_WIDTH/2-score5.get_width()/2, 530))

        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

        pygame.display.flip()
        clock.tick(60)