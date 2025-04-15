import pygame
import sys
import json
import random
import os
from fpdf import FPDF
import smtplib
from email.message import EmailMessage

pygame.init()
WIDTH, HEIGHT = 900, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🧩 Critical Thinking Quiz")

bg_image = pygame.image.load("images/quiz_bg.jpg")
bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))

QUESTION_FONT = pygame.font.SysFont("Georgia", 28, bold=True)
OPTION_FONT = pygame.font.SysFont("Arial", 24)
INFO_FONT = pygame.font.SysFont("Arial", 26, bold=True)
TIMER_FONT = pygame.font.SysFont("Arial", 24)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CORRECT_GREEN = (0, 180, 0)
WRONG_RED = (200, 0, 0)
BUTTON_COLOR = (0, 0, 0)         
BUTTON_HOVER = (40, 40, 40)      


timer_icon = pygame.image.load("images/timer.png")
timer_icon = pygame.transform.scale(timer_icon, (30, 30))

coin_icon = pygame.image.load("images/coin.png")
coin_icon = pygame.transform.scale(coin_icon, (30, 30))

question_index = 0
score = 0
coins = 0
responses = []
start_time = pygame.time.get_ticks()

with open("questions.json", "r", encoding="utf-8") as f:
    all_questions = json.load(f)
    questions = random.sample(all_questions, 10)

class OptionButton:
    def __init__(self, text, x, y, w, h):
        self.text = text
        self.rect = pygame.Rect(x, y, w, h)
        self.color = BUTTON_COLOR

    def draw(self, surface, is_hover=False):
        color = BUTTON_HOVER if is_hover else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=12)
        text_surf = OPTION_FONT.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

def draw_question(q):
    SCREEN.blit(bg_image, (0, 0))
    question_text = questions[q]["question"]
    wrapped_lines = wrap_text(question_text, QUESTION_FONT, 760)
    line_height = 35
    box_height = len(wrapped_lines) * line_height + 30
    box_rect = pygame.Rect(60, 60, 780, box_height)
    pygame.draw.rect(SCREEN, BUTTON_COLOR, box_rect, border_radius=12)
    for i, line in enumerate(wrapped_lines):
        rendered = QUESTION_FONT.render(f"{line}", True, WHITE)
        SCREEN.blit(rendered, (80, 75 + i * line_height))

def draw_hud():
    global score, coins
    elapsed = (pygame.time.get_ticks() - start_time) // 1000

    # Coin section - top left
    SCREEN.blit(coin_icon, (20, 20))
    coin_text = INFO_FONT.render(f"{coins}", True, WHITE)
    SCREEN.blit(coin_text, (60, 22))

    # Timer section - top right
    timer_text = TIMER_FONT.render(f"{elapsed}s", True, WHITE)
    timer_x = WIDTH - 100
    SCREEN.blit(timer_icon, (timer_x, 20))
    SCREEN.blit(timer_text, (timer_x + 40, 22))



