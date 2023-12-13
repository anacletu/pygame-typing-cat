import pygame
from sys import exit
from random import randint

# Constants
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
GAME_SPEED = 60

# Game States
INTRO = 0
WALK = 1
FIGHT = 2
VICTORY = 3
GAME_OVER = 4 

PLAYER_WALK_IMAGES = [
    'assets/images/player/walk1.png',
    'assets/images/player/walk2.png'
]

SKELETON_WALK_IMAGES = [
    'assets/images/enemies/skeleton/walk1.png',
    'assets/images/enemies/skeleton/walk2.png',
    'assets/images/enemies/skeleton/walk3.png',
    'assets/images/enemies/skeleton/walk4.png'
]

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.player_walk = [pygame.image.load(image).convert_alpha() for image in PLAYER_WALK_IMAGES]
        self.player_index = 0

        self.x_pos = -100
        self.y_pos = 665
        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(self.x_pos, self.y_pos))
                
    def walk_animation(self):
        self.player_index += 0.1
        if self.player_index >= len(self.player_walk): self.player_index = 0
        self.image = self.player_walk[int(self.player_index)]
    
    def update(self):
        self.walk_animation()
        
        # Check if player is still entering the screen
        if self.x_pos < 150:
            self.x_pos += 3
            self.rect.midbottom = (self.x_pos, self.y_pos)

class Enemies(pygame.sprite.Sprite):
    def __init__(self, screen):
        super().__init__()
        self.skeleton_walk = [pygame.image.load(image).convert_alpha() for image in SKELETON_WALK_IMAGES]
        
        self.x_pos = randint(1300, 1400)
        self.y_pos = 675
        self.animation_index = 0
        self.image = self.skeleton_walk[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(self.x_pos, self.y_pos))

        self.total_health = 100
        self.screen = screen
                
    def walk_animation(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.skeleton_walk): self.animation_index = 0
        self.image = self.skeleton_walk[int(self.animation_index)]

    def screen_movement(self):
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
        pygame.draw.rect(self.screen, health_color, (self.rect.x, self.rect.y - 10, health_bar_width, 5))
    
    def update(self, word_correct):
        self.walk_animation()
        self.screen_movement()
        self.health_update(word_correct)
        self.display_health()

def initialize_game():
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Typing Cat")

    background_surf = pygame.image.load('assets/images/environment/background.png').convert()
    foreground_surf = pygame.image.load('assets/images/environment/foreground.png').convert_alpha()
    bg_x = 0

    clock = pygame.time.Clock()

    return screen, background_surf, foreground_surf, bg_x, clock

def draw_background(screen, background_surf, bg_x):
    screen.blit(background_surf, (bg_x, 0))
    screen.blit(background_surf, (bg_x + background_surf.get_width(), 0))

def draw_foreground(screen, foreground_surf, bg_x):
    screen.blit(foreground_surf, (bg_x, 20))
    screen.blit(foreground_surf, (bg_x + foreground_surf.get_width(), 20))

def draw_intro_screen(screen, input_text, cursor_visible):
    overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 200)) 

    screen.blit(overlay, (0, 0))

    game_name_font = pygame.font.Font('assets/fonts/PimpawCat-lg3dd.ttf', 80)
    game_name = game_name_font.render('Typing Cat', True, (250, 250, 250))
    game_name_rect = game_name.get_rect(center=(SCREEN_WIDTH // 2, 200))
    screen.blit(game_name, game_name_rect)

    menu_font = pygame.font.Font('assets/fonts/bohemian-typewriter.regular.ttf', 40)
    menu = menu_font.render('Type PLAY or QUIT and press ENTER', True, (250, 250, 250))
    menu_rect = menu.get_rect(center=(SCREEN_WIDTH // 2, 400))
    screen.blit(menu, menu_rect)

    input_surface = menu_font.render(input_text, True, (250, 250, 250))
    input_rect = input_surface.get_rect(center=(SCREEN_WIDTH // 2, 450))
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

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if user_input.lower() == 'play':
                        print("Starting the game!")
                        game_state = WALK  # Transition to the walk state
                        break
                    elif user_input.lower() == 'quit':
                        pygame.quit()
                        exit()
                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                else:
                    user_input += event.unicode

        # Update background position
        bg_x -= 2

        # Wrap the background to create the scrolling effect
        if bg_x < -background_surf.get_width():
            bg_x = 0

        # Draw the background using the functions
        draw_background(screen, background_surf, bg_x)

        if game_state == INTRO:
            draw_intro_screen(screen, user_input, cursor_visible)
            
            # Handle cursor blinking
            cursor_blink_timer += clock.get_rawtime()
            if cursor_blink_timer > 300:  # Blink every 300 milliseconds
                cursor_visible = not cursor_visible
                cursor_blink_timer = 0

        if game_state == WALK:
            player.draw(screen)
            player.update()
            enemies.draw(screen)
            enemies.update(word_correct)

        # Draw the foreground lastly so it covers previous layers
        draw_foreground(screen, foreground_surf, bg_x)
        pygame.display.flip()
        clock.tick(GAME_SPEED)

if __name__ == "__main__":
    main()