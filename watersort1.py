import copy
import random
import pygame
from datetime import datetime
from fpdf import FPDF
from collections import deque
import smtplib
from email.message import EmailMessage
import os


# initialize pygame
pygame.init()

# initialize game variables
WIDTH = 500
HEIGHT = 550
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Water Sort PyGame')
font = pygame.font.Font('freesansbold.ttf', 24)
small_font = pygame.font.Font('freesansbold.ttf', 18)
large_font = pygame.font.Font('freesansbold.ttf', 30)
fps = 60
timer = pygame.time.Clock()
color_choices = ['red', 'orange', 'light blue', 'dark blue', 'dark green', 'pink', 'purple', 'dark gray']
tube_colors = []
initial_colors = []
tubes = 6
new_game = True
selected = False
tube_rects = []
select_rect = 100
win = False
move_count = 0
final_result_text = ""
start_ticks = pygame.time.get_ticks()
best_possible = 0

background_image = pygame.image.load("images/sortback.webp")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
timer_icon = pygame.image.load("images/timer.png")
timer_icon = pygame.transform.scale(timer_icon, (30, 30))


def generate_start():
    tubes_number = tubes
    tubes_colors = []
    available_colors = []
    for i in range(tubes_number):
        tubes_colors.append([])
        if i < tubes_number - 2:
            for j in range(4):
                available_colors.append(i)
    for i in range(tubes_number - 2):
        for j in range(4):
            color = random.choice(available_colors)
            tubes_colors[i].append(color)
            available_colors.remove(color)
    return tubes_number, tubes_colors


