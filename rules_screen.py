"""
import pygame
import sys
from utils import draw_button, get_fonts

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def rules_screen(win, WIDTH, HEIGHT):
    fonts = get_fonts()
    title_font = fonts["title"]
    button_font = fonts["button"]
    rules_font = pygame.font.SysFont("comicsans", 30)

    return_btn = pygame.Rect(WIDTH // 2 - 100, 600, 200, 60)

    rules_lines = [
        
        "1. A word will be chosen randomly based on the selected difficulty.",
        "2. You will guess letters to reveal the word.",
        "3. Each incorrect guess results in a part of the hangman being drawn.",
        "4. If you reveal the word before the hangman is fully drawn, you win!"
    ]

    while True:
        win.fill(WHITE)

        # Title
        title = title_font.render("Rules of Hangman", True, BLACK)
        win.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))

        # Render each rule line separately
        start_y = 200
        line_spacing = 40
        for i, line in enumerate(rules_lines):
            text_surface = rules_font.render(line, True, BLACK)
            win.blit(text_surface, (WIDTH // 2 - text_surface.get_width() // 2, start_y + i * line_spacing))

        # Button
        draw_button("Back to Start", return_btn.x, return_btn.y, return_btn.width, return_btn.height, win, button_font)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if return_btn.collidepoint(mx, my):
                    return "start"

        pygame.display.update()

    """
import pygame
import sys
from utils import draw_button, get_fonts

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def rules_screen(win, WIDTH, HEIGHT):
    fonts = get_fonts()
    title_font = fonts["title"]
    button_font = fonts["button"]
    rules_font = pygame.font.SysFont("comicsans", int(WIDTH * 0.02))  # Scaled font size

    # Load background image
    try:
        bg_img = pygame.image.load("bghang.jpg")
    except:
        bg_img = pygame.Surface((WIDTH, HEIGHT))
        bg_img.fill(WHITE)

    return_btn = pygame.Rect(WIDTH // 2 - 100, int(HEIGHT * 0.8), 200, 60)

    rules_lines = [
        "1. A word will be chosen randomly based on the selected difficulty.",
        "2. You will guess letters to reveal the word.",
        "3. Each incorrect guess results in a part of the hangman being drawn.",
        "4. If you reveal the word before the hangman is fully drawn, you win!"
    ]

    while True:
        # Draw background
        win.blit(pygame.transform.scale(bg_img, (WIDTH, HEIGHT)), (0, 0))

        # Title
        title = title_font.render("Rules of Hangman", True, BLACK)
        win.blit(title, (WIDTH // 2 - title.get_width() // 2, int(HEIGHT * 0.1)))

        # Rules
        start_y = int(HEIGHT * 0.25)
        spacing = int(HEIGHT * 0.06)
        for i, line in enumerate(rules_lines):
            text_surface = rules_font.render(line, True, BLACK)
            win.blit(text_surface, (WIDTH // 2 - text_surface.get_width() // 2, start_y + i * spacing))

        # Button
        draw_button("Back to Start", return_btn.x, return_btn.y, return_btn.width, return_btn.height, win, button_font)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if return_btn.collidepoint(mx, my):
                    return "start"

        pygame.display.update()

