import pygame
import sys
import subprocess


pygame.init()
pygame.mixer.init() 
WIDTH, HEIGHT = 900, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🧠 Cognitive Horizon")


main_bg = pygame.image.load("images/main.jpg")
main_bg = pygame.transform.scale(main_bg, (WIDTH, HEIGHT))

game_bg = pygame.image.load("images/1.jpg")
game_bg = pygame.transform.scale(game_bg, (WIDTH, HEIGHT))

# Load Button Images (Same size for all)
BUTTON_WIDTH, BUTTON_HEIGHT = 260, 80

play_img = pygame.image.load("images/play.png")
play_img = pygame.transform.scale(play_img, (BUTTON_WIDTH, BUTTON_HEIGHT))

exit_img = pygame.image.load("images/exit.png")
exit_img = pygame.transform.scale(exit_img, (BUTTON_WIDTH, BUTTON_HEIGHT))

quiz_img = pygame.image.load("images/quiz.png")
quiz_img = pygame.transform.scale(quiz_img, (BUTTON_WIDTH, BUTTON_HEIGHT))

sort_img = pygame.image.load("images/sort.png")
sort_img = pygame.transform.scale(sort_img, (BUTTON_WIDTH, BUTTON_HEIGHT))

memory_img = pygame.image.load("images/memory.png")
memory_img = pygame.transform.scale(memory_img, (BUTTON_WIDTH, BUTTON_HEIGHT))

# Button Class
class Button:
    def __init__(self, x, y, width, height, action, image=None):
        self.image = image
        self.rect = pygame.Rect(x, y, width, height)
        self.action = action

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def check_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.action()

# Game Actions
def start_quiz():
    print("🧩 Starting Quiz Game...")
    subprocess.run(["python", "quiz.py"])

def start_water_sort():
    print("🌈 Starting Water Sort Game...")
    subprocess.run(["python", "mainsort.py"])

def start_memory_game():
    print("🧠 Launching Memory Game...")
    subprocess.run(["python", "memory.py"])

def quit_game():
    print("👋 Exiting Cognitive Horizon...")
    pygame.mixer.music.stop()  # Stop the music when quitting
    pygame.quit()
    sys.exit()

# Play Background Music
def play_music():
    pygame.mixer.music.load("music.mp3")  # Load the music file
    pygame.mixer.music.play(-1)  # Play the music in a loop (-1 means infinite loop)

# Game Menu
def game_menu():
    game_buttons = [
        Button(320, 180, BUTTON_WIDTH, BUTTON_HEIGHT, start_quiz, image=quiz_img),
        Button(320, 280, BUTTON_WIDTH, BUTTON_HEIGHT, start_water_sort, image=sort_img),
        Button(320, 380, BUTTON_WIDTH, BUTTON_HEIGHT, start_memory_game, image=memory_img),
    ]

    while True:
        SCREEN.blit(game_bg, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            for button in game_buttons:
                button.check_click(event)

        for button in game_buttons:
            button.draw(SCREEN)

        pygame.display.update()

# Main Menu
def main_menu():
    play_music()  # Start the background music when the main menu is shown
    main_buttons = [
        Button(320, 300, BUTTON_WIDTH, BUTTON_HEIGHT, game_menu, image=play_img),
        Button(320, 400, BUTTON_WIDTH, BUTTON_HEIGHT, quit_game, image=exit_img),
    ]

    while True:
        SCREEN.blit(main_bg, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            for button in main_buttons:
                button.check_click(event)

        for button in main_buttons:
            button.draw(SCREEN)

        pygame.display.update()

# Run
if __name__ == "__main__":
    main_menu()