def draw_tubes(tubes_num, tube_cols):
    tube_boxes = []
    spacing_x = WIDTH // (tubes_num // 2 + 1)
    top_y = 100
    bottom_y = 320

    for i in range(tubes_num // 2):
        x = (i + 1) * spacing_x - 32
        for j in range(len(tube_cols[i])):
            pygame.draw.rect(screen, color_choices[tube_cols[i][j]], [x, top_y + 150 - (50 * j), 65, 50], 0, 3)
        box = pygame.draw.rect(screen, 'blue', [x, top_y, 65, 200], 5, 5)
        if select_rect == i:
            pygame.draw.rect(screen, 'green', [x, top_y, 65, 200], 3, 5)
        tube_boxes.append(box)

    for i in range(tubes_num // 2, tubes_num):
        x = (i - tubes_num // 2 + 1) * spacing_x - 32
        for j in range(len(tube_cols[i])):
            pygame.draw.rect(screen, color_choices[tube_cols[i][j]], [x, bottom_y + 150 - (50 * j), 65, 50], 0, 3)
        box = pygame.draw.rect(screen, 'blue', [x, bottom_y, 65, 200], 5, 5)
        if select_rect == i:
            pygame.draw.rect(screen, 'green', [x, bottom_y, 65, 200], 3, 5)
        tube_boxes.append(box)

    return tube_boxes


def calc_move(colors, selected_rect, destination):
    global move_count
    chain = True
    color_on_top = 100
    length = 1
    color_to_move = 100
    if len(colors[selected_rect]) > 0:
        color_to_move = colors[selected_rect][-1]
        for i in range(1, len(colors[selected_rect])):
            if chain:
                if colors[selected_rect][-1 - i] == color_to_move:
                    length += 1
                else:
                    chain = False
    if 4 > len(colors[destination]):
        if len(colors[destination]) == 0:
            color_on_top = color_to_move
        else:
            color_on_top = colors[destination][-1]
    if color_on_top == color_to_move:
        moved = False
        for i in range(length):
            if len(colors[destination]) < 4:
                if len(colors[selected_rect]) > 0:
                    colors[destination].append(color_on_top)
                    colors[selected_rect].pop(-1)
                    moved = True
        if moved:
            move_count += 1
    return colors


def check_victory(colors):
    won = True
    for i in range(len(colors)):
        if len(colors[i]) > 0:
            if len(colors[i]) != 4:
                won = False
            else:
                main_color = colors[i][-1]
                for j in range(len(colors[i])):
                    if colors[i][j] != main_color:
                        won = False
    return won
def send_email_report():
    try:
        print("📤 Attempting to send email...")

        # Email details
        sender_email = 'srijanstuti553@gmail.com'
        receiver_email = '22803011@mail.jiit.ac.in'
        app_password = 'sjkl kctb nygl aknq'
        subject = '🧠 Memory Game Report'
        body = 'Hello,\n\nPlease find attached the Memory Game performance report.\n\nRegards,\nStuti'

        # Create the email message
        msg = EmailMessage()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject
        msg.set_content(body)

        # Attach the PDF
        filename = "WaterSort_Report.pdf"
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


def generate_report(move_count, best_possible):
    global final_result_text
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"WaterSort_Report.pdf"

    efficiency = round((best_possible / move_count) * 100, 2) if move_count > 0 else 0
    efficiency = min(efficiency, 100.0)

    if efficiency >= 90:
        tip = "Perfect strategy! Keep it up!"
    elif efficiency >= 70:
        tip = "Great job! Try grouping earlier."
    elif efficiency >= 50:
        tip = "Good effort! Look for same colors."
    else:
        tip = "Try not to split same colors!"

    final_result_text = f"You Won!\nTotal Moves: {move_count}\nBest Case: {best_possible}\nEfficiency: {efficiency}%\nTip: {tip}"

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=14)
    pdf.cell(200, 10, txt="Water Sort Puzzle Report", ln=True, align='C')
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Total Moves: {move_count}", ln=True)
    pdf.cell(200, 10, txt=f"Best Case Moves: {best_possible}", ln=True)
    pdf.cell(200, 10, txt=f"Efficiency: {efficiency}%", ln=True)
    pdf.multi_cell(0, 10, txt=f"Suggestion: {tip}")
    pdf.output(filename)
    send_email_report()


def calculate_min_moves(start_state):
    visited = set()
    queue = deque()
    queue.append((copy.deepcopy(start_state), 0))
    visited.add(str(start_state))

    while queue:
        state, moves = queue.popleft()
        if check_victory(state):
            return moves

        for i in range(len(state)):
            if not state[i]:
                continue
            for j in range(len(state)):
                if i != j:
                    temp_state = copy.deepcopy(state)
                    before = len(temp_state[j])
                    temp_state = calc_move(temp_state, i, j)
                    after = len(temp_state[j])
                    if after > before:
                        state_str = str(temp_state)
                        if state_str not in visited:
                            visited.add(state_str)
                            queue.append((temp_state, moves + 1))
    return 0


run = True
while run:
    screen.blit(background_image, (0, 0))
    timer.tick(fps)

    seconds = (pygame.time.get_ticks() - start_ticks) // 1000
    screen.blit(timer_icon, (10, 10))
    timer_text = small_font.render(f"{seconds}s", True, 'white')
    screen.blit(timer_text, (45, 15))

    exit_button = pygame.draw.rect(screen, 'red', (450, 10, 40, 30), border_radius=5)
    exit_text = small_font.render("Exit", True, 'white')
    screen.blit(exit_text, (455, 15))

    if win:
        if final_result_text == "":
            generate_report(move_count, best_possible)

        screen.blit(background_image, (0, 0))
        y_offset = 180
        for line in final_result_text.split('\n'):
            result_line = font.render(line, True, 'white')
            screen.blit(result_line, (WIDTH // 2 - result_line.get_width() // 2, y_offset))
            y_offset += 35

        restart_text = small_font.render('Space: Restart | Enter: New Board', True, 'white')
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT - 30))
        pygame.display.flip()
        continue

    title = large_font.render("Water Sort Puzzle", True, 'white')
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 40))

    if new_game:
        tubes, tube_colors = generate_start()
        initial_colors = copy.deepcopy(tube_colors)
        best_possible = calculate_min_moves(initial_colors)
        move_count = 0
        new_game = False
        win = False
        final_result_text = ""
        start_ticks = pygame.time.get_ticks()
    else:
        tube_rects = draw_tubes(tubes, tube_colors)
    win = check_victory(tube_colors)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if exit_button.collidepoint(event.pos):
                run = False
            if not selected:
                for item in range(len(tube_rects)):
                    if tube_rects[item].collidepoint(event.pos):
                        selected = True
                        select_rect = item
            else:
                for item in range(len(tube_rects)):
                    if tube_rects[item].collidepoint(event.pos):
                        dest_rect = item
                        tube_colors = calc_move(tube_colors, select_rect, dest_rect)
                        selected = False
                        select_rect = 100
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                tube_colors = copy.deepcopy(initial_colors)
                move_count = 0
                final_result_text = ""
                start_ticks = pygame.time.get_ticks()
            elif event.key == pygame.K_RETURN:
                new_game = True

    restart_text = small_font.render('Space: Restart | Enter: New Board', True, 'white')
    screen.blit(restart_text, (10, HEIGHT - 30))

    pygame.display.flip()

pygame.quit() 