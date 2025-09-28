"""
import pygame
import sys
from game_screen import game_screen
from start_screen import start_screen
from rules_screen import rules_screen
from levels import level_selection_screen
from profile_manager import create_profile, get_user_stats

# Initialize Pygame
pygame.init()

# Set initial window
WIDTH, HEIGHT = 1200, 800
win = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Hangman Game")

# Profile screen
def profile_screen(win, width, height):
    screen = win
    clock = pygame.time.Clock()

    try:
        background = pygame.image.load("bghang.jpg")
        bg_loaded = True
    except:
        bg_loaded = False

    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    DARK_GRAY = (30, 30, 30)
    NEON_BLUE = (0, 255, 255)
    RED = (255, 50, 50)

    username = ""
    active_input = True
    profile_loaded = False
    show_cursor = True
    cursor_timer = 0

    while True:
        screen.fill(DARK_GRAY)
        if bg_loaded:
            bg_scaled = pygame.transform.scale(background, screen.get_size())
            screen.blit(bg_scaled, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if active_input:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if username.strip():
                            create_profile(username.strip())
                            profile_loaded = True
                            active_input = False
                    elif event.key == pygame.K_BACKSPACE:
                        username = username[:-1]
                    else:
                        if len(username) < 20:
                            username += event.unicode
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)
    
        # Fonts
        title_font = pygame.font.SysFont("comicsans", 80, bold=True)
        input_font = pygame.font.SysFont("comicsans", 36, bold=True)
        stats_font = pygame.font.SysFont("comicsans", 30)

        # Title
        title_text = title_font.render("WELCOME! TO THE GAME", True, BLACK)
        title_rect = title_text.get_rect(center=(screen.get_width() // 2, 100))
        screen.blit(title_text, title_rect)

        if active_input:
            prompt = input_font.render("Enter your name:", True, BLACK)
            screen.blit(prompt, (screen.get_width() // 2 - 150, 220))

            input_rect = pygame.Rect(screen.get_width() // 2 - 200, 270, 400, 60)
            pygame.draw.rect(screen, BLACK, input_rect, border_radius=15)
            pygame.draw.rect(screen, NEON_BLUE, input_rect, 3, border_radius=15)

            display_name = username + ("|" if show_cursor else "")
            user_text = input_font.render(display_name, True, NEON_BLUE)
            screen.blit(user_text, (input_rect.x + 15, input_rect.y + 15))

            cursor_timer += 1
            if cursor_timer >= 30:
                show_cursor = not show_cursor
                cursor_timer = 0

        elif profile_loaded:
            stats = get_user_stats(username)
            welcome = input_font.render(f"Welcome, {username}!", True, NEON_BLUE)
            screen.blit(welcome, (screen.get_width() // 2 - 200, 200))

            lines = [
                f"Matches Played: {stats['matches_played']}",
                f"Wins: {stats['wins']}",
                f"Losses: {stats['losses']}",
                f"Challenges Attempted: {stats['challenges_attempted']}",
                f"Challenge Score: {stats['challenge_score']}",
                f"High Score: {stats['high_score']}"
            ]

            for i, line in enumerate(lines):
                stat_line = stats_font.render(line, True, BLACK)
                screen.blit(stat_line, (screen.get_width() // 2 - 200, 260 + i * 40))

            pygame.display.flip()
            pygame.time.wait(2000)  # Show profile for 2 seconds before continuing
            return username

        pygame.display.flip()
        clock.tick(60)

# Main loop
def run():
    global WIDTH, HEIGHT
    username = profile_screen(win, WIDTH, HEIGHT)  # Show profile screen first

    current_screen = "start"
    difficulty = None

    while True:
        WIDTH, HEIGHT = win.get_size()

        if current_screen == "start":
            current_screen = start_screen(win, WIDTH, HEIGHT)
        elif current_screen == "rules":
            current_screen = rules_screen(win, WIDTH, HEIGHT)
        elif current_screen == "level":
            difficulty = level_selection_screen(win, WIDTH, HEIGHT)
            current_screen = "game"
        elif current_screen == "game":
            current_screen = game_screen(win, WIDTH, HEIGHT, difficulty, username)

if __name__ == "__main__":
    run()
    pygame.quit()
    sys.exit()
"""
import pygame
import sys
from game_screen import game_screen
from start_screen import start_screen
from rules_screen import rules_screen
from levels import level_selection_screen
from profile_manager import create_profile, get_user_stats

