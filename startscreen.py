import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants and Setup
WIDTH, HEIGHT = 1200, 800
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
FONT = pygame.font.SysFont('comicsans', 50)

# Function to draw buttons
def draw_button(text, x, y, w, h, win):
    pygame.draw.rect(win, GRAY, (x, y, w, h), border_radius=10)
    label = FONT.render(text, True, BLACK)
    win.blit(label, (x + (w - label.get_width()) // 2, y + (h - label.get_height()) // 2))
    return pygame.Rect(x, y, w, h)

# Rules text
rules_text = [
    "1. Guess the word letter by letter.",
    "2. You have 6 chances to guess wrong.",
    "3. Use mouse or keyboard to play.",
    "4. Click 'Show Answer' to skip a round.",
    "5. Game ends after 10 rounds."
]

# Main Start Screen Function
def start_screen(win):
    running = True
    start_btn = draw_button("Start Game", 450, 250, 300, 70, win)
    rules_btn = draw_button("View Rules", 450, 350, 300, 70, win)
    exit_btn = draw_button("Exit", 450, 450, 300, 70, win)

    while running:
        win.fill(WHITE)
        title = FONT.render("Welcome to Hangman", True, BLACK)
        win.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if start_btn.collidepoint(mx, my):
                    print("Start Game button clicked!")
                    return "game"  # Transition to the game screen
                elif rules_btn.collidepoint(mx, my):
                    print("View Rules button clicked!")
                    return "rules"  # Transition to the rules screen
                elif exit_btn.collidepoint(mx, my):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

# Rules Screen Function
def rules_screen(win):
    running = True
    back_btn = draw_button("Back", 50, HEIGHT - 100, 200, 60, win)

    while running:
        win.fill(WHITE)
        title = FONT.render("Game Rules", True, BLACK)
        win.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))

        # Display rules
        y_offset = 120
        for rule in rules_text:
            rule_label = pygame.font.SysFont('comicsans', 36).render(rule, True, BLACK)
            win.blit(rule_label, (100, y_offset))
            y_offset += 50

        # Event handling for back button
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if back_btn.collidepoint(mx, my):
                    print("Back button clicked!")
                    return "start"  # Go back to the start screen

        pygame.display.update()

# Main entry point
def main():
    win = pygame.display.set_mode((WIDTH, HEIGHT))  # Initialize the window
    pygame.display.set_caption("Hangman Game")

    current_screen = "start"  # Starting screen

    # Main game loop
    while True:
        if current_screen == "start":
            print("Displaying Start Screen...")
            current_screen = start_screen(win)
        elif current_screen == "rules":
            print("Displaying Rules Screen...")
            current_screen = rules_screen(win)
        elif current_screen == "game":
            # You would call your game logic here
            print("Game logic goes here.")
            break

    pygame.quit()

# Start the game
if __name__ == "__main__":
    main()
