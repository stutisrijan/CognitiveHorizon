import pygame
import random
import sys
import smtplib
from email.message import EmailMessage
import datetime
import os
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
MAX_ROUNDS = 10
time_limit = 30  # seconds per round
start_ticks = pygame.time.get_ticks()

# Colors and shapes
colors = [pygame.Color("red"), pygame.Color("green"), pygame.Color("blue"), pygame.Color("yellow")]
shapes = ["circle", "square", "triangle", "diamond"]

# === Email Report ===
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

# === PDF Report ===
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
    c.drawString(100, height - 210, f"Total Time: {time_taken} seconds")
    c.drawString(100, height - 240, f"Rounds Completed: {MAX_ROUNDS}")

    c.line(80, height - 260, width - 80, height - 260)

    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, height - 290, "📈 Improvement Tips:")
    c.setFont("Helvetica", 12)
    c.drawString(120, height - 310, "- Focus on shape-color combinations to reduce confusion.")
    c.drawString(120, height - 330, "- Improve timing by rehearsing typical patterns.")
    c.drawString(120, height - 350, "- Analyze mistakes after each round to learn faster.")

    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, height - 380, "🎮 Playing Tips:")
    c.setFont("Helvetica", 12)
    c.drawString(120, height - 400, "- Scan the full pattern grid before answering.")
    c.drawString(120, height - 420, "- Try to visualize the missing element in your mind.")
    c.drawString(120, height - 440, "- Use the entire time if needed—accuracy is more important.")

    c.save()
    print(f"✅ PDF report with tips saved as {filename}")

    # Send email after report is saved
    send_email_report()

# === Draw Shape ===
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

# === Pattern Generation ===
def generate_pattern():
    pattern = []
    for _ in range(8):
        shape = random.choice(shapes)
        color = random.choice(colors)
        pattern.append((shape, color))

    missing_index = random.randint(0, 8)
    correct = random.choice([(s, c) for s in shapes for c in colors])
    options = [correct]
    while len(options) < 4:
        option = random.choice([(s, c) for s in shapes for c in colors])
        if option not in options:
            options.append(option)
    random.shuffle(options)
    return pattern, missing_index, correct, options

# === Draw Pattern ===
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

# === Draw Options ===
def draw_options(options):
    y = 450
    for idx, (shape, color) in enumerate(options):
        x = 150 + idx * 150
        pygame.draw.rect(screen, pygame.Color("white"), (x - 40, y - 40, 80, 80))
        draw_shape(shape, color, (x, y))
        pygame.draw.rect(screen, pygame.Color("black"), (x - 40, y - 40, 80, 80), 2)

# === Get Selected Option ===
def get_selected_option(pos):
    y = 450
    for idx in range(4):
        x = 150 + idx * 150
        rect = pygame.Rect(x - 40, y - 40, 80, 80)
        if rect.collidepoint(pos):
            return idx
    return None

# === Report Screen ===
def show_report_screen(score, total_time):
    showing = True
    while showing:
        screen.blit(background_img, (0, 0))

        report_title = font.render("🎯 Game Report", True, pygame.Color("red"))
        final_score_text = font.render(f"Final Score: {score} / {MAX_ROUNDS}", True, pygame.Color("white"))
        total_time_text = font.render(f"Total Time: {total_time}s", True, pygame.Color("white"))
        check_pdf_text = font.render("📄 PDF report saved as 'report.pdf'", True, pygame.Color("yellow"))
        exit_note_text = font.render("❌ Press any key or close to exit.", True, pygame.Color("green"))

        screen.blit(report_title, (WIDTH // 2 - 100, 120))
        screen.blit(final_score_text, (WIDTH // 2 - 150, 200))
        screen.blit(total_time_text, (WIDTH // 2 - 150, 250))
        screen.blit(check_pdf_text, (WIDTH // 2 - 220, 300))
        screen.blit(exit_note_text, (WIDTH // 2 - 220, 360))

        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                showing = False

        pygame.display.update()
        clock.tick(30)

# === Initial pattern
pattern, missing_index, correct_answer, answer_options = generate_pattern()

# === Main game loop ===
running = True
final_score = 0
final_time = 0

while running:
    screen.blit(background_img, (0, 0))

    seconds = (pygame.time.get_ticks() - start_ticks) // 1000
    remaining = max(0, time_limit - seconds)

    screen.blit(timer_icon, (WIDTH - 160, 20))
    screen.blit(font.render(f"{remaining}s", True, pygame.Color("white")), (WIDTH - 120, 22))

    screen.blit(coin_icon, (20, 20))
    screen.blit(font.render(f"{score}", True, pygame.Color("white")), (60, 22))

    exit_rect = pygame.Rect(WIDTH - 50, 20, 30, 30)
    screen.blit(exit_icon, (WIDTH - 50, 20))

    draw_pattern(pattern[:], missing_index)
    draw_options(answer_options)

    if round_count >= MAX_ROUNDS:
        final_score = score
        final_time = round_count * time_limit
        generate_pdf_report(final_score, final_time)
        break  # Exit game loop to show report screen

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if exit_rect.collidepoint(event.pos):
                running = False
            elif remaining > 0:
                idx = get_selected_option(event.pos)
                if idx is not None:
                    round_count += 1
                    if answer_options[idx] == correct_answer:
                        score += 1
                    pattern, missing_index, correct_answer, answer_options = generate_pattern()
                    start_ticks = pygame.time.get_ticks()

    pygame.display.update()
    clock.tick(30)

# === Show final report screen
show_report_screen(final_score, final_time)

pygame.quit()
sys.exit()






