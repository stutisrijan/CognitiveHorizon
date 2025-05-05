import pygame
import random
import time
import sys
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import smtplib
from email.message import EmailMessage

pygame.init()

# Window settings
WIDTH, HEIGHT = 600, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Memory Matching Game - Images")

# Fonts
main_font = pygame.font.Font(None, 36)
title_font = pygame.font.Font(pygame.font.match_font('comicsansms'), 28)
bottom_font = pygame.font.SysFont("papyrus", 28)
big_font = pygame.font.Font(None, 74)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Card settings
CARD_SIZE = 100
MARGIN = 20

# Load images
background = pygame.image.load("images/memoryback.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

backcard_img = pygame.image.load("images/backcard.jpg")
backcard_img = pygame.transform.scale(backcard_img, (CARD_SIZE, CARD_SIZE))

timer_icon = pygame.image.load("images/timer.png")
timer_icon = pygame.transform.scale(timer_icon, (40, 40))

import smtplib
from email.message import EmailMessage
import os

def send_email_report():
    try:
        print("📤 Attempting to send email...")

        # Email details
        sender_email = os.getenv('EMAIL_USER')
        app_password = os.getenv('EMAIL_PASS')
        receiver_email = '22803011@mail.jiit.ac.in'
        subject = '🧠 Memory Game Report'
        body = 'Hello,\n\nPlease find attached the Memory Game performance report.\n\nRegards,\nStuti'

        # Create the email message
        msg = EmailMessage()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject
        msg.set_content(body)

        # Attach the PDF
        filename = 'Memory_Game_Report.pdf'
        if not os.path.exists(filename):
            print("❌ Report PDF not found.")
            return

        with open(filename, 'rb') as f:
            file_data = f.read()
            file_name = os.path.basename(f.name)
            msg.add_attachment(file_data, maintype='application', subtype='pdf', filename=file_name)

        # Send the email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender_email, app_password)
            smtp.send_message(msg)

        print("✅ Email sent successfully!")

    except Exception as e:
        print(f"❌ Error sending email: {e}")


# Load image tiles (img1.jpg/jpeg to img8.jpg/jpeg)
def load_tile_images():
    image_tiles = []
    for i in range(1, 9):
        for ext in ['jpg', 'jpeg']:
            path = f"images/img{i}.{ext}"
            if os.path.exists(path):
                img = pygame.image.load(path)
                img = pygame.transform.scale(img, (CARD_SIZE, CARD_SIZE))
                image_tiles.append(img)
                break
    return image_tiles

tile_images = load_tile_images()

# PDF report function
def generate_pdf_report(attempts, matches, total_time):
    accuracy = (matches / attempts) * 100 if attempts > 0 else 0
    file_name = "Memory_Game_Report.pdf"

    c = canvas.Canvas(file_name, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 20)
    c.drawString(50, height - 50, "🧠 Memory Matching Game - Performance Report")

    c.setFont("Helvetica", 14)
    c.drawString(50, height - 100, f"🕒 Time Taken: {total_time} seconds")
    c.drawString(50, height - 130, f"🎯 Attempts Made: {attempts}")
    c.drawString(50, height - 160, f"✅ Matches Found: {matches}")
    c.drawString(50, height - 190, f"📊 Accuracy: {accuracy:.2f}%")

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 230, "📝 Memory Review:")

    c.setFont("Helvetica", 12)
    if accuracy >= 80:
        feedback = "Excellent memory! Keep up the good work."
    elif accuracy >= 60:
        feedback = "Good memory. Try to improve your focus and observation."
    else:
        feedback = "Keep practicing! Try to remember tile positions more actively."

    c.drawString(60, height - 260, feedback)

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 300, "💡 Tips to Improve Memory:")

    tips = [
        "- Use visualization to remember card positions.",
        "- Try chunking patterns into smaller groups.",
        "- Practice daily with small memory games.",
        "- Take short breaks during longer sessions.",
        "- Stay hydrated and sleep well!"
    ]

    y = height - 330
    for tip in tips:
        c.setFont("Helvetica", 12)
        c.drawString(60, y, tip)
        y -= 20

    c.save()
    send_email_report()


    


# Card positions
def create_card_positions():
    positions = []
    grid_width = 4 * CARD_SIZE + 3 * MARGIN
    grid_height = 4 * CARD_SIZE + 3 * MARGIN
    x_offset = (WIDTH - grid_width) // 2
    y_offset = 100
    for i in range(4):
        for j in range(4):
            x = x_offset + j * (CARD_SIZE + MARGIN)
            y = y_offset + i * (CARD_SIZE + MARGIN)
            positions.append((x, y))
    return positions

