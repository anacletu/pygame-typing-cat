import pygame
from sys import exit
from random import randint, choice, shuffle

pygame.init()

# Fonts
title_font = pygame.font.Font('assets/fonts/PimpawCat-lg3dd.ttf', 80)
game_font = pygame.font.Font('assets/fonts/bohemian-typewriter.regular.ttf', 30)
words_font = pygame.font.Font('assets/fonts/bohemian-typewriter.regular.ttf', 24)

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
        elif action == 'death':
            sprite_sheet = pygame.image.load('assets/images/enemies/skeleton/Death.png')
            frames_per_row = 4  
            frames_per_column = 1

    if enemy == 'flying_eye':
        if action == 'walk':
            sprite_sheet = pygame.image.load('assets/images/enemies/flying_eye/Walk.png')
            frames_per_row = 8  
            frames_per_column = 1  
        elif action == 'attack':
            sprite_sheet = pygame.image.load('assets/images/enemies/flying_eye/Attack.png')
            frames_per_row = 8  
            frames_per_column = 1
        elif action == 'death':
            sprite_sheet = pygame.image.load('assets/images/enemies/flying_eye/Death.png')
            frames_per_row = 4  
            frames_per_column = 1
    
    if enemy == 'goblin':
        if action == 'walk':
            sprite_sheet = pygame.image.load('assets/images/enemies/goblin/Walk.png')
            frames_per_row = 8  
            frames_per_column = 1  
        elif action == 'attack':
            sprite_sheet = pygame.image.load('assets/images/enemies/goblin/Attack.png')
            frames_per_row = 8  
            frames_per_column = 1
        elif action == 'death':
            sprite_sheet = pygame.image.load('assets/images/enemies/goblin/Death.png')
            frames_per_row = 4  
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

        self.attacking = False
        self.health = 0
        self.damage = False
                
    def walk_animation(self):
        self.player_index += 0.15
        if self.player_index >= 15 or self.player_index < 8: self.player_index = 8 # loop through walk frames in sprite sheet 
        self.image = self.player_frames[int(self.player_index)]

        # Limit for player position on the screen
        if self.x_pos < 120:
            self.x_pos += 2.5
            self.rect.midbottom = (self.x_pos, self.y_pos)
    
    def stand_animation(self):
        if self.x_pos < 120: # Making sure character is in the right spot if user starts game too fast
            self.rect.midbottom = (120, self.y_pos)
        
        self.player_index += 0.12
        if self.player_index >= 7: self.player_index = 0 # loop through stand frames in sprite sheet 
        self.image = self.player_frames[int(self.player_index)]

    def damage_animation(self):
        self.player_index += 0.07
        if self.player_index >= 27 or self.player_index < 24: self.player_index = 24 # loop through damage frames in sprite sheet 
        self.image = self.player_frames[int(self.player_index)]

    def attack_animation(self):
        self.player_index += 0.1
        if self.player_index < 56: self.player_index = 56 # loop through attack frames in sprite sheet 
        self.image = self.player_frames[int(self.player_index)]

    def defeated_animation(self):
        if self.player_index > 40 or self.player_index < 32: self.player_index = 32 # loop through damage frames in sprite sheet 
        if int(self.player_index) != 39:
            self.player_index += 0.1
        self.image = self.player_frames[int(self.player_index)]
    
    def health_status(self):
        if self.damage:
            self.health += 0.2
            self.damage = False
    
    def get_health_amount(self):
        return self.health
    
    def update(self, action, word_correct):
        if word_correct:
            self.attacking = True
        if self.player_index >= 63:
                self.attacking = False

        if action == 'walk':
            self.walk_animation()
        elif action == 'stand' and not self.attacking:
            self.stand_animation()
        elif action == 'attack' and self.attacking:
            self.attack_animation()
        elif action == 'damage':
            self.damage_animation()
            self.damage = True
            self.health_status()
        elif action == 'defeated':
            self.defeated_animation()

