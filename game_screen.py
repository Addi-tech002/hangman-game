"""
import pygame
import random
import sys
from utils import scale_font, load_word_and_hint, draw_button

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)

# Constants
RADIUS = 30
GAP = 25
MAX_ROUNDS = 10

def game_screen(win, WIDTH, HEIGHT, difficulty, challenge_mode=False):
    # Get max screen size dynamically
    screen_info = pygame.display.Info()
    WIDTH, HEIGHT = screen_info.current_w, screen_info.current_h
    win = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

    # Adjust rounds based on difficulty
    if difficulty == 'easy':
        max_rounds = 10
    elif difficulty == 'medium':
        max_rounds = 8
    else:
        max_rounds = 5

    images = [pygame.image.load(f"hangman{i}.png") for i in range(7)]
    clock = pygame.time.Clock()
    FPS = 60
    guessed = []
    hangman_status = 0
    score = {'wins': 0, 'losses': 0}
    rounds_played = 0

    word = ""
    hint = ""
    letters = []
    button_rect = pygame.Rect(0, 0, 0, 0)
    start_time = pygame.time.get_ticks()  # Challenge timer

    def reset_round():
        nonlocal guessed, hangman_status, letters, word, hint, button_rect
        guessed = []
        hangman_status = 0
        word, hint = load_word_and_hint(difficulty)  # Use difficulty
        letters = []
        A = 65
        startx = round((WIDTH - (RADIUS * 2 + GAP) * 13) / 2)
        starty = HEIGHT - 170
        for i in range(26):
            x = startx + GAP * 2 + ((RADIUS * 2 + GAP) * (i % 13))
            y = starty + ((i // 13) * (GAP + RADIUS * 2))
            letters.append([x, y, chr(A + i), True])
        button_rect = pygame.Rect(WIDTH - 250, 20, 220, 50)

    def draw():
        win.fill(WHITE)
        LETTER_FONT = scale_font(45, WIDTH)
        WORD_FONT = scale_font(80, WIDTH)
        TITLE_FONT = scale_font(90, WIDTH)
        HINT_FONT = scale_font(35, WIDTH)
        SCORE_FONT = scale_font(30, WIDTH)
        BUTTON_FONT = scale_font(30, WIDTH)

        title = TITLE_FONT.render("HANGMAN", True, BLACK)
        win.blit(title, (WIDTH / 2 - title.get_width() / 2, 30))

        display_word = " ".join([letter if letter in guessed else "_" for letter in word])
        word_text = WORD_FONT.render(display_word, True, BLACK)
        win.blit(word_text, (WIDTH / 2 - word_text.get_width() / 2, 160))

        hint_text = HINT_FONT.render("Hint: " + hint, True, BLACK)
        win.blit(hint_text, (WIDTH / 2 - hint_text.get_width() / 2, 260))

        score_text = SCORE_FONT.render(
            f"Wins: {score['wins']} | Losses: {score['losses']} | Round: {rounds_played}/{max_rounds}",
            True, BLACK)
        win.blit(score_text, (20, 20))

        # Button Drawing (Updated)
        draw_button("Show Answer", WIDTH - 240, 20, 200, 50, win, BUTTON_FONT)

        for x, y, ltr, visible in letters:
            if visible:
                pygame.draw.circle(win, BLACK, (x, y), RADIUS, 3)
                txt = LETTER_FONT.render(ltr, True, BLACK)
                win.blit(txt, (x - txt.get_width() / 2, y - txt.get_height() / 2))

        win.blit(images[hangman_status], (100, 350))
        pygame.display.update()

    def display_message(message):
        font = scale_font(70, WIDTH)
        win.fill(WHITE)
        msg = font.render(message, True, BLACK)
        win.blit(msg, (WIDTH / 2 - msg.get_width() / 2, HEIGHT / 2 - msg.get_height() / 2))
        pygame.display.update()
        pygame.time.delay(2000)

    def disable_letter_on_screen(letter, letters):
        for ltr in letters:
            if ltr[2] == letter:
                ltr[3] = False

    reset_round()

    while True:
        clock.tick(FPS)
        WIDTH, HEIGHT = win.get_size()

        # Re-update button_rect
        button_rect.update(WIDTH - 250, 20, 220, 50)
        draw()

        # Challenge Mode Timer Logic (60 seconds)
        if challenge_mode:
            elapsed_time = pygame.time.get_ticks() - start_time
            if elapsed_time > 60000:  # Challenge ends after 60 seconds
                display_message(f"Time's up! You guessed {score['wins']} words correctly!")
                return "start"

        if rounds_played >= max_rounds and not challenge_mode:
            display_message(f"Game Over! Wins: {score['wins']}, Losses: {score['losses']}")
            return "start" 
            

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if button_rect.collidepoint(mx, my):
                    display_message(f"Answer: {word}")
                    score['losses'] += 1
                    rounds_played += 1
                    reset_round()
                else:
                    for letter in letters:
                        x, y, ltr, visible = letter
                        if visible and ((x - mx) ** 2 + (y - my) ** 2) ** 0.5 <= RADIUS:
                            guessed.append(ltr)
                            disable_letter_on_screen(ltr, letters)
                            if ltr not in word:
                                hangman_status += 1
                            break

            elif event.type == pygame.KEYDOWN:
                key = pygame.key.name(event.key).upper()
                if len(key) == 1 and key.isalpha() and key not in guessed:
                    guessed.append(key)
                    disable_letter_on_screen(key, letters)
                    if key not in word:
                        hangman_status += 1

        # Win/Loss Conditions
        if all([ltr in guessed for ltr in word]):
            display_message("You WON!")
            score['wins'] += 1
            rounds_played += 1
            reset_round()
        elif hangman_status >= 6:
            display_message(f"You LOST! Word was: {word}")
            score['losses'] += 1
            rounds_played += 1
            reset_round()

""" 

