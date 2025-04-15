import pygame
import subprocess
import sys
import os

pygame.init()

WIDTH, HEIGHT = 500, 550
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Water Sort Puzzle")
font = pygame.font.Font('freesansbold.ttf', 32)
small_font = pygame.font.Font('freesansbold.ttf', 18)
fps = 60
timer = pygame.time.Clock()

# Load images
bg_image = pygame.image.load("images/sortback.webp")
bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))

level1_img = pygame.image.load("images/level1.png")
level1_img = pygame.transform.scale(level1_img, (200, 80))

level2_img = pygame.image.load("images/LEVEL2.png")
level2_img = pygame.transform.scale(level2_img, (200, 80))

# States
menu_state = "main"  # can be "main", "levels"

def draw_main_menu():
    screen.blit(bg_image, (0, 0))
    title = font.render("Water Sort Puzzle", True, 'white')
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 80))

    rules = [
        "Rules:",
        "- Pour water of the same color together.",
        "- You can only pour on same color or empty tube.",
        "- Solve by sorting all tubes with 1 color."
    ]
    for i, rule in enumerate(rules):
        rule_text = small_font.render(rule, True, 'white')
        screen.blit(rule_text, (40, 150 + i * 25))

    play_button = pygame.draw.rect(screen, 'green', (170, 300, 160, 50), border_radius=10)
    play_text = small_font.render("Play", True, 'white')
    screen.blit(play_text, (play_button.x + 55, play_button.y + 15))
    return play_button

def draw_level_menu():
    screen.blit(bg_image, (0, 0))
    title = font.render("Choose Level", True, 'white')
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 60))

    level1_btn = screen.blit(level1_img, (150, 180))
    level2_btn = screen.blit(level2_img, (150, 300))

    return level1_btn, level2_btn

def launch_game(filename):
    if getattr(sys, 'frozen', False):
        script_path = os.path.join(os.path.dirname(sys.executable), filename)
    else:
        script_path = filename
    subprocess.Popen([sys.executable, script_path])

run = True
while run:
    timer.tick(fps)
    screen.blit(bg_image, (0, 0))

    if menu_state == "main":
        play_btn = draw_main_menu()
    elif menu_state == "levels":
        level1_btn, level2_btn = draw_level_menu()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if menu_state == "main":
                if play_btn.collidepoint(event.pos):
                    menu_state = "levels"
            elif menu_state == "levels":
                if level1_btn.collidepoint(event.pos):
                    launch_game("watersort1.py")
                elif level2_btn.collidepoint(event.pos):
                    launch_game("watersort2.py")

    pygame.display.flip()

pygame.quit()