class Enemies(pygame.sprite.Sprite):
    def __init__(self, screen, type):
        super().__init__()
        self.type = type
        self.enemy_frames = enemies_sprite_sheet(self.type, 'walk')
        self.animation_index = 0

        self.x_pos = randint(810, 900)
        if type == 'flying_eye': self.y_pos = 520
        else: self.y_pos = 605
        self.image = self.enemy_frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(self.x_pos, self.y_pos))

        if type == 'goblin': self.total_health = 50
        else: self.total_health = 100
        self.screen = screen
        self.is_attacking = False

    def get_is_attacking(self):
        return self.is_attacking

    def walk_animation(self):
        if self.type == 'goblin': self.animation_index -= 0.2
        else: self.animation_index -= 0.12
        if self.animation_index <= 0: self.animation_index = 3
        self.image = self.enemy_frames[int(self.animation_index)]
    
    def attack_animation(self):
        self.enemy_frames = enemies_sprite_sheet(self.type, 'attack')
        self.animation_index -= 0.12
        if self.animation_index <= 0: self.animation_index = 7
        self.image = self.enemy_frames[int(self.animation_index)]

    def death_animation(self):
        self.enemy_frames = enemies_sprite_sheet(self.type, 'death')
        if self.animation_index > 3: self.animation_index = 3
        self.animation_index -= 0.1
        self.image = self.enemy_frames[int(self.animation_index)]

    def screen_movement(self):
        if self.x_pos >= 200 and self.total_health > 0: 
            if self.type == 'goblin': self.x_pos -= 2
            else: self.x_pos -= 1
        self.rect.midbottom = (self.x_pos, self.y_pos)

    def health_update(self, word_correct):
        if word_correct and self.x_pos < 800:
            self.total_health -= 15

    def display_health(self):
        health_bar_width = (self.total_health / 100) * 50
        health_color = (0, 255, 0)
        if self.total_health < 50:
            health_color = (255, 0, 0)
        pygame.draw.rect(self.screen, health_color, (self.rect.x + 100, self.rect.y + 80, health_bar_width, 5))
    
    def update(self, word_correct):
        if self.x_pos <= 200 and self.total_health > 0:
            self.attack_animation()
            self.is_attacking = True
        elif self.x_pos > 200 and self.total_health > 0: 
            self.walk_animation()
            self.is_attacking = False
        else:
            self.death_animation()
            self.is_attacking = False
            self.get_is_attacking()
            # Check if the death animation is finished
            if self.animation_index <= 0:
                self.kill()  # Remove the sprite from the group
        
        self.screen_movement()
        self.health_update(word_correct)
        self.display_health()

class PlayerHealth():
    def __init__(self, screen):
        self.heart = pygame.image.load('assets/images/player/heart.png')
        self.containers = []
        self.screen = screen
        self.bleed_control = 0

        for _ in range(5):
            self.heart_rect = self.heart.get_rect()
            self.containers.append(self.heart_rect)
    
    def update_containers(self, health_lost):
        length = len(self.containers)
        if length > 0 and self.bleed_control < health_lost:
            self.containers.pop()
            self.bleed_control += 1   

    def display_hearts(self):
        heart_width = self.heart.get_width()
        padding = 5

        for i, self.heart_rect in enumerate(self.containers):
            x = 548 + i * (heart_width + padding)
            y = 543
            self.screen.blit(self.heart, (x, y))

    def update(self, health_lost):
        self.update_containers(health_lost)
        self.display_hearts()

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
                return_text = self.text
                self.text = ""
                return return_text
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                if len(self.text) < 26:
                    self.text += event.unicode

    def update(self):
        pass

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)
        font_surface = self.font.render(self.text, True, (255, 255, 255))
        screen.blit(font_surface, (self.position[0] + 5, self.position[1] + 5))

