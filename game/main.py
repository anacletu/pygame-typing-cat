import pygame
from pygame.locals import *
from sys import exit

# Initial setup
pygame.init()
screen = pygame.display.set_mode((1280, 720)) # draws the canvas
clock = pygame.time.Clock()

# Surfaces and assets
icon = pygame.image.load('assets/images/icon.png')
font = pygame.font.Font('assets/fonts/CattieRegular-EaBG8.ttf', 70)

sky_surf = pygame.image.load('assets/images/environment/sky.jpg').convert()
ground_surf = pygame.image.load('assets/images/environment/ground.png').convert_alpha()
text_surf = font.render('Typing Cat', True, 'Black')
text_rect = text_surf.get_rect(midtop = (640, 40))

# Actors
fish1_surf = pygame.image.load('assets/images/actors/fish1.png').convert_alpha()
fish1_rect = fish1_surf.get_rect(midbottom = (1000, 0))

player_surf = pygame.image.load('assets/images/actors/cat.png').convert_alpha()
player_rect = player_surf.get_rect(midbottom = (200, 720))

# Typing
text = ""
typing_surf = font.render(text, True, 'Black')
typing_rect = typing_surf.get_rect(midtop = (640, 200))

pygame.display.set_caption('Typing Cat')
pygame.display.set_icon(icon)

# Game loop
while True:
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: # allows user to close the game and stops the code
            pygame.quit()
            exit()


    screen.blit(sky_surf, (-1280, 0))
    screen.blit(ground_surf, (0, 67))
    
    pygame.draw.rect(screen, 'Orange', text_rect, 6, 20)
    screen.blit(text_surf, text_rect)

    fish1_rect.bottom += 3
    if fish1_rect.top > 720: fish1_rect.bottom = 0

    screen.blit(fish1_surf, fish1_rect)
    screen.blit(player_surf, player_rect)
    screen.blit(typing_surf, typing_rect)

    pygame.display.update()
    clock.tick(60) # max refresh rate