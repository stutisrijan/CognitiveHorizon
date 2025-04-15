import pygame
import subprocess
import sys
import os

pygame.init()

WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🧠 90s Quiz Game")
font = pygame.font.Font(None, 48)
small_font = pygame.font.Font(None, 28)
clock = pygame.time.Clock()

# Load background image or fallback to color
try:
    bg_image = pygame.image.load("images/quiz_bg.jpg")
    bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))
except:
    bg_image = None

# Load button images or draw basic buttons
use_images = True
try:
    level1_img = pygame.image.load("images/level1.png")
    level1_img = pygame.transform.scale(level1_img, (200, 80))
    level2_img = pygame.image.load("images/LEVEL2.png")
    level2_img = pygame.transform.scale(level2_img, (200, 80))
except:
    use_images = False

def draw_main_menu():
    if bg_image:
        screen.blit(bg_image, (0, 0))
    else:
        screen.fill((30, 30, 60))

    title = font.render("Quiz", True, 'white')
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2,40))

    if use_images:
        level1_btn = screen.blit(level1_img, (200, 220))
        level2_btn = screen.blit(level2_img, (200, 340))
    else:
        level1_btn = pygame.draw.rect(screen, 'dodgerblue', (200, 220, 200, 80), border_radius=10)
        level2_btn = pygame.draw.rect(screen, 'darkorange', (200, 340, 200, 80), border_radius=10)
        l1 = small_font.render("Level 1", True, 'white')
        l2 = small_font.render("Level 2", True, 'white')
        screen.blit(l1, (level1_btn.x + 60, level1_btn.y + 25))
        screen.blit(l2, (level2_btn.x + 60, level2_btn.y + 25))

    return level1_btn, level2_btn

def launch_level(script_name):
    subprocess.Popen([sys.executable, script_name])

def main():
    running = True
    while running:
        clock.tick(60)
        level1_btn, level2_btn = draw_main_menu()
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if level1_btn.collidepoint(event.pos):
                    launch_level("quizlevel1.py")
                elif level2_btn.collidepoint(event.pos):
                    launch_level("quizlevel2.py")

    pygame.quit()

if __name__ == "__main__":

    main()