import pygame
import random
import sys
from utils import scale_font, load_word_and_hint, draw_button
from profile_manager import update_stats

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)

# Constants
RADIUS = 30
GAP = 25

def game_screen(win, WIDTH, HEIGHT, difficulty, username):
    screen_info = pygame.display.Info()
    WIDTH, HEIGHT = screen_info.current_w, screen_info.current_h
    win = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

    # Set rounds based on difficulty
    max_rounds = {'easy': 10, 'medium': 8, 'hard': 5}[difficulty]

    images = [pygame.image.load(f"hangman{i}.png") for i in range(7)]
    clock = pygame.time.Clock()
    FPS = 60
    guessed = []
    hangman_status = 0
    score = {'wins': 0, 'losses': 0}
    rounds_played = 0

    word = ""
    hint = ""
    letters = []
    button_rect = pygame.Rect(0, 0, 0, 0)

    def reset_round():
        nonlocal guessed, hangman_status, letters, word, hint, button_rect
        guessed = []
        hangman_status = 0
        word, hint = load_word_and_hint(difficulty)
        letters = []
        A = 65
        startx = round((WIDTH - (RADIUS * 2 + GAP) * 13) / 2)
        starty = HEIGHT - 170
        for i in range(26):
            x = startx + GAP * 2 + ((RADIUS * 2 + GAP) * (i % 13))
            y = starty + ((i // 13) * (GAP + RADIUS * 2))
            letters.append([x, y, chr(A + i), True])
        button_rect = pygame.Rect(WIDTH - 250, 20, 220, 50)

    def draw():
        win.fill(WHITE)
        LETTER_FONT = scale_font(45, WIDTH)
        WORD_FONT = scale_font(80, WIDTH)
        TITLE_FONT = scale_font(90, WIDTH)
        HINT_FONT = scale_font(35, WIDTH)
        SCORE_FONT = scale_font(30, WIDTH)
        BUTTON_FONT = scale_font(30, WIDTH)

        title = TITLE_FONT.render("HANGMAN", True, BLACK)
        win.blit(title, (WIDTH / 2 - title.get_width() / 2, 30))

        display_word = " ".join([letter if letter in guessed else "_" for letter in word])
        word_text = WORD_FONT.render(display_word, True, BLACK)
        win.blit(word_text, (WIDTH / 2 - word_text.get_width() / 2, 160))

        hint_text = HINT_FONT.render("Hint: " + hint, True, BLACK)
        win.blit(hint_text, (WIDTH / 2 - hint_text.get_width() / 2, 360))
        #Dynamically scale hint font to fit screen


        score_text = SCORE_FONT.render(
            f"Wins: {score['wins']} | Losses: {score['losses']} | Round: {rounds_played}/{max_rounds}",
            True, BLACK)
        win.blit(score_text, (20, 20))

        draw_button("Show Answer", WIDTH - 240, 20, 200, 50, win, BUTTON_FONT)

        for x, y, ltr, visible in letters:
            if visible:
                pygame.draw.circle(win, BLACK, (x, y), RADIUS, 3)
                txt = LETTER_FONT.render(ltr, True, BLACK)
                win.blit(txt, (x - txt.get_width() / 2, y - txt.get_height() / 2))

        win.blit(images[hangman_status], (100, 350))
        pygame.display.update()

    def display_message(message):
        font = scale_font(70, WIDTH)
        win.fill(WHITE)
        msg = font.render(message, True, BLACK)
        win.blit(msg, (WIDTH / 2 - msg.get_width() / 2, HEIGHT / 2 - msg.get_height() / 2))
        pygame.display.update()
        pygame.time.delay(2000)

    def disable_letter_on_screen(letter, letters):
        for ltr in letters:
            if ltr[2] == letter:
                ltr[3] = False

    reset_round()

    while True:
        clock.tick(FPS)
        WIDTH, HEIGHT = win.get_size()
        button_rect.update(WIDTH - 250, 20, 220, 50)
        draw()

        if rounds_played >= max_rounds:
            display_message(f"Game Over! Wins: {score['wins']}, Losses: {score['losses']}")
            return "start"

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if button_rect.collidepoint(mx, my):
                    display_message(f"Answer: {word}")
                    score['losses'] += 1
                    rounds_played += 1
                    update_stats(username, win=False, challenge=False, score=0)
                    reset_round()
                else:
                    for letter in letters:
                        x, y, ltr, visible = letter
                        if visible and ((x - mx) ** 2 + (y - my) ** 2) ** 0.5 <= RADIUS:
                            guessed.append(ltr)
                            disable_letter_on_screen(ltr, letters)
                            if ltr not in word:
                                hangman_status += 1
                            break

            elif event.type == pygame.KEYDOWN:
                key = pygame.key.name(event.key).upper()
                if len(key) == 1 and key.isalpha() and key not in guessed:
                    guessed.append(key)
                    disable_letter_on_screen(key, letters)
                    if key not in word:
                        hangman_status += 1

        if all([ltr in guessed for ltr in word]):
            display_message("You WON!")
            score['wins'] += 1
            rounds_played += 1
            update_stats(username, win=True, challenge=False, score=1)
            reset_round()
        elif hangman_status >= 6:
            display_message(f"You LOST! Word was: {word}")
            score['losses'] += 1
            rounds_played += 1
            update_stats(username, win=False, challenge=False, score=0)
            reset_round()
