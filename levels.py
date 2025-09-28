"""
import pygame
import sys
from utils import draw_button, get_fonts  # Assuming this imports utility functions like draw_button

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def level_selection_screen(win, WIDTH, HEIGHT):
    fonts = get_fonts()  # Get fonts
    button_font = fonts["button"]

    # Create buttons for selecting difficulty
    easy_btn = pygame.Rect(WIDTH // 2 - 100, 300, 200, 60)
    medium_btn = pygame.Rect(WIDTH // 2 - 100, 400, 200, 60)
    hard_btn = pygame.Rect(WIDTH // 2 - 100, 500, 200, 60)

    while True:
        win.fill(WHITE)  # Clear screen

        # Draw title
        title = fonts["title"].render("Select Difficulty", True, BLACK)
        win.blit(title, (WIDTH // 2 - title.get_width() // 2, 150))  # Position title in the center

        # Draw difficulty buttons
        draw_button("Easy", easy_btn.x, easy_btn.y, easy_btn.width, easy_btn.height, win, button_font)
        draw_button("Medium", medium_btn.x, medium_btn.y, medium_btn.width, medium_btn.height, win, button_font)
        draw_button("Hard", hard_btn.x, hard_btn.y, hard_btn.width, hard_btn.height, win, button_font)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()

                # Check if a difficulty button was clicked
                if easy_btn.collidepoint(mx, my):
                    print("Easy button clicked")  # Debugging line
                    return "easy"  # Return selected difficulty
                elif medium_btn.collidepoint(mx, my):
                    print("Medium button clicked")  # Debugging line
                    return "medium"
                elif hard_btn.collidepoint(mx, my):
                    print("Hard button clicked")  # Debugging line
                    return "hard"

        pygame.display.update()  # Update the screen
"""
import pygame
import sys
from utils import draw_button, get_fonts

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def level_selection_screen(win, WIDTH, HEIGHT):
    pygame.init()
    fonts = get_fonts()
    button_font = fonts["button"]
    title_font = fonts["title"]

    # Load the background image
    try:
        background_img = pygame.image.load("bghang.jpg")  # Adjust path as needed
    except pygame.error:
        print("Failed to load background image. Using fallback.")
        background_img = pygame.Surface((WIDTH, HEIGHT))
        background_img.fill(WHITE)

    # Initial dimensions
    current_width, current_height = WIDTH, HEIGHT

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.VIDEORESIZE:
                current_width, current_height = event.w, event.h
                win = pygame.display.set_mode((current_width, current_height), pygame.RESIZABLE)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if easy_btn.collidepoint(mx, my):
                    print("Easy button clicked")
                    return "easy"
                elif medium_btn.collidepoint(mx, my):
                    print("Medium button clicked")
                    return "medium"
                elif hard_btn.collidepoint(mx, my):
                    print("Hard button clicked")
                    return "hard"

        # Draw and scale background
        scaled_bg = pygame.transform.scale(background_img, (current_width, current_height))
        win.blit(scaled_bg, (0, 0))

        # Draw title
        title = title_font.render("Select Difficulty", True, BLACK)
        win.blit(title, (current_width // 2 - title.get_width() // 2, 150))

        # Update buttons based on current window size
        easy_btn = pygame.Rect(current_width // 2 - 100, 300, 200, 60)
        medium_btn = pygame.Rect(current_width // 2 - 100, 400, 200, 60)
        hard_btn = pygame.Rect(current_width // 2 - 100, 500, 200, 60)

        # Draw difficulty buttons
        draw_button("Easy", easy_btn.x, easy_btn.y, easy_btn.width, easy_btn.height, win, button_font)
        draw_button("Medium", medium_btn.x, medium_btn.y, medium_btn.width, medium_btn.height, win, button_font)
        draw_button("Hard", hard_btn.x, hard_btn.y, hard_btn.width, hard_btn.height, win, button_font)

        pygame.display.update()
