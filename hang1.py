import pygame
import random
import string
import sys

# Initialize Pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 500
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman Game")

# Fonts
LETTER_FONT = pygame.font.SysFont('comicsans', 40)
WORD_FONT = pygame.font.SysFont('comicsans', 60)
TITLE_FONT = pygame.font.SysFont('comicsans', 70)

# Load hangman images (make sure you have hangman0.png to hangman6.png)
images = []
for i in range(7):
    image = pygame.image.load(f"hangman{i}.png")
    images.append(image)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Button variables
RADIUS = 20
GAP = 15
startx = round((WIDTH - (RADIUS * 2 + GAP) * 13) / 2)
starty = 400

# Load words from file
with open("word.txt", "r") as file:
    words = [line.strip().upper() for line in file if line.strip()]

# Game variables
FPS = 60
clock = pygame.time.Clock()


def reset_game():
    global hangman_status, word, guessed, letters
    hangman_status = 0
    word = random.choice(words)
    guessed = []
    letters = []
    A = 65
    for i in range(26):
        x = startx + GAP * 2 + ((RADIUS * 2 + GAP) * (i % 13))
        y = starty + ((i // 13) * (GAP + RADIUS * 2))
        letters.append([x, y, chr(A + i), True])


def draw():
    win.fill(WHITE)

    # Draw title
    text = TITLE_FONT.render("HANGMAN", 1, BLACK)
    win.blit(text, (WIDTH / 2 - text.get_width() / 2, 20))

    # Draw word
    display_word = ""
    for letter in word:
        if letter in guessed:
            display_word += letter + " "
        else:
            display_word += "_ "

    text = WORD_FONT.render(display_word, 1, BLACK)
    win.blit(text, (WIDTH / 2 - text.get_width() / 2, 200))

    # Draw letter buttons
    for letter in letters:
        x, y, ltr, visible = letter
        if visible:
            pygame.draw.circle(win, BLACK, (x, y), RADIUS, 3)
            text = LETTER_FONT.render(ltr, 1, BLACK)
            win.blit(text, (x - text.get_width() / 2, y - text.get_height() / 2))

    # Draw hangman image
    win.blit(images[hangman_status], (150, 100))
    pygame.display.update()


def display_message(message):
    win.fill(WHITE)
    text = WORD_FONT.render(message, 1, BLACK)
    win.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(2000)


def end_screen(message):
    display_message(message)

    # Ask to play again
    win.fill(WHITE)
    again_text = LETTER_FONT.render("Play Again? (Y/N)", 1, BLACK)
    win.blit(again_text, (WIDTH / 2 - again_text.get_width() / 2, HEIGHT / 2))
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


# Initialize game
reset_game()

# Main game loop
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

    # Check win
    won = all(letter in guessed for letter in word)
    if won:
        end_screen("You WON!")

    # Check loss
    if hangman_status == 6:
        end_screen(f"You LOST! Word was: {word}")

pygame.quit()
sys.exit()