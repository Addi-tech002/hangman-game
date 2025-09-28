import pygame
import sys
from profile_manager import create_profile, get_user_stats

pygame.init()
screen = pygame.display.set_mode((1000, 700), pygame.RESIZABLE)
pygame.display.set_caption("Hangman: Enter Player Name")
clock = pygame.time.Clock()

# Load optional background
try:
    background = pygame.image.load("bghang.jpg")
    bg_loaded = True
except:
    bg_loaded = False

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_GRAY = (30, 30, 30)
LIGHT_BLUE = (100, 200, 255)
NEON_BLUE = (0, 255, 255)
RED = (255, 50, 50)

def get_scaled_font(size, base=1000):
    scale = screen.get_width() / base
    return pygame.font.SysFont("comicsans", int(size * scale), bold=True)

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

    title_font = get_scaled_font(80)
    input_font = get_scaled_font(36)
    stats_font = get_scaled_font(30)

    # Title
    title_text = title_font.render("WELCOME! TO THE GAME", True, RED)
    title_rect = title_text.get_rect(center=(screen.get_width() // 2, 100))
    screen.blit(title_text, title_rect)

    if active_input:
        prompt = input_font.render("Enter your name:", True, WHITE)
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
        welcome = input_font.render(f"Welcome, {username}!", True, LIGHT_BLUE)
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
            stat_line = stats_font.render(line, True, WHITE)
            screen.blit(stat_line, (screen.get_width() // 2 - 200, 260 + i * 40))

    pygame.display.flip()
    clock.tick(60)  