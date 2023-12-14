import pygame
from sys import exit
from random import randint

pygame.init()

# Fonts
title_font = pygame.font.Font('assets/fonts/PimpawCat-lg3dd.ttf', 80)
game_font = pygame.font.Font('assets/fonts/bohemian-typewriter.regular.ttf', 30)

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GAME_SPEED = 60

# Game States
INTRO = 0
PLAY = 1
VICTORY = 2
GAME_OVER = 3

# Preparing the sprites
def player_sprite_sheet():
    sprite_sheet = pygame.image.load('assets/images/player/cat_sprite.png')

    frame_width = 70  
    frame_height = 70  
    frames_per_row = 8  
    frames_per_column = 15  

    frames = []
    for row in range(frames_per_column):
        for col in range(frames_per_row):
            frame = pygame.Rect(col * frame_width, row * frame_height, frame_width, frame_height)
            frames.append(frame)

    individual_frames = [sprite_sheet.subsurface(frame).copy() for frame in frames]

    return individual_frames

def enemies_sprite_sheet(enemy, action):
    if enemy == 'skeleton':
        if action == 'walk':
            sprite_sheet = pygame.image.load('assets/images/enemies/skeleton/Walk.png')
            frames_per_row = 4  
            frames_per_column = 1  
        elif action == 'attack':
            sprite_sheet = pygame.image.load('assets/images/enemies/skeleton/Attack.png')
            frames_per_row = 8  
            frames_per_column = 1  

    frame_width = 300  
    frame_height = 300  

    frames = []
    for row in range(frames_per_column):
        for col in range(frames_per_row):
            frame = pygame.Rect(col * frame_width, row * frame_height, frame_width, frame_height)
            frames.append(frame)

    individual_frames = [sprite_sheet.subsurface(frame).copy() for frame in frames]

    return individual_frames

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.player_frames = player_sprite_sheet()
        self.player_index = 8

        self.x_pos = -100
        self.y_pos = 510
        self.image = self.player_frames[self.player_index]
        self.rect = self.image.get_rect(midbottom=(self.x_pos, self.y_pos))
                
    def walk_animation(self):
        self.player_index += 0.1
        if self.player_index >= 15 or self.player_index < 8: self.player_index = 8 # loop through walk frames in sprite sheet 
        self.image = self.player_frames[int(self.player_index)]

        # Limit for player position on the screen
        if self.x_pos < 130:
            self.x_pos += 2
            self.rect.midbottom = (self.x_pos, self.y_pos)
    
    def stand_animation(self):
        self.player_index += 0.1
        if self.player_index >= 7: self.player_index = 0 # loop through stand frames in sprite sheet 
        self.image = self.player_frames[int(self.player_index)]

    def damage_animation(self):
        self.player_index += 0.07
        if self.player_index >= 27 or self.player_index < 24: self.player_index = 24 # loop through damage frames in sprite sheet 
        self.image = self.player_frames[int(self.player_index)]

    def fight_animation(self):
        self.player_index += 0.1
        if self.player_index >= 62 or self.player_index < 55: self.player_index = 55 # loop through attack frames in sprite sheet 
        self.image = self.player_frames[int(self.player_index)]
    
    def update(self, action):
        if action == 'walk':
            self.walk_animation()
        elif action == 'stand':
            self.stand_animation()
        elif action == 'attack':
            self.fight_animation()
        elif action == 'damage':
            self.damage_animation()

class Enemies(pygame.sprite.Sprite):
    def __init__(self, screen):
        super().__init__()
        self.enemy_frames = enemies_sprite_sheet('skeleton', 'walk')
        self.animation_index = 0

        self.x_pos = randint(900, 1000)
        self.y_pos = 605
        self.image = self.enemy_frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(self.x_pos, self.y_pos))

        self.total_health = 100
        self.screen = screen
        self.is_attacking = False
                
    def walk_animation(self):
        self.animation_index -= 0.1
        if self.animation_index <= 0: self.animation_index = 3
        self.image = self.enemy_frames[int(self.animation_index)]
    
    def attack_animation(self):
        self.enemy_frames = enemies_sprite_sheet('skeleton', 'attack')
        self.animation_index -= 0.12
        if self.animation_index <= 0: self.animation_index = 7
        self.image = self.enemy_frames[int(self.animation_index)]

    def screen_movement(self):
        if self.x_pos >= 200: 
            self.x_pos -= 1
        self.rect.midbottom = (self.x_pos, self.y_pos)

    def health_update(self, word_correct):
        if word_correct:
            self.total_health -= 10

    def display_health(self):
        health_bar_width = (self.total_health / 100) * 50
        health_color = (0, 255, 0)
        if self.total_health < 50:
            health_color = (255, 0, 0)
        pygame.draw.rect(self.screen, health_color, (self.rect.x + 100, self.rect.y + 80, health_bar_width, 5))
    
    def update(self, word_correct):
        if self.x_pos <= 200:
            self.attack_animation()
            self.is_attacking = True
        else: 
            self.walk_animation()
            self.is_attacking = False
        
        self.screen_movement()
        self.health_update(word_correct)
        self.display_health()