class Word:
    def __init__(self, screen, font):
        self.x_pos = randint(150, 650)
        self.y_pos = -50
        self.screen = screen
        self.font = font
        self.word_surface = None
        self.word_rect = None
        self.generate_word()
        self.chosen_word = ""

    def generate_word(self):
        with open('assets/words/words.txt', 'r') as file:
            # Read all lines from the file
            words = file.readlines()

            # Remove newline characters from the words
            words = [word.strip().lower() for word in words]
            used_words = []

            # Ensure that the selected word has not been used before in the game session
            available_words = [word for word in words if word not in used_words]
            if available_words:
                self.chosen_word = choice(available_words)
                used_words.append(self.chosen_word)
            else:
                used_words = []

            # Render the chosen word
            self.word_surface = self.font.render(self.chosen_word, True, (250, 250, 250))
            self.word_rect = self.word_surface.get_rect(center=(self.x_pos, self.y_pos))

    def draw(self):
        self.screen.blit(self.word_surface, self.word_rect)

    def move(self):
        self.y_pos += 2
        self.word_rect.y = self.y_pos
    
    def is_typed_correctly(self, typed_word):
        return typed_word == self.chosen_word

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

    def update(self, typed_word):
        for word in self.words:
            word.update()
            if word.is_typed_correctly(typed_word):
                # Handle correct typed word (e.g., remove the word, increase score)
                self.words.remove(word)
                return True
                # Add your score logic here

    def remove_offscreen_words(self):
        self.words = [word for word in self.words if word.y_pos < SCREEN_HEIGHT + 50]

class GameProgress:
    def __init__(self, screen):
        self.screen = screen
        self.x = 100
        self.y = 20
        self.width = 600
        self.height = 10

        self.victory = False

    def draw(self):
        self.width -= 0.2 # Controls the time to win the game
        pygame.draw.rect(self.screen, (0, 255, 0), (self.x, self.y, self.width, self.height))

    def get_victory(self):
        if self.width <= 0:
            self.victory = True
        return self.victory
    
    def update(self):
        self.draw()

def initialize_game():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Typing Cat")

    background_surf = pygame.image.load('assets/images/environment/background.png').convert()
    foreground_surf = pygame.image.load('assets/images/environment/foreground.png').convert_alpha()
    bg_x = 0

    clock = pygame.time.Clock()

    return screen, background_surf, foreground_surf, bg_x, clock

def difficulty_control():
    time_since_last_word = 0
    time_since_last_enemy = 0
    word_max_speed = 5000
    enemy_max_speed = 10000

    return time_since_last_word, time_since_last_enemy, word_max_speed, enemy_max_speed

def draw_background(screen, background_surf, bg_x):
    screen.blit(background_surf, (bg_x, -50))
    screen.blit(background_surf, (bg_x + background_surf.get_width(), -50))

def draw_foreground(screen, foreground_surf, bg_x):
    screen.blit(foreground_surf, (bg_x, -100))
    screen.blit(foreground_surf, (bg_x + foreground_surf.get_width(), -100))