def display_feedback(correct):
    color = CORRECT_GREEN if correct else WRONG_RED
    message = "Correct! +10 Coins" if correct else "Wrong!"
    text = INFO_FONT.render(message, True, WHITE)
    pygame.draw.rect(SCREEN, color, (270, 500, 360, 50), border_radius=12)
    SCREEN.blit(text, (WIDTH // 2 - text.get_width() // 2, 510))
    pygame.display.update()
    pygame.time.wait(1000)

def wrap_text(text, font, max_width):
    words = text.split(' ')
    lines = []
    current_line = ''
    for word in words:
        test_line = current_line + word + ' '
        if font.size(test_line)[0] < max_width:
            current_line = test_line
        else:
            lines.append(current_line.strip())
            current_line = word + ' '
    lines.append(current_line.strip())
    return lines

def generate_report():
    correct_answers = sum(1 for r in responses if r["selected"] == r["correct"])
    total_questions = len(responses)
    accuracy = (correct_answers / total_questions) * 100

    pdf = FPDF()
    pdf.add_page()

    font_folder = os.path.join(os.path.dirname(__file__), "fonts")
    pdf.add_font("DejaVu", "", os.path.join(font_folder, "DejaVuSans.ttf"), uni=True)
    pdf.add_font("DejaVu", "B", os.path.join(font_folder, "DejaVuSans-Bold.ttf"), uni=True)
    pdf.add_font("DejaVu", "I", os.path.join(font_folder, "DejaVuSans-Oblique.ttf"), uni=True)
    pdf.add_font("DejaVu", "BI", os.path.join(font_folder, "DejaVuSans-BoldOblique.ttf"), uni=True)

    pdf.set_font("DejaVu", "B", size=14)
    pdf.cell(200, 10, txt="Critical Thinking Quiz Report", ln=True, align="C")
    pdf.set_font("DejaVu", size=12)
    pdf.ln(5)

    for i, res in enumerate(responses):
        q = questions[i]["question"]
        report_text = f"Q{i+1}: {q}\nSelected: {res['selected']}\nCorrect: {res['correct']}\n"
        pdf.multi_cell(0, 10, txt=report_text)

    pdf.ln(5)
    pdf.cell(200, 10, txt=f"Final Score: {score} | Coins: {coins}", ln=True, align="C")
    pdf.cell(200, 10, txt=f"Accuracy: {accuracy:.2f}%", ln=True, align="C")
    pdf.ln(10)

    pdf.set_font("DejaVu", "I", size=11)
    if accuracy < 60:
        tips = (
            "Tips to Improve:\n"
            "- Think about cause and effect.\n"
            "- Don't rush decisions.\n"
            "- Ask critical questions.\n"
            "- Always double-check info before reacting."
        )
        pdf.multi_cell(0, 10, txt=tips)
    else:
        pdf.cell(0, 10, txt="Great job! Keep practicing to stay sharp!", ln=True)

    filename = os.path.join(os.path.dirname(__file__), "quiz_report.pdf")
    pdf.output(filename)
    print(f"[✔] Report saved as {filename}")
    send_email_report()

def send_email_report():
    try:
        print("📤 Attempting to send email...")
        sender_email = 'srijanstuti553@gmail.com'
        receiver_email = '22803011@mail.jiit.ac.in'
        app_password = 'sjkl kctb nygl aknq'
        subject = '🧠 Memory Game Report'
        body = 'Hello,\n\nPlease find attached the Memory Game performance report.\n\nRegards,\nStuti'

        msg = EmailMessage()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject
        msg.set_content(body)

        filename = "quiz_report.pdf"
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

def main():
    global question_index, score, coins
    running = True
    while running:
        SCREEN.blit(bg_image, (0, 0))

        if question_index >= len(questions):
            final = INFO_FONT.render(f"Final Score: {score} | Coins: {coins}", True, BLACK)
            SCREEN.blit(final, (WIDTH // 2 - final.get_width() // 2, HEIGHT // 2 - 30))
            pygame.display.update()
            pygame.time.wait(3000)
            generate_report()
            running = False
            continue

        draw_question(question_index)
        opts = questions[question_index]["options"]
        buttons = []
        y_pos = 220
        for i, opt in enumerate(opts):
            btn = OptionButton(opt, 250, y_pos + i * 65, 400, 50)
            buttons.append(btn)
            btn.draw(SCREEN)

        # ✅ Draw HUD and live report LAST so they're always visible
        draw_hud()


        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for btn in buttons:
                    if btn.is_clicked(event.pos):
                        selected = btn.text
                        correct_ans = questions[question_index]["answer"]
                        correct = selected == correct_ans
                        responses.append({"selected": selected, "correct": correct_ans})
                        if correct:
                            score += 1
                            coins += 10
                        display_feedback(correct)
                        question_index += 1


if __name__ == "__main__":
    main()
