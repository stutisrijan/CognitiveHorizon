import pygame
import sys
import subprocess

pygame.init()

# Window setup
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Memory Game Menu")

# Load background
background = pygame.image.load("images/memoryback.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Load button images
level1_img = pygame.image.load("images/level1.png")
level1_img = pygame.transform.scale(level1_img, (200, 80))
level2_img = pygame.image.load("images/level2.png")
level2_img = pygame.transform.scale(level2_img, (200, 80))

# Font setup
title_font = pygame.font.SysFont("comicsansms", 48, bold=True)
exit_font = pygame.font.SysFont("arial", 28, bold=True)
WHITE = (255, 255, 255)

# Button rectangles
level1_rect = level1_img.get_rect(center=(WIDTH // 2, 160))
level2_rect = level2_img.get_rect(center=(WIDTH // 2, 250))
exit_rect = pygame.Rect(WIDTH - 100, 20, 80, 30)

# Game launching functions
def launch_level1():
    subprocess.run(["python", "memorynum.py"])

def launch_level2():
    subprocess.run(["python", "memoryimg.py"])

# Main loop
running = True
while running:
    screen.blit(background, (0, 0))

    # Title
    title_text = title_font.render("Memory Game", True, WHITE)
    screen.blit(title_text, title_text.get_rect(center=(WIDTH // 2, 60)))

    # Buttons
    screen.blit(level1_img, level1_rect.topleft)
    screen.blit(level2_img, level2_rect.topleft)

    # Exit
    exit_text = exit_font.render("Exit", True, WHITE)
    screen.blit(exit_text, (exit_rect.x, exit_rect.y))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if level1_rect.collidepoint(event.pos):
                launch_level1()
            elif level2_rect.collidepoint(event.pos):
                launch_level2()
            elif exit_rect.collidepoint(event.pos):
                pygame.quit()
                sys.exit()

    pygame.display.flip()
