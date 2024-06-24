import pygame
import sys
import random
from pygame.locals import QUIT, KEYDOWN, KEYUP, K_a, K_z, K_UP, K_DOWN

# Initialize Pygame
pygame.init()

# Set up the display
screen_width, screen_height = 1920, 1017
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Eagle Eats Cooking Simulator')

# Load the background images
try:
    title_background = pygame.image.load('title.png')
    game_background_image = pygame.image.load('gamescreen.png')  # Replace with your game background image file
    game_background_image = pygame.transform.scale(game_background_image, (screen_width, screen_height))  # Scale to match screen size
    tutorial_background_image = pygame.image.load('tutorial.png')
    tutorial_background_image = pygame.transform.scale(tutorial_background_image, (screen_width, screen_height))
    credits_background_image = pygame.image.load('credits.png')
    credits_background_image = pygame.transform.scale(credits_background_image, (screen_width, screen_height))
    win_background_image = pygame.image.load('win.jpg')  # Add a win screen image
    win_background_image = pygame.transform.scale(win_background_image, (screen_width, screen_height))
except pygame.error as e:
    print("Failed to load image:", e)
    sys.exit()

# Load background music
pygame.mixer.music.load('background_music.mp3')
pygame.mixer.music.play(-1)  # -1 means loop indefinitely

pause_background = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
pause_background.fill((0, 0, 0, 180))  # A semi-transparent black background for the pause menu

# Define button colors
button_color = (0, 128, 0)
button_hover_color = (0, 255, 0)
text_color = (255, 255, 255)
lives_color = (0, 0, 0)

# Define button properties
button_font = pygame.font.Font(None, 50)

buttons = {
    "Tutorial": pygame.Rect(400, 680, 300, 100),
    "Play": pygame.Rect(810, 680, 300, 100),
    "Credits": pygame.Rect(1220, 680, 300, 100),
}

pause_buttons = {
    "Resume": pygame.Rect(810, 400, 300, 100),
    "Tutorial": pygame.Rect(810, 550, 300, 100),  # New button for Tutorial in pause menu
    "Quit": pygame.Rect(810, 700, 300, 100),
}

# Initial game state
in_game = False
pause_game = False
in_tutorial = False  # Flag for tutorial screen
in_credits = False  # Flag for credits screen
in_win_screen = False  # Flag for win screen

# Define object properties
class FallingObject(pygame.sprite.Sprite):
    def __init__(self, image_path):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width)  # Random x position across the screen width
        self.rect.y = random.randint(-2 * screen_height, -self.rect.height)  # Start above the screen
        self.speed = random.randint(7, 15)  # Random speed (adjust as needed for slower falling)

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > screen_height:
            self.kill()  # Remove object when it goes off screen

# Create sprite groups
all_sprites = pygame.sprite.Group()
object_type1_group = pygame.sprite.Group()
object_type2_group = pygame.sprite.Group()
object_type3_group = pygame.sprite.Group()
object_type4_group = pygame.sprite.Group()
object_type5_group = pygame.sprite.Group()

# Maximum number of falling objects allowed for each type
max_objects_type1 = 2
max_objects_type2 = 2
max_objects_type3 = 2
max_objects_type4 = 2
max_objects_type5 = 2

# Tick delay variables
tick_delay_type1 = 0
tick_delay_type2 = 0
tick_delay_type3 = 0
tick_delay_type4 = 0
tick_delay_type5 = 0
max_tick_delay = 60  # Adjust this value as needed for longer or shorter delays

# Life system
lives = 3
life_font = pygame.font.Font(None, 75)

# Score system
score = 0
score_font = pygame.font.Font(None, 75)

