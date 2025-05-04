import pygame
import subprocess
import sys
import os

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Word Builder Game")
font = pygame.font.Font('freesansbold.ttf', 36)
small_font = pygame.font.Font('freesansbold.ttf', 20)
clock = pygame.time.Clock()

# Load background image
background = pygame.image.load("images/builder.webp")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Load level images
level1_img = pygame.image.load("images/level1.png")
level2_img = pygame.image.load("images/LEVEL2.png")

# Scale both to same height while preserving aspect ratio
img_height = 100
level1_ratio = level1_img.get_width() / level1_img.get_height()
level2_ratio = level2_img.get_width() / level2_img.get_height()

level1_img = pygame.transform.scale(level1_img, (int(level1_ratio * img_height), img_height))
level2_img = pygame.transform.scale(level2_img, (int(level2_ratio * img_height), img_height))

def draw_main_menu():
    screen.blit(background, (0, 0))  # Draw background first
    title = font.render("Word Builder Game", True, 'darkblue')
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 60))

    instruction_lines = [
        "Improve your vocabulary and spelling!",
        "Click a level to begin."
    ]
    for i, line in enumerate(instruction_lines):
        line_text = small_font.render(line, True, 'black')
        screen.blit(line_text, (WIDTH // 2 - line_text.get_width() // 2, 140 + i * 30))

    # Display level buttons
    level1_btn = screen.blit(level1_img, (WIDTH // 2 - level1_img.get_width() // 2, 250))
    level2_btn = screen.blit(level2_img, (WIDTH // 2 - level2_img.get_width() // 2, 380))
    return level1_btn, level2_btn

def launch_game(script):
    """Launch the specified game script."""
    if getattr(sys, 'frozen', False):
        script_path = os.path.join(os.path.dirname(sys.executable), script)
    else:
        script_path = script
    subprocess.Popen([sys.executable, script_path])

# Main loop
run = True
while run:
    level1_btn, level2_btn = draw_main_menu()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if level1_btn.collidepoint(event.pos):
                launch_game("builder_level1.py")
            elif level2_btn.collidepoint(event.pos):
                launch_game("builder_level2.py")

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
