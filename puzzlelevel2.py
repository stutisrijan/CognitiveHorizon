
import pygame
import random
import sys
import os
import smtplib
from email.message import EmailMessage
import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Initialize Pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pattern Finder")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 40)

# Load assets
background_img = pygame.image.load("images/path.png")
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

timer_icon = pygame.image.load("images/timer.png")
timer_icon = pygame.transform.scale(timer_icon, (30, 30))

coin_icon = pygame.image.load("images/coin.png")
coin_icon = pygame.transform.scale(coin_icon, (30, 30))

exit_icon = pygame.image.load("images/exit.png")
exit_icon = pygame.transform.scale(exit_icon, (30, 30))

# Game settings
score = 0
round_count = 0
MAX_ROUNDS = 15
time_limit = 15
start_ticks = pygame.time.get_ticks()

# Report state
report_generated = False
final_score = 0
final_time = 0

# Colors and shapes
colors = [pygame.Color("red"), pygame.Color("green"), pygame.Color("blue"), pygame.Color("yellow")]
shapes = ["circle", "square", "triangle", "diamond"]
def send_email_report():
    try:
        print("📤 Attempting to send email...")
        sender_email = 'sandeepchoudhary76100@gmail.com'
        receiver_email = '22803021@mail.jiit.ac.in'
        app_password = 'rmyp kazn xopc tiwz'
        subject = 'Report.pdf'
        body = 'Hello,\n\nPlease find attached the performance report.\n\nRegards,\nStuti'

        msg = EmailMessage()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject
        msg.set_content(body)

        filename = 'report.pdf'
        if not os.path.exists(filename):
            print("❌ Report PDF not found.")
            return

        with open(filename, 'rb') as f:
            file_data = f.read()
            file_name = os.path.basename(f.name)
            msg.add_attachment(file_data, maintype='application', subtype='pdf', filename=file_name)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender_email, app_password)
            smtp.send_message(msg)

        print("✅ Email sent successfully!")

    except Exception as e:
        print(f"❌ Error sending email: {e}")

# === Generate PDF Report ===
def generate_pdf_report(score, time_taken):
    filename = "report.pdf"
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(width / 2, height - 100, "Pattern Finder Report")

    c.setFont("Helvetica", 14)
    c.drawString(100, height - 150, f"Date: {timestamp}")
    c.drawString(100, height - 180, f"Score: {score} / {MAX_ROUNDS}")
    c.drawString(100, height - 210, f"Rounds Completed: {MAX_ROUNDS}")
    c.drawString(100, height - 240, f"Time Taken: {time_taken} seconds")

    # Add improvement and playing tips
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, height - 290, "Improvement Tips:")
    c.setFont("Helvetica", 13)
    c.drawString(120, height - 310, "• Try to improve speed by recognizing shape-color combinations faster.")
    c.drawString(120, height - 330, "• Focus on the positions of missing elements to anticipate the pattern.")

    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, height - 370, "Playing Tips:")
    c.setFont("Helvetica", 13)
    c.drawString(120, height - 390, "• Stay calm and observe the grid layout carefully.")
    c.drawString(120, height - 410, "• Use process of elimination for tricky patterns.")

    c.save()
    print(f"✅ PDF report saved as {filename}")
    send_email_report()
# === Draw a shape ===
def draw_shape(shape, color, pos):
    x, y = pos
    if shape == "circle":
        pygame.draw.circle(screen, color, (x, y), 25)
    elif shape == "square":
        pygame.draw.rect(screen, color, pygame.Rect(x - 25, y - 25, 50, 50))
    elif shape == "triangle":
        pygame.draw.polygon(screen, color, [(x, y - 30), (x - 25, y + 25), (x + 25, y + 25)])
    elif shape == "diamond":
        pygame.draw.polygon(screen, color, [(x, y - 30), (x - 25, y), (x, y + 30), (x + 25, y)])

