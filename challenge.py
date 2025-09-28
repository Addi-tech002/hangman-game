"""
import time
import pygame
import random
from utils import scale_font, draw_button

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def challenge_mode(win, WIDTH, HEIGHT, difficulty="easy"):
    clock = pygame.time.Clock()
    FPS = 60
    start_time = time.time()
    duration = 60  # 60 seconds challenge
    wins = 0
    round_num = 0
    MAX_ROUNDS = 5  # Limit the number of rounds

    # Load fonts dynamically
    LETTER_FONT = scale_font(60, WIDTH)
    INFO_FONT = scale_font(30, WIDTH)
    BIG_FONT = scale_font(70, WIDTH)
    BUTTON_FONT = scale_font(30, WIDTH)

    word_list = []
    try:
        with open("word.txt", "r") as f:
            for line in f:
                if line.startswith(f"{difficulty}:"):
                    _, content = line.split(":", 1)
                    word, hint = content.strip().split(" - ", 1)
                    word_list.append((word.strip().lower(), hint.strip()))
    except:
        print("Error loading word.txt")
        return

    if not word_list:
        return

    def render_text_centered(text, font, y):
        rendered = font.render(text, True, BLACK)
        win.blit(rendered, (WIDTH // 2 - rendered.get_width() // 2, y))

    def end_screen(message):
        while True:
            win.fill(WHITE)
            render_text_centered(message, BIG_FONT, HEIGHT // 2 - 80)
            render_text_centered(f"✅ Total correct guesses: {wins}", LETTER_FONT, HEIGHT // 2)
            button_rect = draw_button("Back to Menu", WIDTH // 2 - 100, HEIGHT // 2 + 100, 200, 60, win, BUTTON_FONT)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if button_rect.collidepoint(pygame.mouse.get_pos()):
                        return "start"  # Go back to start screen

    while round_num < MAX_ROUNDS:
        clock.tick(FPS)
        elapsed = time.time() - start_time
        time_left = int(duration - elapsed)

        if elapsed >= duration:
            return end_screen("⏰ Time's Up!")

        word, hint = random.choice(word_list)
        guessed = ""
        input_active = True

        while input_active:
            clock.tick(FPS)
            elapsed = time.time() - start_time
            time_left = int(duration - elapsed)
            if elapsed >= duration:
                return end_screen("⏰ Time's Up!")

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        input_active = False
                    elif event.key == pygame.K_BACKSPACE:
                        guessed = guessed[:-1]
                    elif event.unicode.isalpha():
                        guessed += event.unicode.lower()

            win.fill(WHITE)
            render_text_centered(f"🎯 Challenge Mode ({difficulty.capitalize()})", INFO_FONT, 30)
            render_text_centered(f"Round {round_num + 1}/{MAX_ROUNDS}", INFO_FONT, 80)
            render_text_centered(f"Hint: {hint}", INFO_FONT, 150)
            render_text_centered(f"Word: {'_ ' * len(word)}", LETTER_FONT, 220)
            render_text_centered(f"Your Guess: {guessed}", LETTER_FONT, 300)
            render_text_centered(f"Time Left: {time_left}s", INFO_FONT, 370)
            render_text_centered(f"Score: {wins}", INFO_FONT, 420)
            pygame.display.update()

        if guessed == word:
            wins += 1
            feedback = "✅ Correct!"
        else:
            feedback = f"❌ Wrong! Word was: {word}"

        win.fill(WHITE)
        render_text_centered(feedback, LETTER_FONT, HEIGHT // 2)
        pygame.display.update()
        pygame.time.delay(1500)
        round_num += 1

    return end_screen("🎉 All Rounds Completed!")
"""
import time
import pygame
import random
from utils import scale_font, draw_button

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def challenge_mode(win, WIDTH, HEIGHT, difficulty="easy"):
    clock = pygame.time.Clock()
    FPS = 60
    start_time = time.time()
    duration = 60
    wins = 0
    round_num = 0
    MAX_ROUNDS = 5

    # Load fonts
    LETTER_FONT = scale_font(60, WIDTH)
    INFO_FONT = scale_font(30, WIDTH)
    BIG_FONT = scale_font(70, WIDTH)
    BUTTON_FONT = scale_font(30, WIDTH)

    # Load and prepare background
    try:
        bg_img = pygame.image.load("bghang.jpg")
    except:
        print("Couldn't load background image.")
        bg_img = pygame.Surface((WIDTH, HEIGHT))
        bg_img.fill(WHITE)

    word_list = []
    try:
        with open("word.txt", "r") as f:
            for line in f:
                if line.startswith(f"{difficulty}:"):
                    _, content = line.split(":", 1)
                    word, hint = content.strip().split(" - ", 1)
                    word_list.append((word.strip().lower(), hint.strip()))
    except:
        print("Error loading word.txt")
        return

    if not word_list:
        return

    def render_text_centered(text, font, y):
        rendered = font.render(text, True, BLACK)
        win.blit(rendered, (WIDTH // 2 - rendered.get_width() // 2, y))

    def end_screen(message):
        while True:
            win.blit(pygame.transform.scale(bg_img, (WIDTH, HEIGHT)), (0, 0))
            render_text_centered(message, BIG_FONT, HEIGHT // 2 - 80)
            render_text_centered(f"✅ Total correct guesses: {wins}", LETTER_FONT, HEIGHT // 2)
            button_rect = draw_button("Back to Menu", WIDTH // 2 - 100, HEIGHT // 2 + 100, 200, 60, win, BUTTON_FONT)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if button_rect.collidepoint(pygame.mouse.get_pos()):
                        return "start"

    while round_num < MAX_ROUNDS:
        clock.tick(FPS)
        elapsed = time.time() - start_time
        time_left = int(duration - elapsed)
        if elapsed >= duration:
            return end_screen("⏰ Time's Up!")

        word, hint = random.choice(word_list)
        guessed = ""
        input_active = True

        while input_active:
            clock.tick(FPS)
            elapsed = time.time() - start_time
            time_left = int(duration - elapsed)
            if elapsed >= duration:
                return end_screen("⏰ Time's Up!")

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        input_active = False
                    elif event.key == pygame.K_BACKSPACE:
                        guessed = guessed[:-1]
                    elif event.unicode.isalpha():
                        guessed += event.unicode.lower()

            win.blit(pygame.transform.scale(bg_img, (WIDTH, HEIGHT)), (0, 0))
            render_text_centered(f"🎯 Challenge Mode ({difficulty.capitalize()})", INFO_FONT, 30)
            render_text_centered(f"Round {round_num + 1}/{MAX_ROUNDS}", INFO_FONT, 80)
            render_text_centered(f"Hint: {hint}", INFO_FONT, 150)
            render_text_centered(f"Word: {'_ ' * len(word)}", LETTER_FONT, 220)
            render_text_centered(f"Your Guess: {guessed}", LETTER_FONT, 300)
            render_text_centered(f"Time Left: {time_left}s", INFO_FONT, 370)
            render_text_centered(f"Score: {wins}", INFO_FONT, 420)
            pygame.display.update()

        if guessed == word:
            wins += 1
            feedback = "✅ Correct!"
        else:
            feedback = f"❌ Wrong! Word was: {word}"

        win.blit(pygame.transform.scale(bg_img, (WIDTH, HEIGHT)), (0, 0))
        render_text_centered(feedback, LETTER_FONT, HEIGHT // 2)
        pygame.display.update()
        pygame.time.delay(1500)
        round_num += 1

    return end_screen("🎉 All Rounds Completed!")