# Initialize Pygame
pygame.init()

# Set initial window
WIDTH, HEIGHT = 1200, 800
win = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Hangman Game")

# Profile screen
def profile_screen(win, width, height):
    screen = win
    clock = pygame.time.Clock()

    try:
        background = pygame.image.load("bghang.jpg")
        bg_loaded = True
    except:
        bg_loaded = False

    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    DARK_GRAY = (30, 30, 30)
    NEON_BLUE = (0, 255, 255)

    username = ""
    active_input = True
    profile_loaded = False
    show_cursor = True
    cursor_timer = 0

    while True:
        screen.fill(DARK_GRAY)
        if bg_loaded:
            bg_scaled = pygame.transform.scale(background, screen.get_size())
            screen.blit(bg_scaled, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if active_input:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if username.strip():
                            create_profile(username.strip())
                            profile_loaded = True
                            active_input = False
                    elif event.key == pygame.K_BACKSPACE:
                        username = username[:-1]
                    else:
                        if len(username) < 20:
                            username += event.unicode
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)
    
        # Fonts
        title_font = pygame.font.SysFont("comicsans", 80, bold=True)
        input_font = pygame.font.SysFont("comicsans", 36, bold=True)
        stats_font = pygame.font.SysFont("comicsans", 30)

        # Title
        title_text = title_font.render("WELCOME! TO THE GAME", True, BLACK)
        title_rect = title_text.get_rect(center=(screen.get_width() // 2, 100))
        screen.blit(title_text, title_rect)

        if active_input:
            prompt = input_font.render("Enter your name:", True, BLACK)
            screen.blit(prompt, (screen.get_width() // 2 - 150, 220))

            input_rect = pygame.Rect(screen.get_width() // 2 - 200, 270, 400, 60)
            pygame.draw.rect(screen, BLACK, input_rect, border_radius=15)
            pygame.draw.rect(screen, NEON_BLUE, input_rect, 3, border_radius=15)

            display_name = username + ("|" if show_cursor else "")
            user_text = input_font.render(display_name, True, NEON_BLUE)
            screen.blit(user_text, (input_rect.x + 15, input_rect.y + 15))

            cursor_timer += 1
            if cursor_timer >= 30:
                show_cursor = not show_cursor
                cursor_timer = 0

        elif profile_loaded:
            stats = get_user_stats(username)
            if stats is None:  # fallback in case profile creation failed
                stats = {
                    "matches_played": 0,
                    "wins": 0,
                    "losses": 0,
                    "challenges_attempted": 0,
                    "challenge_score": 0,
                    "high_score": 0
                }

            welcome = input_font.render(f"Welcome, {username}!", True, NEON_BLUE)
            screen.blit(welcome, (screen.get_width() // 2 - 200, 200))

            lines = [
                f"Matches Played: {stats['matches_played']}",
                f"Wins: {stats['wins']}",
                f"Losses: {stats['losses']}",
                f"Challenges Attempted: {stats['challenges_attempted']}",
                f"Challenge Score: {stats['challenge_score']}",
                f"High Score: {stats['high_score']}"
            ]

            for i, line in enumerate(lines):
                stat_line = stats_font.render(line, True, BLACK)
                screen.blit(stat_line, (screen.get_width() // 2 - 200, 260 + i * 40))

            pygame.display.flip()
            pygame.time.wait(2000)  # Show profile for 2 seconds before continuing
            return username

        pygame.display.flip()
        clock.tick(60)

# Main loop
def run():
    global WIDTH, HEIGHT
    username = profile_screen(win, WIDTH, HEIGHT)

    current_screen = "start"
    difficulty = None

    while True:
        WIDTH, HEIGHT = win.get_size()

        if current_screen == "start":
            current_screen = start_screen(win, WIDTH, HEIGHT)
        elif current_screen == "rules":
            current_screen = rules_screen(win, WIDTH, HEIGHT)
        elif current_screen == "level":
            difficulty = level_selection_screen(win, WIDTH, HEIGHT)
            current_screen = "game"
        elif current_screen == "game":
            current_screen = game_screen(win, WIDTH, HEIGHT, difficulty, username)

if __name__ == "__main__":
    run()
    pygame.quit()
    sys.exit()
