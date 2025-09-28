
"""import pygame #main code 
import random

# Initialize Pygame
pygame.init()

# Initial window size
WIDTH, HEIGHT = 1200, 800
win = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Hangman Game")

# Font scaling function
def scale_font(size):
    return pygame.font.SysFont('comicsans', int(size * WIDTH / 1200))

# Load hangman images
images = [pygame.image.load(f"hangman{i}.png") for i in range(7)]

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)

# Fonts (will scale inside draw loop)
LETTER_FONT = scale_font(45)
WORD_FONT = scale_font(80)
TITLE_FONT = scale_font(90)
HINT_FONT = scale_font(35)
SCORE_FONT = scale_font(30)
BUTTON_FONT = scale_font(30)

# Game variables
RADIUS = 30
GAP = 25
letters = []
hangman_status = 0
guessed = []
word = ""
hint = ""
score = {'wins': 0, 'losses': 0}
rounds_played = 0
max_rounds = 10
button_rect = pygame.Rect(WIDTH - 250, 20, 220, 50)

# Load word and hint from file
def load_word_and_hint():
    global word, hint
    with open("word.txt", "r") as file:
        pairs = [line.strip().split(":") for line in file if ":" in line]
        selected = random.choice(pairs)
        word = selected[0].strip().upper()
        hint = selected[1].strip()

# Reset the game round
def reset_game():
    global guessed, hangman_status, letters
    guessed = []
    hangman_status = 0
    load_word_and_hint()
    letters.clear()
    A = 65
    startx = round((WIDTH - (RADIUS * 2 + GAP) * 13) / 2)
    starty = HEIGHT - 170
    for i in range(26):
        x = startx + GAP * 2 + ((RADIUS * 2 + GAP) * (i % 13))
        y = starty + ((i // 13) * (GAP + RADIUS * 2))
        letters.append([x, y, chr(A + i), True])

# Hide a letter on-screen
def disable_letter_on_screen(letter):
    for l in letters:
        if l[2] == letter:
            l[3] = False
            break

# Draw everything
def draw():
    global LETTER_FONT, WORD_FONT, TITLE_FONT, HINT_FONT, SCORE_FONT, BUTTON_FONT
    LETTER_FONT = scale_font(45)
    WORD_FONT = scale_font(80)
    TITLE_FONT = scale_font(90)
    HINT_FONT = scale_font(35)
    SCORE_FONT = scale_font(30)
    BUTTON_FONT = scale_font(30)

    win.fill(WHITE)

    # Title
    title = TITLE_FONT.render("HANGMAN", 1, BLACK)
    win.blit(title, (WIDTH / 2 - title.get_width() / 2, 30))

    # Word
    display_word = " ".join([letter if letter in guessed else "_" for letter in word])
    word_text = WORD_FONT.render(display_word, 1, BLACK)
    win.blit(word_text, (WIDTH / 2 - word_text.get_width() / 2, 160))

    # Hint
    hint_text = HINT_FONT.render("Hint: " + hint, 1, BLACK)
    win.blit(hint_text, (WIDTH / 2 - hint_text.get_width() / 2, 260))

    # Score
    score_text = SCORE_FONT.render(
        f"Wins: {score['wins']} | Losses: {score['losses']} | Round: {rounds_played}/{max_rounds}", 1, BLACK)
    win.blit(score_text, (20, 20))

    # Show Answer button
    pygame.draw.rect(win, GRAY, button_rect, border_radius=15)
    btn_text = BUTTON_FONT.render("Show Answer", 1, BLACK)
    win.blit(btn_text, (button_rect.x + 15, button_rect.y + 10))

    # Letters
    for letter in letters:
        x, y, ltr, visible = letter
        if visible:
            pygame.draw.circle(win, BLACK, (x, y), RADIUS, 3)
            txt = LETTER_FONT.render(ltr, 1, BLACK)
            win.blit(txt, (x - txt.get_width() / 2, y - txt.get_height() / 2))

    # Hangman image
    win.blit(images[hangman_status], (100, 350))

    pygame.display.update()

# Show win/loss message
def display_message(message):
    win.fill(WHITE)
    msg_text = WORD_FONT.render(message, 1, BLACK)
    win.blit(msg_text, (WIDTH / 2 - msg_text.get_width() / 2, HEIGHT / 2 - msg_text.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(2000)

# Start the game
reset_game()
FPS = 60
clock = pygame.time.Clock()
run = True

while run:
    clock.tick(FPS)
    WIDTH, HEIGHT = win.get_size()
    startx = round((WIDTH - (RADIUS * 2 + GAP) * 13) / 2)
    starty = HEIGHT - 170
    button_rect = pygame.Rect(WIDTH - 250, 20, 220, 50)
    draw()

    if rounds_played >= max_rounds:
        display_message(f"Game Over! Wins: {score['wins']}, Losses: {score['losses']}")
        break

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        # Mouse Click
        if event.type == pygame.MOUSEBUTTONDOWN:
            m_x, m_y = pygame.mouse.get_pos()
            if button_rect.collidepoint(m_x, m_y):
                display_message(f"Answer: {word}")
                score['losses'] += 1
                rounds_played += 1
                reset_game()
                continue
            for letter in letters:
                x, y, ltr, visible = letter
                if visible:
                    dis = ((x - m_x) ** 2 + (y - m_y) ** 2) ** 0.5
                    if dis < RADIUS:
                        guessed.append(ltr)
                        disable_letter_on_screen(ltr)
                        if ltr not in word:
                            hangman_status += 1

        # Keyboard Press
        if event.type == pygame.KEYDOWN:
            key = pygame.key.name(event.key).upper()
            if len(key) == 1 and key.isalpha() and key not in guessed:
                guessed.append(key)
                disable_letter_on_screen(key)
                if key not in word:
                    hangman_status += 1

    # Win condition
    if all(letter in guessed for letter in word):
        display_message("You WON!")
        score['wins'] += 1
        rounds_played += 1
        reset_game()

    # Loss condition
    if hangman_status == 6:
        display_message(f"You LOST! Word was: {word}")
        score['losses'] += 1
        rounds_played += 1
        reset_game()

pygame.quit()"""