# === Pattern generation ===
def generate_pattern():
    pattern = []
    for _ in range(8):
        shape = random.choice(shapes)
        color = random.choice(colors)
        pattern.append((shape, color))

    missing_index = random.randint(0, 8)
    correct = random.choice([(s, c) for s in shapes for c in colors])

    options = [correct]

    # Add one "near-miss" wrong option
    wrong_shape = correct[0]
    wrong_color = random.choice([c for c in colors if c != correct[1]])
    options.append((wrong_shape, wrong_color))

    # Add more incorrect options
    while len(options) < 4:
        option = random.choice([(s, c) for s in shapes for c in colors])
        if option not in options:
            options.append(option)

    random.shuffle(options)
    return pattern, missing_index, correct, options

# === Draw pattern ===
def draw_pattern(pattern, missing_index):
    x_start, y_start = 150, 100
    pattern_index = 0
    for i in range(9):
        row = i // 3
        col = i % 3
        x = x_start + col * 100
        y = y_start + row * 100

        if i == missing_index:
            pygame.draw.rect(screen, pygame.Color("gray"), (x - 30, y - 30, 60, 60), 2)
        else:
            shape, color = pattern[pattern_index]
            draw_shape(shape, color, (x, y))
            pattern_index += 1

# === Draw options ===
def draw_options(options):
    y = 450
    for idx, (shape, color) in enumerate(options):
        x = 150 + idx * 150
        pygame.draw.rect(screen, pygame.Color("white"), (x - 40, y - 40, 80, 80))
        draw_shape(shape, color, (x, y))
        pygame.draw.rect(screen, pygame.Color("black"), (x - 40, y - 40, 80, 80), 2)

# === Detect selected option ===
def get_selected_option(pos):
    y = 450
    for idx in range(4):
        x = 150 + idx * 150
        rect = pygame.Rect(x - 40, y - 40, 80, 80)
        if rect.collidepoint(pos):
            return idx
    return None

# Generate first pattern
pattern, missing_index, correct_answer, answer_options = generate_pattern()

# === Main game loop ===
running = True
while running:
    screen.blit(background_img, (0, 0))  # Set background

    # Timer logic
    seconds = (pygame.time.get_ticks() - start_ticks) // 1000
    remaining = max(0, time_limit - seconds)

    # Timer UI
    screen.blit(timer_icon, (WIDTH - 160, 20))
    timer_text = font.render(f"{remaining}s", True, pygame.Color("white"))
    screen.blit(timer_text, (WIDTH - 120, 22))

    # Score UI
    screen.blit(coin_icon, (20, 20))
    score_text = font.render(f"{score}", True, pygame.Color("white"))
    screen.blit(score_text, (60, 22))

    # Exit icon UI
    exit_rect = pygame.Rect(WIDTH - 50, 20, 30, 30)
    screen.blit(exit_icon, (WIDTH - 50, 20))

    # Draw elements
    if round_count < MAX_ROUNDS:
        draw_pattern(pattern[:], missing_index)
        draw_options(answer_options)

    # End game after MAX_ROUNDS
    if round_count >= MAX_ROUNDS:
        if not report_generated:
            final_score = score
            final_time = round_count * time_limit
            generate_pdf_report(final_score, final_time)
            report_generated = True

        game_over_text = font.render("🎉 All Rounds Completed!", True, pygame.Color("red"))
        screen.blit(game_over_text, (WIDTH // 2 - 180, HEIGHT // 2 - 60))

        report_line1 = font.render(f"Final Score: {final_score}", True, pygame.Color("white"))
        screen.blit(report_line1, (WIDTH // 2 - 120, HEIGHT // 2))

        report_line2 = font.render(f"Total Time: {final_time}s", True, pygame.Color("white"))
        screen.blit(report_line2, (WIDTH // 2 - 120, HEIGHT // 2 + 40))

        pygame.display.update()
        pygame.time.wait(5000)
        running = False

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if exit_rect.collidepoint(event.pos):
                running = False
            elif remaining > 0 and round_count < MAX_ROUNDS:
                idx = get_selected_option(event.pos)
                if idx is not None:
                    if answer_options[idx] == correct_answer:
                        score += 1
                    round_count += 1
                    pattern, missing_index, correct_answer, answer_options = generate_pattern()
                    start_ticks = pygame.time.get_ticks()

    pygame.display.update()
    clock.tick(30)

pygame.quit()
sys.exit()