def draw_lives():
    life_text = life_font.render(f"Lives: {lives}", True, lives_color)
    life_rect = life_text.get_rect(center=(screen_width // 2, 20 + life_text.get_height() // 2))
    screen.blit(life_text, life_rect)

def draw_score():
    score_text = score_font.render(f"Score: {score}", True, lives_color)
    score_rect = score_text.get_rect(center=(screen_width // 2, 80 + score_text.get_height() // 2))
    screen.blit(score_text, score_rect)

def draw_buttons():
    for text, rect in buttons.items():
        if not in_game and not in_tutorial and not in_credits and not in_win_screen:  # Draw buttons only if not in game, tutorial, credits, or win screen
            color = button_hover_color if rect.collidepoint(pygame.mouse.get_pos()) else button_color
            pygame.draw.rect(screen, color, rect)
            text_surf = button_font.render(text, True, text_color)
            text_rect = text_surf.get_rect(center=rect.center)
            screen.blit(text_surf, text_rect)

def draw_pause_menu():
    screen.blit(pause_background, (0, 0))
    for text, rect in pause_buttons.items():
        color = button_hover_color if rect.collidepoint(pygame.mouse.get_pos()) else button_color
        pygame.draw.rect(screen, color, rect)
        text_surf = button_font.render(text, True, text_color)
        text_rect = text_surf.get_rect(center=rect.center)
        screen.blit(text_surf, text_rect)

def draw_tutorial_screen():
    screen.fill((0, 0, 0))  # Clear the screen with black
    screen.blit(tutorial_background_image, (0, 0))

    back_button_rect = pygame.Rect(50, 50, 150, 50)
    pygame.draw.rect(screen, text_color, back_button_rect)
    back_button_text = button_font.render("Back", True, text_color)
    screen.blit(back_button_text, back_button_rect)

    return back_button_rect

def draw_credits_screen():
    screen.fill((0, 0, 0))  # Clear the screen with black
    screen.blit(credits_background_image, (0, 0))

    back_button_rect = pygame.Rect(50, 50, 150, 50)
    pygame.draw.rect(screen, text_color, back_button_rect)
    back_button_text = button_font.render("Back", True, text_color)
    screen.blit(back_button_text, back_button_rect)

    return back_button_rect

def draw_win_screen():
    screen.fill((0, 0, 0))  # Clear the screen with black
    screen.blit(win_background_image, (0, 0))

    back_button_rect = pygame.Rect(50, 50, 150, 50)
    pygame.draw.rect(screen, text_color, back_button_rect)
    back_button_text = button_font.render("Back", True, text_color)
    screen.blit(back_button_text, back_button_rect)

    return back_button_rect

# Main loop
running = True
clock = pygame.time.Clock()

# Define player box properties
player_box_width, player_box_height = 150, 30
player_box_color = (255, 0, 0)
player_box_speed = 10

player_box = pygame.Rect(screen_width // 2 - player_box_width // 2, screen_height - player_box_height - 10, player_box_width, player_box_height)

while running:
    keys = pygame.key.get_pressed()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                if not in_game and not in_tutorial and not in_credits and not in_win_screen:
                    for text, rect in buttons.items():
                        if rect.collidepoint(event.pos):
                            print(f"{text} button clicked!")
                            if text == "Play":
                                in_game = True  # Transition to the game screen
                            elif text == "Tutorial":
                                in_tutorial = True  # Show tutorial screen
                            elif text == "Credits":
                                in_credits = True  # Show credits screen
                elif pause_game:
                    for text, rect in pause_buttons.items():
                        if rect.collidepoint(event.pos):
                            print(f"{text} button clicked!")
                            if text == "Resume":
                                pause_game = False  # Resume the game
                            elif text == "Tutorial":
                                in_tutorial = True  # Show tutorial screen
                            elif text == "Quit":
                                in_game = False  # Return to the title screen
                                pause_game = False
                elif in_tutorial:
                    back_button_rect = draw_tutorial_screen()  # Draw the tutorial screen
                    if back_button_rect.collidepoint(event.pos):
                        in_tutorial = False  # Return to the game from tutorial screen
                elif in_credits:
                    back_button_rect = draw_credits_screen()  # Draw the credits screen
                    if back_button_rect.collidepoint(event.pos):
                        in_credits = False  # Return to the game from credits screen
                elif in_win_screen:
                    back_button_rect = draw_win_screen()  # Draw the win screen
                    if back_button_rect.collidepoint(event.pos):
                        in_win_screen = False  # Return to the title screen
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if in_game:
                    pause_game = not pause_game  # Toggle pause state
            elif event.key == pygame.K_f:  # Toggle fullscreen on 'F' key press
                pygame.display.toggle_fullscreen()

    screen.fill((0, 0, 0))  # Clear the screen

    if in_game:
        screen.blit(game_background_image, (0, 0))  # Draw the game background image

        if not pause_game:
            # Tick delay logic for spawning falling objects
            if tick_delay_type1 > 0:
                tick_delay_type1 -= 1
            elif len(object_type1_group) < max_objects_type1 and random.random() < 0.02:
                new_object = FallingObject('topBun.png')
                all_sprites.add(new_object)
                object_type1_group.add(new_object)
                tick_delay_type1 = max_tick_delay

            if tick_delay_type2 > 0:
                tick_delay_type2 -= 1
            elif len(object_type2_group) < max_objects_type2 and random.random() < 0.02:
                new_object = FallingObject('bottomBun.png')
                all_sprites.add(new_object)
                object_type2_group.add(new_object)
                tick_delay_type2 = max_tick_delay

            if tick_delay_type3 > 0:
                tick_delay_type3 -= 1
            elif len(object_type3_group) < max_objects_type3 and random.random() < 0.02:
                new_object = FallingObject('tomatoes.png')
                all_sprites.add(new_object)
                object_type3_group.add(new_object)
                tick_delay_type3 = max_tick_delay

           # Falling objects spawning logic continued...

            # Objects of type 4
            if tick_delay_type4 > 0:
                tick_delay_type4 -= 1
            elif len(object_type4_group) < max_objects_type4 and random.random() < 0.02:
                new_object = FallingObject('cheese.png')
                all_sprites.add(new_object)
                object_type4_group.add(new_object)
                tick_delay_type4 = max_tick_delay

            # Objects of type 5
            if tick_delay_type5 > 0:
                tick_delay_type5 -= 1
            elif len(object_type5_group) < max_objects_type5 and random.random() < 0.02:
                new_object = FallingObject('lettuce.png')
                all_sprites.add(new_object)
                object_type5_group.add(new_object)
                tick_delay_type5 = max_tick_delay

            # Update and draw all falling objects
            all_sprites.update()
            all_sprites.draw(screen)

            # Collision detection with the player box
            for group in [object_type1_group, object_type2_group, object_type3_group, object_type4_group, object_type5_group]:
                for obj in group:
                    if obj.rect.colliderect(player_box):
                        obj.kill()  # Remove object when it collides with the player box
                        score += 1  # Increment the score
                        if score >= 160:
                            in_game = False  # End the game
                            in_win_screen = True  # Show win screen

            # Check if objects hit the ground
            for group in [object_type1_group, object_type2_group, object_type3_group, object_type4_group, object_type5_group]:
                for obj in group:
                    if obj.rect.y >= screen_height:
                        obj.kill()
                        lives -= 1
                        if lives <= 0:
                            # Game over condition
                            in_game = False
                            pause_game = False
                            lives = 3  # Reset lives for next game
                            score = 0  # Reset score for next game

            draw_lives()  # Draw lives counter
            draw_score()  # Draw score counter

            # Update player box position based on keyboard input
            if keys[pygame.K_LEFT] and player_box.left > 0:
                player_box.x -= player_box_speed
            if keys[pygame.K_RIGHT] and player_box.right < screen_width:
                player_box.x += player_box_speed

            # Draw player box
            pygame.draw.rect(screen, player_box_color, player_box)

        else:
            draw_pause_menu()  # Draw the pause menu if game is paused

    elif in_tutorial:
        back_button_rect = draw_tutorial_screen()  # Draw the tutorial screen
        if back_button_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, button_hover_color, back_button_rect)
        else:
            pygame.draw.rect(screen, button_color, back_button_rect)
    elif in_credits:
        back_button_rect = draw_credits_screen()  # Draw the credits screen
        if back_button_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, button_hover_color, back_button_rect)
        else:
            pygame.draw.rect(screen, button_color, back_button_rect)
    elif in_win_screen:
        back_button_rect = draw_win_screen()  # Draw the win screen
        if back_button_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, button_hover_color, back_button_rect)
        else:
            pygame.draw.rect(screen, button_color, back_button_rect)
    else:
        screen.blit(title_background, (0, 0))  # Draw the title screen background

    draw_buttons()  # Draw buttons outside of in_game and in_tutorial checks

    pygame.display.flip()
    clock.tick(60)  # Cap the frame rate at 60 FPS

pygame.quit()
sys.exit()
