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

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Load hangman images
images = []
for i in range(7):
    image = pygame.image.load(f"hangman{i}.png")
    images.append(image)

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

    # Draw title
    title_text = TITLE_FONT.render("HANGMAN", 1, BLACK)
    win.blit(title_text, (WIDTH / 2 - title_text.get_width() / 2, 20))

    # Draw word
    display_word = ""
    for letter in word:
        if letter in guessed:
            display_word += letter + " "
        else:
            display_word += "_ "
    text = WORD_FONT.render(display_word, 1, BLACK)
    win.blit(text, (WIDTH / 2 - text.get_width() / 2, 200))

    # Draw hint
    hint_text = HINT_FONT.render("Hint: " + hint, 1, BLACK)
    win.blit(hint_text, (WIDTH / 2 - hint_text.get_width() / 2, 270))

    # Draw letters
    for letter in letters:
        x, y, ltr, visible = letter
        if visible:
            pygame.draw.circle(win, BLACK, (x, y), RADIUS, 3)
            letter_text = LETTER_FONT.render(ltr, 1, BLACK)
            win.blit(letter_text, (x - letter_text.get_width() / 2, y - letter_text.get_height() / 2))

    # Draw hangman image
    win.blit(images[hangman_status], (100, 100))

    pygame.display.update()


def display_message(message):
    win.fill(WHITE)
    text = WORD_FONT.render(message, 1, BLACK)
    win.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(2000)


def end_screen(message):
    display_message(message)

    again_text = LETTER_FONT.render("Play Again? (Y/N)", 1, BLACK)
    win.blit(again_text, (WIDTH / 2 - again_text.get_width() / 2, HEIGHT / 2 + 60))
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    reset_game()
                    waiting = False
                elif event.key == pygame.K_n:
                    pygame.quit()
                    sys.exit()


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
        end_screen("You WON!")

    # Lose condition
    if hangman_status == 6:
        end_screen(f"You LOST! Word was: {word}")

pygame.quit()