class TextBox:
    def __init__(self, font, position, width, height):
        self.font = font
        self.text = ""
        self.position = position
        self.width = width
        self.height = height
        self.rect = pygame.Rect(position[0], position[1], width, height)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                # Process the entered text (e.g., check correctness, trigger actions)
                print("Entered text:", self.text)
                self.text = ""
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode

    def update(self):
        # You can add additional update logic here if needed
        pass

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)
        font_surface = self.font.render(self.text, True, (255, 255, 255))
        screen.blit(font_surface, (self.position[0] + 5, self.position[1] + 5))

class Word:
    def __init__(self, screen, font):
        self.x_pos = randint(100, 700)
        self.y_pos = -50
        self.screen = screen
        self.font = font
        self.word_surface = None
        self.word_rect = None

    def generate_word(self):
        with open('assets/words/words.txt', 'r') as file:
            self.word_surface = self.font.render(file.readline().strip(), True, (250, 250, 250))
            self.word_rect = self.word_surface.get_rect(center=(self.x_pos, self.y_pos))

    def draw(self):
        self.screen.blit(self.word_surface, self.word_rect)

    def move(self):
        self.y_pos += 2
        self.word_rect.y = self.y_pos

    def update(self):
        self.move()

class FetchWords:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.words = []

    def create_word(self):
        word = Word(self.screen, self.font)
        word.generate_word()
        self.words.append(word)

    def draw(self):
        for word in self.words:
            word.draw()

    def update(self):
        for word in self.words:
            word.update()

    def remove_offscreen_words(self):
        self.words = [word for word in self.words if word.y_pos < SCREEN_HEIGHT + 50]

def initialize_game():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Typing Cat")

    background_surf = pygame.image.load('assets/images/environment/background.png').convert()
    foreground_surf = pygame.image.load('assets/images/environment/foreground.png').convert_alpha()
    bg_x = 0

    clock = pygame.time.Clock()

    return screen, background_surf, foreground_surf, bg_x, clock

def draw_background(screen, background_surf, bg_x):
    screen.blit(background_surf, (bg_x, -50))
    screen.blit(background_surf, (bg_x + background_surf.get_width(), -50))

def draw_foreground(screen, foreground_surf, bg_x):
    screen.blit(foreground_surf, (bg_x, -100))
    screen.blit(foreground_surf, (bg_x + foreground_surf.get_width(), -100))

def draw_intro_screen(screen, input_text, cursor_visible, title_font, game_font):
    overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 200)) 

    screen.blit(overlay, (0, 0))

    game_name_font = title_font
    game_name = game_name_font.render('Typing Cat', True, (250, 250, 250))
    game_name_rect = game_name.get_rect(center=(SCREEN_WIDTH // 2, 200))
    screen.blit(game_name, game_name_rect)

    menu_font = game_font
    menu = menu_font.render('Type PLAY or QUIT and press ENTER', True, (250, 250, 250))
    menu_rect = menu.get_rect(center=(SCREEN_WIDTH // 2, 350))
    screen.blit(menu, menu_rect)

    input_surface = menu_font.render(input_text, True, (250, 250, 250))
    input_rect = input_surface.get_rect(center=(SCREEN_WIDTH // 2, 400))
    screen.blit(input_surface, input_rect)

    if cursor_visible:
        cursor_rect = pygame.Rect(input_rect.right, input_rect.y, 2, input_rect.height)
        pygame.draw.rect(screen, (255, 255, 255), cursor_rect)

def main():
    screen, background_surf, foreground_surf, bg_x, clock = initialize_game()

    game_state = INTRO
    user_input = ""
    cursor_blink_timer = 0
    cursor_visible = True
    word_correct = False

    player = pygame.sprite.GroupSingle(Player())
    enemies = pygame.sprite.GroupSingle(Enemies(screen))
    text_box = TextBox(game_font, (20, 540), 220, 45)
    words = FetchWords(screen, game_font)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_f:pygame.display.toggle_fullscreen()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if user_input.lower() == 'play':
                        game_state = PLAY
                        break
                    elif user_input.lower() == 'quit':
                        pygame.quit()
                        exit()
                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                else:
                    user_input += event.unicode
            
            text_box.handle_event(event)

        draw_background(screen, background_surf, bg_x)
        
        if game_state == INTRO:
            draw_intro_screen(screen, user_input, cursor_visible, title_font, game_font)
            bg_x -= 2
            if bg_x < -background_surf.get_width(): # Wrap the background to create the scrolling effect
                bg_x = 0

            player.draw(screen)
            player.update('walk')
            
            # Handle cursor blinking
            cursor_blink_timer += clock.get_rawtime()
            if cursor_blink_timer > 300:  # Blink every 300 milliseconds
                cursor_visible = not cursor_visible
                cursor_blink_timer = 0
        
        if game_state == PLAY:
            player.draw(screen)

            if enemies.sprite.is_attacking:
                player.update('damage')
            else:
                player.update('stand')

            enemies.draw(screen)
            enemies.update(word_correct)

            if randint(1, 500) < 5:  # Adjust the probability as needed
                words.create_word()

            words.draw()
            words.update()
            words.remove_offscreen_words()

        # Draw the foreground lastly so it covers previous layers
        draw_foreground(screen, foreground_surf, bg_x)
        if game_state == PLAY:
            text_box.draw(screen)
            text_box.update()
        
        pygame.display.flip()
        clock.tick(GAME_SPEED)

if __name__ == "__main__":
    main()