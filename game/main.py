import pygame
from sys import exit
from random import randint

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load('assets/images/player/walk1.png').convert_alpha()
        player_walk_2 = pygame.image.load('assets/images/player/walk2.png').convert_alpha()
        self.player_walk = [player_walk_1,player_walk_2]
        self.player_index = 0

        self.x_pos = -100
        self.y_pos = 665
        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (self.x_pos, self.y_pos))
                
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
    def __init__(self):
        super().__init__()
        skeleton_walk_1 = pygame.image.load('assets/images/enemies/skeleton/walk1.png').convert_alpha()
        skeleton_walk_2 = pygame.image.load('assets/images/enemies/skeleton/walk2.png').convert_alpha()
        skeleton_walk_3 = pygame.image.load('assets/images/enemies/skeleton/walk3.png').convert_alpha()
        skeleton_walk_4 = pygame.image.load('assets/images/enemies/skeleton/walk4.png').convert_alpha()
        self.skeleton_walk = [skeleton_walk_1, skeleton_walk_2, skeleton_walk_3, skeleton_walk_4]
        
        self.x_pos = randint(1300,1400)
        self.y_pos = 675
        self.animation_index = 0
        self.image = self.skeleton_walk[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (self.x_pos, self.y_pos))
                
    def walk_animation(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.skeleton_walk): self.animation_index = 0
        self.image = self.skeleton_walk[int(self.animation_index)]

    def screen_movement(self):
        self.x_pos -= 1
        self.rect.midbottom = (self.x_pos, self.y_pos)
    
    def update(self):
        self.walk_animation()
        self.screen_movement()

def initialize_game():
    pygame.init()

    width, height = 1280, 720
    screen = pygame.display.set_mode((width, height))
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
    # Create a semi-transparent dark overlay
    overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 200)) 

    screen.blit(overlay, (0, 0))

    game_name_font = pygame.font.Font('assets/fonts/PimpawCat-lg3dd.ttf', 80)
    game_name = game_name_font.render('Typing Cat', True, (250, 250, 250))
    game_name_rect = game_name.get_rect(center = (640, 200))
    screen.blit(game_name, game_name_rect)

    menu_font = pygame.font.Font('assets/fonts/bohemian-typewriter.regular.ttf', 40)
    menu = menu_font.render('Type PLAY or QUIT and press ENTER', True, (250, 250, 250))
    menu_rect = menu.get_rect(center = (640, 400))
    screen.blit(menu, menu_rect)

    input_surface = menu_font.render(input_text, True, (250, 250, 250))
    input_rect = input_surface.get_rect(center=(640, 450))
    screen.blit(input_surface, input_rect)

    if cursor_visible:
        cursor_rect = pygame.Rect(input_rect.right, input_rect.y, 2, input_rect.height)
        pygame.draw.rect(screen, (255, 255, 255), cursor_rect)

def main():
    screen, background_surf, foreground_surf, bg_x, clock = initialize_game()

    screen_type = 0
    user_input = ""
    cursor_blink_timer = 0
    cursor_visible = True

    #Groups
    player = pygame.sprite.GroupSingle()
    player.add(Player())
    enemies = pygame.sprite.GroupSingle()
    enemies.add(Enemies())

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if user_input.lower() == 'play':
                        print("Starting the game!")
                        screen_type = 1  # Transition to the game state
                        break  # Break out of the while loop
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

        if screen_type == 0:
            draw_intro_screen(screen, user_input, cursor_visible)
            
            # Handle cursor blinking
            cursor_blink_timer += clock.get_rawtime()
            if cursor_blink_timer > 300:  # Blink every 300 milliseconds
                cursor_visible = not cursor_visible
                cursor_blink_timer = 0

        if screen_type == 1:
            player.draw(screen)
            player.update()
            enemies.draw(screen)
            enemies.update()

        # Draw the foreground lastly so it covers previous layers
        draw_foreground(screen, foreground_surf, bg_x)
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()