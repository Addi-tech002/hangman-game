
import pygame
import random

# Colors
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)

def scale_font(size, width):
    """Scales font size based on screen width."""
    return pygame.font.SysFont('comicsans', int(size * width / 1200))

def get_fonts():
    """Returns a dictionary of pre-configured fonts."""
    return {
        "title": pygame.font.SysFont('comicsans', 48),
        "text": pygame.font.SysFont('comicsans', 28),
        "button": pygame.font.SysFont('comicsans', 36),
    }

def draw_button(text, x, y, width, height, win, font, 
                bg_color=(200, 200, 200), text_color=(0, 0, 0), border_radius=10):
    """Draws a button and returns its rectangle for event handling."""
    pygame.draw.rect(win, bg_color, (x, y, width, height), border_radius=border_radius)  # Draw the button
    label = font.render(text, True, text_color)  # Render the text
    win.blit(label, (x + (width - label.get_width()) // 2, y + (height - label.get_height()) // 2))
    return pygame.Rect(x, y, width, height)


def load_word_and_hint(difficulty):
    """Loads a word and its hint from a file based on difficulty."""
    filename = "word.txt"
    
    try:
        with open(filename, "r") as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        return "unknown", "File not found."

    # Filter words based on difficulty
    if difficulty == "easy":
        filtered = [line for line in lines if line.startswith("easy:")]
    elif difficulty == "medium":
        filtered = [line for line in lines if line.startswith("medium:")]
    else:
        filtered = [line for line in lines if line.startswith("hard:")]

    pairs = []
    for line in filtered:
        try:
            _, content = line.strip().split(":", 1)  # Split difficulty and content
            word, hint = content.split(" - ", 1)  # Split word and hint
            pairs.append((word.strip(), hint.strip()))
        except ValueError:
            # Skip badly formatted lines
            continue

    if not pairs:
        return "unknown", "No word found for this difficulty"

    return random.choice(pairs)

def disable_letter_on_screen(letter, letters):
    """Disables the letter on the screen after it has been guessed."""
    for l in letters:
        if l[2] == letter:  # Check the letter
            l[3] = False  # Mark it as inactive
            break

def calculate_letter_positions(width, height, radius, gap):
    """Calculates the positions of all the letters (A-Z) on the screen."""
    letters = []
    startx = round((width - (radius * 2 + gap) * 13) / 2)  # Starting X position (centered)
    starty = height - 170  # Starting Y position

    for i in range(26):
        x = startx + gap * 2 + ((radius * 2 + gap) * (i % 13))  # Calculate X position
        y = starty + ((i // 13) * (gap + radius * 2))  # Calculate Y position (two rows)
        letters.append([x, y, chr(65 + i), True])  # Add letter and initial active status

    return letters