positions = create_card_positions()

# Create shuffled pairs
def generate_pairs():
    symbols = list(range(8)) * 2
    random.shuffle(symbols)
    return symbols

pairs = generate_pairs()

# Card class
class Card:
    def __init__(self, symbol, position):
        self.symbol = symbol
        self.position = position
        self.rect = pygame.Rect(position[0], position[1], CARD_SIZE, CARD_SIZE)
        self.revealed = False
        self.matched = False

    def draw(self, surface):
        if self.revealed or self.matched:
            surface.blit(tile_images[self.symbol], self.rect)
        else:
            surface.blit(backcard_img, self.rect)

cards = [Card(pairs[i], positions[i]) for i in range(16)]

first_card = None
second_card = None
matches = 0
attempts = 0
clock = pygame.time.Clock()
running = True

# Memorize phase
memorize_time = 30
start_time = time.time()

for card in cards:
    card.revealed = True

while time.time() - start_time < memorize_time:
    screen.blit(background, (0, 0))
    for card in cards:
        card.draw(screen)

    screen.blit(timer_icon, (10, 10))
    remaining = int(memorize_time - (time.time() - start_time))
    timer_text = main_font.render(f"{remaining}s", True, WHITE)
    screen.blit(timer_text, (60, 18))

    exit_text = main_font.render("Exit", True, WHITE)
    screen.blit(exit_text, (WIDTH - 70, 15))

    reminder_text = bottom_font.render("Remember the Tiles", True, WHITE)
    screen.blit(reminder_text, reminder_text.get_rect(center=(WIDTH // 2, HEIGHT - 30)))

    pygame.display.flip()

for card in cards:
    card.revealed = False

game_start_time = time.time()

while running:
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            total_time = int(time.time() - game_start_time)
            generate_pdf_report(attempts, matches, total_time)
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos

            if WIDTH - 80 <= mx <= WIDTH - 10 and 10 <= my <= 40:
                total_time = int(time.time() - game_start_time)
                generate_pdf_report(attempts, matches, total_time)
                pygame.quit()
                sys.exit()

            for card in cards:
                if card.rect.collidepoint(event.pos) and not card.revealed and not card.matched:
                    card.revealed = True
                    if first_card is None:
                        first_card = card
                    elif second_card is None:
                        second_card = card
                        attempts += 1

    if first_card and second_card:
        pygame.time.delay(500)
        if first_card.symbol == second_card.symbol:
            first_card.matched = True
            second_card.matched = True
            matches += 1
        else:
            first_card.revealed = False
            second_card.revealed = False
        first_card = None
        second_card = None

    for card in cards:
        card.draw(screen)

    screen.blit(timer_icon, (10, 10))
    elapsed = int(time.time() - game_start_time)
    timer_text = main_font.render(f"{elapsed}s", True, WHITE)
    screen.blit(timer_text, (60, 18))

    exit_text = main_font.render("Exit", True, WHITE)
    screen.blit(exit_text, (WIDTH - 70, 15))

    match_text = main_font.render(f"Matches: {matches}  Attempts: {attempts}", True, WHITE)
    screen.blit(match_text, (20, HEIGHT - 70))

    reminder_text = bottom_font.render("Remember the Tiles", True, WHITE)
    screen.blit(reminder_text, reminder_text.get_rect(center=(WIDTH // 2, HEIGHT - 30)))

    if matches == 8:
        total_time = int(time.time() - game_start_time)
        generate_pdf_report(attempts, matches, total_time)

        accuracy = (matches / attempts) * 100 if attempts > 0 else 0
        feedback = ""
        if accuracy >= 80:
            feedback = "Excellent memory! Keep it up!"
        elif accuracy >= 60:
            feedback = "Good! Try to improve focus."
        else:
            feedback = "Practice more. You can do it!"

        screen.fill(BLACK)
        win_text = big_font.render("You Win!", True, RED)
        screen.blit(win_text, win_text.get_rect(center=(WIDTH // 2, 100)))

        summary_lines = [
            f"Time Taken: {total_time} sec",
            f"Attempts: {attempts}",
            f"Matches: {matches}",
            f"Accuracy: {accuracy:.2f}%",
            f"Memory Tip: {feedback}"
        ]

        for idx, line in enumerate(summary_lines):
            summary = main_font.render(line, True, WHITE)
            screen.blit(summary, (50, 200 + idx * 50))

        pygame.display.flip()
        pygame.time.delay(6000)
        running = False

    pygame.display.flip()
    clock.tick(30)

pygame.quit()