import pygame
from config import *


def fase_credit():
    #starters
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Pui Pui Creditos')
    clock = pygame.time.Clock()

    #fonts
    font = pygame.font.Font("assets/stacked_pixel.ttf", 40)
    font_title = pygame.font.Font("assets/FatPix-SVG.ttf", 70)

    running = True
    while running:

        screen.fill(cyan)

        text = font_title.render("MUSICAS", False, magenta)
        screen.blit(text, (SCREEN_WIDTH/2-text.get_width()/2, 30))

        textm = font.render("https://clement-panchout.itch.io/", False, white)
        screen.blit(textm, (SCREEN_WIDTH/2-textm.get_width()/2, 120))
        textm2 = font.render("yet-another-free-music-pack", False, white)
        screen.blit(textm2, (SCREEN_WIDTH/2-textm2.get_width()/2, 160))

        text2 = font_title.render("ARTE", False, magenta)
        screen.blit(text2, (SCREEN_WIDTH/2-text2.get_width()/2, 220))

        texta = font.render("https://cupnooble.itch.io/", False, white)
        screen.blit(texta, (SCREEN_WIDTH/2-texta.get_width()/2, 300))

        texta2 = font.render("sprout-lands-ui-pack", False, white)
        screen.blit(texta2, (SCREEN_WIDTH/2-texta2.get_width()/2, 340))

        text3 = font_title.render("FONTES", False, magenta)
        screen.blit(text3, (SCREEN_WIDTH/2-text3.get_width()/2, 390))

        textf = font.render("https://ngndang.itch.io/fat-pix-font", False, white)
        screen.blit(textf, (SCREEN_WIDTH/2-textf.get_width()/2, 480))

        textf2 = font.render("https://monkopus.itch.io/stacked-pixel", False, white)
        screen.blit(textf2, (SCREEN_WIDTH/2-textf2.get_width()/2, 530))

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