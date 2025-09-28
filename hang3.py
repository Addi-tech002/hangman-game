import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Window setup
WIDTH, HEIGHT = 1000, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman Game")

# Fonts
LETTER_FONT = pygame.font.SysFont('comicsans', 40)
WORD_FONT = pygame.font.SysFont('comicsans', 60)
TITLE_FONT = pygame.font.SysFont('comicsans', 70)
HINT_FONT = pygame.font.SysFont('comicsans', 30)
SCORE_FONT = pygame.font.SysFont('comicsans', 30)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)

# Load hangman images
images = [pygame.image.load(f"hangman{i}.png") for i in range(7)]

# Button variables
RADIUS = 25
GAP = 20
letters = []
startx = round((WIDTH - (RADIUS * 2 + GAP) * 13) / 2)
starty = 450

# Game variables
hangman_status = 0
guessed = []
word = ""
hint = ""
score = {'wins': 0, 'losses': 0}

# Show Answer button
button_rect = pygame.Rect(WIDTH - 200, 20, 160, 40)


def load_word_and_hint():
    global word, hint
    with open("word.txt", "r") as file:
        word_hint_pairs = [line.strip().split(":") for line in file if ":" in line]
        selected = random.choice(word_hint_pairs)
        word = selected[0].strip().upper()
        hint = selected[1].strip()


def reset_game():
    global guessed, hangman_status, letters
    guessed = []
    hangman_status = 0
    load_word_and_hint()
    letters.clear()
    A = 65
    for i in range(26):
        x = startx + GAP * 2 + ((RADIUS * 2 + GAP) * (i % 13))
        y = starty + ((i // 13) * (GAP + RADIUS * 2))
        letters.append([x, y, chr(A + i), True])


def draw():
    win.fill(WHITE)

    # Title
    title_text = TITLE_FONT.render("HANGMAN", 1, BLACK)
    win.blit(title_text, (WIDTH / 2 - title_text.get_width() / 2, 20))

    # Word
    display_word = ""
    for letter in word:
        if letter in guessed:
            display_word += letter + " "
        else:
            display_word += "_ "
    word_text = WORD_FONT.render(display_word, 1, BLACK)
    win.blit(word_text, (WIDTH / 2 - word_text.get_width() / 2, 200))

    # Hint
    hint_text = HINT_FONT.render("Hint: " + hint, 1, BLACK)
    win.blit(hint_text, (WIDTH / 2 - hint_text.get_width() / 2, 270))

    # Score
    score_text = SCORE_FONT.render(f"Wins: {score['wins']} | Losses: {score['losses']}", 1, BLACK)
    win.blit(score_text, (20, 20))

    # Show Answer button
    pygame.draw.rect(win, GRAY, button_rect, border_radius=10)
    button_text = LETTER_FONT.render("Show Answer", 1, BLACK)
    win.blit(button_text, (button_rect.x + 10, button_rect.y + 5))

    # Letters
    for letter in letters:
        x, y, ltr, visible = letter
        if visible:
            pygame.draw.circle(win, BLACK, (x, y), RADIUS, 3)
            letter_text = LETTER_FONT.render(ltr, 1, BLACK)
            win.blit(letter_text, (x - letter_text.get_width() / 2, y - letter_text.get_height() / 2))

    # Hangman Image
    win.blit(images[hangman_status], (100, 100))

    pygame.display.update()


def display_message(message):
    win.fill(WHITE)
    msg_text = WORD_FONT.render(message, 1, BLACK)
    win.blit(msg_text, (WIDTH / 2 - msg_text.get_width() / 2, HEIGHT / 2 - msg_text.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(1500)


# Start game
reset_game()
FPS = 60
clock = pygame.time.Clock()
run = True

while run:
    clock.tick(FPS)
    draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            m_x, m_y = pygame.mouse.get_pos()

            # Check Show Answer button click
            if button_rect.collidepoint(m_x, m_y):
                display_message(f"Answer: {word}")
                score['losses'] += 1
                reset_game()
                continue

            # Check alphabet button click
            for letter in letters:
                x, y, ltr, visible = letter
                if visible:
                    dis = ((x - m_x) ** 2 + (y - m_y) ** 2) ** 0.5
                    if dis < RADIUS:
                        letter[3] = False
                        guessed.append(ltr)
                        if ltr not in word:
                            hangman_status += 1

    # Win condition
    if all(letter in guessed for letter in word):
        display_message("You WON!")
        score['wins'] += 1
        reset_game()

    # Lose condition
    if hangman_status == 6:
        display_message(f"You LOST! Word was: {word}")
        score['losses'] += 1
        reset_game()

pygame.quit()
