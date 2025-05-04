import pygame
import subprocess
import sys
import os

# Initialize Pygame
pygame.init()

# Set up screen
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🕹️ Main Game Menu")
clock = pygame.time.Clock()

# Fonts
font = pygame.font.Font(None, 60)

# Load background image
try:
    bg_image = pygame.image.load("images/path.png")  # Path to background
    bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))
except Exception as e:
    print(f"Failed to load background image: {e}")
    bg_image = None

# Load button images
use_images = True
try:
    level1_img = pygame.image.load("images/level1.png")  # Path to Level 1 button
    level1_img = pygame.transform.scale(level1_img, (250, 80))
    
    level2_img = pygame.image.load("images/LEVEL2.png")  # Path to Level 2 button
    level2_img = pygame.transform.scale(level2_img, (250, 80))
except Exception as e:
    print(f"Failed to load button images: {e}")
    use_images = False

def draw_main_menu():
    if bg_image:
        screen.blit(bg_image, (0, 0))
    else:
        screen.fill((25, 25, 112))  # fallback to solid color

    # Title
    title = font.render("Game Main Menu", True, 'white')
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 60))

    # Draw buttons
    if use_images:
        level1_btn = screen.blit(level1_img, (WIDTH // 2 - 125, 220))  # 250/2 = 125
        level2_btn = screen.blit(level2_img, (WIDTH // 2 - 125, 350))
    else:
        # Fallback to rectangles if images not available
        BUTTON_WIDTH, BUTTON_HEIGHT = 250, 80
        button_color1 = (70, 130, 180)
        button_color2 = (255, 140, 0)
        level1_btn = pygame.draw.rect(screen, button_color1, (WIDTH // 2 - 125, 220, BUTTON_WIDTH, BUTTON_HEIGHT), border_radius=12)
        level2_btn = pygame.draw.rect(screen, button_color2, (WIDTH // 2 - 125, 350, BUTTON_WIDTH, BUTTON_HEIGHT), border_radius=12)

    return level1_btn, level2_btn

def launch_level(script_name):
    try:
        subprocess.Popen([sys.executable, script_name])
    except Exception as e:
        print(f"Failed to launch {script_name}: {e}")

def main():
    running = True
    while running:
        clock.tick(60)
        level1_btn, level2_btn = draw_main_menu()
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if level1_btn.collidepoint(event.pos):
                    launch_level("puzzlelevel1.py")
                elif level2_btn.collidepoint(event.pos):
                    launch_level("puzzlelevel2.py")

    pygame.quit()

if __name__ == "__main__":
    main()