"""import pygame
import random
import os

# Initialize Pygame
pygame.init()

# Set up window
WIDTH, HEIGHT = 1200, 800
win = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Hangman Game")

# Load hangman images
images = [pygame.image.load(f"hangman{i}.png") for i in range(7)]

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)

# Game constants
RADIUS = 30
GAP = 25
MAX_ROUNDS = 10

# Game variables
letters = []
hangman_status = 0
guessed = []
word = ""
hint = ""
score = {'wins': 0, 'losses': 0}
rounds_played = 0
button_rect = pygame.Rect(WIDTH - 250, 20, 220, 50)


# Scale font dynamically
def scale_font(size, base_width):
    return pygame.font.SysFont('comicsans', int(size * base_width / 1200))


# Load word and hint
def load_word_and_hint():
    with open("word.txt", "r") as file:
        pairs = [line.strip().split(":") for line in file if ":" in line]
        selected = random.choice(pairs)
        return selected[0].strip().upper(), selected[1].strip()


# Setup game round
def setup_round():
    global guessed, hangman_status, letters, word, hint
    guessed = []
    hangman_status = 0
    word, hint = load_word_and_hint()
    letters.clear()
    startx = round((WIDTH - (RADIUS * 2 + GAP) * 13) / 2)
    starty = HEIGHT - 170
    A = 65
    for i in range(26):
        x = startx + GAP * 2 + ((RADIUS * 2 + GAP) * (i % 13))
        y = starty + ((i // 13) * (GAP + RADIUS * 2))
        letters.append([x, y, chr(A + i), True])


# Disable guessed letter
def disable_letter(ltr):
    for letter in letters:
        if letter[2] == ltr:
            letter[3] = False
            break


# Draw game state
def draw():
    global WIDTH, HEIGHT
    WIDTH, HEIGHT = win.get_size()
    win.fill(WHITE)

    # Fonts
    LETTER_FONT = scale_font(45, WIDTH)
    WORD_FONT = scale_font(80, WIDTH)
    TITLE_FONT = scale_font(90, WIDTH)
    HINT_FONT = scale_font(35, WIDTH)
    SCORE_FONT = scale_font(30, WIDTH)
    BUTTON_FONT = scale_font(30, WIDTH)

    # Draw title
    title = TITLE_FONT.render("HANGMAN", True, BLACK)
    win.blit(title, (WIDTH / 2 - title.get_width() / 2, 30))

    # Word display
    display_word = " ".join([ltr if ltr in guessed else "_" for ltr in word])
    word_surface = WORD_FONT.render(display_word, True, BLACK)
    win.blit(word_surface, (WIDTH / 2 - word_surface.get_width() / 2, 160))

    # Hint
    hint_surface = HINT_FONT.render("Hint: " + hint, True, BLACK)
    win.blit(hint_surface, (WIDTH / 2 - hint_surface.get_width() / 2, 260))

    # Score
    score_surface = SCORE_FONT.render(
        f"Wins: {score['wins']} | Losses: {score['losses']} | Round: {rounds_played}/{MAX_ROUNDS}", True, BLACK)
    win.blit(score_surface, (20, 20))

    # Show Answer button
    global button_rect
    button_rect = pygame.Rect(WIDTH - 250, 20, 220, 50)
    pygame.draw.rect(win, GRAY, button_rect, border_radius=15)
    btn_text = BUTTON_FONT.render("Show Answer", True, BLACK)
    win.blit(btn_text, (button_rect.x + 15, button_rect.y + 10))

    # Letters
    for x, y, ltr, visible in letters:
        if visible:
            pygame.draw.circle(win, BLACK, (x, y), RADIUS, 3)
            txt = LETTER_FONT.render(ltr, True, BLACK)
            win.blit(txt, (x - txt.get_width() / 2, y - txt.get_height() / 2))

    # Hangman image
    win.blit(images[hangman_status], (100, 350))
    pygame.display.update()


# Display result message
def display_message(message):
    global WIDTH, HEIGHT
    win.fill(WHITE)
    font = scale_font(70, WIDTH)
    text = font.render(message, True, BLACK)
    win.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(2000)


# Main game loop
def run_game():
    global guessed, hangman_status, rounds_played, score
    clock = pygame.time.Clock()
    FPS = 60
    setup_round()
    running = True

    while running:
        clock.tick(FPS)
        draw()

        if rounds_played >= MAX_ROUNDS:
            display_message(f"Game Over! Wins: {score['wins']}, Losses: {score['losses']}")
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()

                if button_rect.collidepoint(mx, my):
                    display_message(f"Answer: {word}")
                    score['losses'] += 1
                    rounds_played += 1
                    setup_round()
                    continue

                for ltr in letters:
                    x, y, ch, visible = ltr
                    if visible and ((x - mx) ** 2 + (y - my) ** 2) ** 0.5 <= RADIUS:
                        guessed.append(ch)
                        disable_letter(ch)
                        if ch not in word:
                            hangman_status += 1

            elif event.type == pygame.KEYDOWN:
                key = pygame.key.name(event.key).upper()
                if len(key) == 1 and key.isalpha() and key not in guessed:
                    guessed.append(key)
                    disable_letter(key)
                    if key not in word:
                        hangman_status += 1

        # Win
        if all(ch in guessed for ch in word):
            display_message("You WON!")
            score['wins'] += 1
            rounds_played += 1
            setup_round()

        # Loss
        elif hangman_status >= 6:
            display_message(f"You LOST! Word was: {word}")
            score['losses'] += 1
            rounds_played += 1
            setup_round()

    pygame.quit()
"""
import pygame
import random
import os
import sys
from start_screen import start_screen
from rules_screen import rules_screen
from game_screen import game_screen