def draw_intro_screen(screen, input_text, cursor_visible, title_font, game_font, game_state):
    overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 200))

    screen.blit(overlay, (0, 0))

    game_name_font = title_font
    game_name = game_name_font.render('Typing Cat', True, (250, 250, 250))
    game_name_rect = game_name.get_rect(center=(SCREEN_WIDTH // 2, 200))
    screen.blit(game_name, game_name_rect)

    if game_state == INTRO:
        message_lines = ['Type PLAY or QUIT and press ENTER']
    elif game_state == VICTORY:
        message_lines = ['YOU WON! Thanks for playing!', 'Type QUIT to leave the game']

    menu_font = game_font
    line_height = 30 
    for i, line in enumerate(message_lines):
        menu = menu_font.render(line, True, (250, 250, 250))
        menu_rect = menu.get_rect(center=(SCREEN_WIDTH // 2, 350 + i * line_height))
        screen.blit(menu, menu_rect)

    input_surface = menu_font.render(input_text, True, (250, 250, 250))
    input_rect = input_surface.get_rect(center=(SCREEN_WIDTH // 2, 420))
    screen.blit(input_surface, input_rect)

    if cursor_visible:
        cursor_rect = pygame.Rect(input_rect.right, input_rect.y, 2, input_rect.height)
        pygame.draw.rect(screen, (255, 255, 255), cursor_rect)

def draw_game_over_screen(screen, font):
    screen.fill((0,0,0))

    game_over_message = font.render('GAME OVER', True, (250, 250, 250))
    game_over_rect = game_over_message.get_rect(center=(SCREEN_WIDTH // 2, 200))
    screen.blit(game_over_message, game_over_rect)

def main():
    screen, background_surf, foreground_surf, bg_x, clock = initialize_game()
    time_since_last_word, time_since_last_enemy, word_max_speed, enemy_max_speed = difficulty_control()

    # Initialization of game variables
    game_state = INTRO
    user_input = ""
    typed_word = ""
    health_lost = 0
    cursor_blink_timer = 0
    cursor_visible = True
    word_correct = False
    victory = False

    player = pygame.sprite.GroupSingle(Player())
    player_health = PlayerHealth(screen)
    enemies_group = pygame.sprite.Group()
    enemies_group.add(Enemies(screen, choice(['skeleton'])))
    text_box = TextBox(game_font, (20, 540), 500, 45)
    words = FetchWords(screen, words_font)
    progress_bar = GameProgress(screen)

    while True:
        # Update the elapsed time
        elapsed_time = clock.tick(GAME_SPEED)
        word_creation_interval = randint(1000, word_max_speed)  # Time interval in milliseconds
        enemy_creation_interval = randint(6000, enemy_max_speed)
        if word_max_speed > 1002: word_max_speed -= 1
        if enemy_max_speed > 6101: enemy_max_speed -= 100
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN and not game_state == PLAY:
                if event.key == pygame.K_RETURN:
                    if user_input.lower() == 'play':
                        user_input = ""
                        game_state = PLAY
                        break
                    elif user_input.lower() == 'quit':
                        pygame.quit()
                        exit()
                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                else:
                    user_input += event.unicode
            
            if game_state == PLAY: typed_word = text_box.handle_event(event)

        draw_background(screen, background_surf, bg_x)
        
        if game_state == INTRO or game_state == VICTORY:
            draw_intro_screen(screen, user_input, cursor_visible, title_font, game_font, game_state)
            bg_x -= 2
            if bg_x < -background_surf.get_width(): # Wrap the background to create the scrolling effect
                bg_x = 0

            player.draw(screen)
            player.update('walk', word_correct)
            
            # Handle cursor blinking
            cursor_blink_timer += clock.get_rawtime()
            if cursor_blink_timer > 300:  # Blink every 300 milliseconds
                cursor_visible = not cursor_visible
                cursor_blink_timer = 0
        
        if victory:
            game_state = VICTORY
        
        if game_state == PLAY:
            progress_bar.update()
            victory = progress_bar.get_victory()

            player.draw(screen)
            player.x_pos = 120

            time_since_last_enemy += elapsed_time
            if time_since_last_enemy >= enemy_creation_interval:
                enemies_group.add(Enemies(screen, choice(['skeleton', 'flying_eye', 'goblin'])))
                time_since_last_enemy = 0

            enemies_group.draw(screen)
            enemies_group.update(word_correct)

            for enemy in enemies_group:
                if enemy.get_is_attacking(): 
                    player.update('damage', word_correct)
                    break
                else:
                    player.update('stand', word_correct)
                    player.update('attack', word_correct)

            health_lost = player.sprite.get_health_amount() / 10

            if health_lost > 5:
                game_state = GAME_OVER

            # Check if it's time to create a new word
            time_since_last_word += elapsed_time
            if time_since_last_word >= word_creation_interval:
                words.create_word()
                time_since_last_word = 0  # Reset the timer after creating a word

            words.draw()
            word_correct = words.update(typed_word)
            words.remove_offscreen_words()

        # Draw the foreground lastly so it covers previous layers
        draw_foreground(screen, foreground_surf, bg_x)
        if game_state == PLAY:
            text_box.draw(screen)
            text_box.update()
        
        if game_state == PLAY: player_health.update(health_lost)

        if game_state == GAME_OVER:
            draw_game_over_screen(screen, title_font)
            player.draw(screen)
            player.update('defeated', word_correct)
        
        pygame.display.flip()
        clock.tick(GAME_SPEED)

if __name__ == "__main__":
    main()