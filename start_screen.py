"""
import pygame
import sys
from utils import draw_button, get_fonts
from challenge import challenge_mode

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def start_screen(win, WIDTH, HEIGHT):
    fonts = get_fonts()
    title_font = fonts["title"]
    button_font = fonts["button"]

    # Create buttons
    start_game_btn = pygame.Rect(WIDTH // 2 - 100, 300, 200, 60)
    view_rules_btn = pygame.Rect(WIDTH // 2 - 100, 400, 200, 60)
    challenge_btn = pygame.Rect(WIDTH // 2 - 100, 500, 200, 60)

    while True:
        win.fill(WHITE)

        # Draw the title
        title = title_font.render("Welcome to Hangman!", True, BLACK)
        win.blit(title, (WIDTH // 2 - title.get_width() // 2, 150))

        # Draw buttons
        draw_button("Start Game", start_game_btn.x, start_game_btn.y, start_game_btn.width, start_game_btn.height, win, button_font)
        draw_button("View Rules", view_rules_btn.x, view_rules_btn.y, view_rules_btn.width, view_rules_btn.height, win, button_font)
        draw_button("Challenge", challenge_btn.x, challenge_btn.y, challenge_btn.width, challenge_btn.height, win, button_font)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()

                if start_game_btn.collidepoint(mx, my):
                    return "level"

                if view_rules_btn.collidepoint(mx, my):
                    return "rules"

                if challenge_btn.collidepoint(mx, my):
                    challenge_mode(win, WIDTH, HEIGHT, difficulty="easy")

        pygame.display.update()
"""
import pygame
import sys
from utils import draw_button, get_fonts
from challenge import challenge_mode

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def start_screen(win, WIDTH, HEIGHT):
    pygame.init()
    fonts = get_fonts()
    title_font = fonts["title"]
    button_font = fonts["button"]

    # Load background image
    try:
        background_img = pygame.image.load("bghang.jpg")
    except pygame.error:
        print("Failed to load background image. Check path and filename.")
        background_img = pygame.Surface((WIDTH, HEIGHT))
        background_img.fill(WHITE)

    # Initial window size
    current_width, current_height = WIDTH, HEIGHT

    # Button base positions (we'll scale them later based on new window size)
    start_game_btn = pygame.Rect(WIDTH // 2 - 100, 300, 200, 60)
    view_rules_btn = pygame.Rect(WIDTH // 2 - 100, 400, 200, 60)
    challenge_btn = pygame.Rect(WIDTH // 2 - 100, 500, 200, 60)

    while True:
        # Check for resizing events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.VIDEORESIZE:
                current_width, current_height = event.w, event.h
                win = pygame.display.set_mode((current_width, current_height), pygame.RESIZABLE)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if start_game_btn.collidepoint(mx, my):
                    return "level"
                if view_rules_btn.collidepoint(mx, my):
                    return "rules"
                if challenge_btn.collidepoint(mx, my):
                    challenge_mode(win, current_width, current_height, difficulty="easy")

        # Scale and draw background image to fit current window
        scaled_bg = pygame.transform.scale(background_img, (current_width, current_height))
        win.blit(scaled_bg, (0, 0))

        # Title
        title = title_font.render("Welcome to Hangman!", True, BLACK)
        win.blit(title, (current_width // 2 - title.get_width() // 2, 150))

        # Update buttons to be centered with new dimensions
        start_game_btn = pygame.Rect(current_width // 2 - 100, 300, 200, 60)
        view_rules_btn = pygame.Rect(current_width // 2 - 100, 400, 200, 60)
        challenge_btn = pygame.Rect(current_width // 2 - 100, 500, 200, 60)

        # Draw buttons
        draw_button("Start Game", start_game_btn.x, start_game_btn.y, start_game_btn.width, start_game_btn.height, win, button_font)
        draw_button("View Rules", view_rules_btn.x, view_rules_btn.y, view_rules_btn.width, view_rules_btn.height, win, button_font)
        draw_button("Challenge", challenge_btn.x, challenge_btn.y, challenge_btn.width, challenge_btn.height, win, button_font)

        pygame.display.update()