# Initialize Pygame
pygame.init()

# Set up window
WIDTH, HEIGHT = 1200, 800
win = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Hangman Game")

# Load hangman images
images = [pygame.image.load(f"hangman{i}.png") for i in range(7)]

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)

# Game constants
RADIUS = 30
GAP = 25
MAX_ROUNDS = 10

# Game variables
letters = []
hangman_status = 0
guessed = []
word = ""
hint = ""
score = {'wins': 0, 'losses': 0}
rounds_played = 0
button_rect = pygame.Rect(WIDTH - 250, 20, 220, 50)


# Scale font dynamically
def scale_font(size, base_width):
    return pygame.font.SysFont('comicsans', int(size * base_width / 1200))


# Load word and hint
def load_word_and_hint():
    with open("word.txt", "r") as file:
        pairs = [line.strip().split(":") for line in file if ":" in line]
        selected = random.choice(pairs)
        return selected[0].strip().upper(), selected[1].strip()


# Setup game round
def setup_round():
    global guessed, hangman_status, letters, word, hint
    guessed = []
    hangman_status = 0
    word, hint = load_word_and_hint()
    letters.clear()
    startx = round((WIDTH - (RADIUS * 2 + GAP) * 13) / 2)
    starty = HEIGHT - 170
    A = 65
    for i in range(26):
        x = startx + GAP * 2 + ((RADIUS * 2 + GAP) * (i % 13))
        y = starty + ((i // 13) * (GAP + RADIUS * 2))
        letters.append([x, y, chr(A + i), True])


# Disable guessed letter
def disable_letter(ltr):
    for letter in letters:
        if letter[2] == ltr:
            letter[3] = False
            break


# Draw game state
def draw():
    global WIDTH, HEIGHT
    WIDTH, HEIGHT = win.get_size()
    win.fill(WHITE)

    # Fonts
    LETTER_FONT = scale_font(45, WIDTH)
    WORD_FONT = scale_font(80, WIDTH)
    TITLE_FONT = scale_font(90, WIDTH)
    HINT_FONT = scale_font(35, WIDTH)
    SCORE_FONT = scale_font(30, WIDTH)
    BUTTON_FONT = scale_font(30, WIDTH)

    # Draw title
    title = TITLE_FONT.render("HANGMAN", True, BLACK)
    win.blit(title, (WIDTH / 2 - title.get_width() / 2, 30))

    # Word display
    display_word = " ".join([ltr if ltr in guessed else "_" for ltr in word])
    word_surface = WORD_FONT.render(display_word, True, BLACK)
    win.blit(word_surface, (WIDTH / 2 - word_surface.get_width() / 2, 160))

    # Hint
    hint_surface = HINT_FONT.render("Hint: " + hint, True, BLACK)
    win.blit(hint_surface, (WIDTH / 2 - hint_surface.get_width() / 2, 260))

    # Score
    score_surface = SCORE_FONT.render(
        f"Wins: {score['wins']} | Losses: {score['losses']} | Round: {rounds_played}/{MAX_ROUNDS}", True, BLACK)
    win.blit(score_surface, (20, 20))

    # Show Answer button
    global button_rect
    button_rect = pygame.Rect(WIDTH - 250, 20, 220, 50)
    pygame.draw.rect(win, GRAY, button_rect, border_radius=15)
    btn_text = BUTTON_FONT.render("Show Answer", True, BLACK)
    win.blit(btn_text, (button_rect.x + 15, button_rect.y + 10))

    # Letters
    for x, y, ltr, visible in letters:
        if visible:
            pygame.draw.circle(win, BLACK, (x, y), RADIUS, 3)
            txt = LETTER_FONT.render(ltr, True, BLACK)
            win.blit(txt, (x - txt.get_width() / 2, y - txt.get_height() / 2))

    # Hangman image
    win.blit(images[hangman_status], (100, 350))
    pygame.display.update()


# Display result message
def display_message(message):
    global WIDTH, HEIGHT
    win.fill(WHITE)
    font = scale_font(70, WIDTH)
    text = font.render(message, True, BLACK)
    win.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(2000)


# Game screen function for the main game loop
def game_screen():
    global guessed, hangman_status, rounds_played, score
    clock = pygame.time.Clock()
    FPS = 60
    setup_round()
    running = True

    while running:
        clock.tick(FPS)
        draw()

        if rounds_played >= MAX_ROUNDS:
            display_message(f"Game Over! Wins: {score['wins']}, Losses: {score['losses']}")
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()

                if button_rect.collidepoint(mx, my):
                    display_message(f"Answer: {word}")
                    score['losses'] += 1
                    rounds_played += 1
                    setup_round()
                    continue

                for ltr in letters:
                    x, y, ch, visible = ltr
                    if visible and ((x - mx) ** 2 + (y - my) ** 2) ** 0.5 <= RADIUS:
                        guessed.append(ch)
                        disable_letter(ch)
                        if ch not in word:
                            hangman_status += 1

            elif event.type == pygame.KEYDOWN:
                key = pygame.key.name(event.key).upper()
                if len(key) == 1 and key.isalpha() and key not in guessed:
                    guessed.append(key)
                    disable_letter(key)
                    if key not in word:
                        hangman_status += 1

        # Win condition
        if all(ch in guessed for ch in word):
            display_message("You WON!")
            score['wins'] += 1
            rounds_played += 1
            setup_round()

        # Loss condition
        elif hangman_status >= 6:
            display_message(f"You LOST! Word was: {word}")
            score['losses'] += 1
            rounds_played += 1
            setup_round()


# Main loop that manages screens
current_screen = "start"  # Starting screen
while True:
    if current_screen == "start":
        current_screen = start_screen(win, WIDTH, HEIGHT)
    elif current_screen == "rules":
        current_screen = rules_screen(win, WIDTH, HEIGHT)
    elif current_screen == "game":
        game_screen()  # Call the separate game screen function

pygame.quit()
sys.exit()