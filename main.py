import pygame
import random

# Define the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Initialize Pygame
pygame.init()

# Set up the game window
window_width = 800
window_height = 600
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Memory Game")

# Set up the game clock
clock = pygame.time.Clock()

# Set up the game font
font = pygame.font.SysFont("game", 40)

# Set up the card dimensions
card_width = 100
card_height = 100

# Set up the game grid
grid_size = 4  # Adjust this value to change the grid size
grid = []
revealed = []

# Generate the grid of cards
for row in range(grid_size):
    grid.append([])
    revealed.append([])
    for col in range(grid_size):
        grid[row].append(None)
        revealed[row].append(False)

# Load card images
card_images = []
for i in range(1, (grid_size * grid_size) // 2 + 1):
    image = pygame.image.load(f"card_{i}.jpg")
    card_images.append(image)
    card_images.append(image)

# Shuffle the card images
random.shuffle(card_images)

# Calculate the positions of the cards on the grid
margin_x = (window_width - grid_size * card_width) // 2
margin_y = (window_height - grid_size * card_height) // 2

for row in range(grid_size):
    for col in range(grid_size):
        x = margin_x + col * card_width
        y = margin_y + row * card_height
        grid[row][col] = pygame.Rect(x, y, card_width, card_height)

# Variables to keep track of the game state
selected_card = None
matched_pairs = 0
turns = 0

# Game level
current_level = 1
max_level = 2
cards_per_level = 7

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                if selected_card is None:
                    # Get the clicked card position
                    mouse_pos = pygame.mouse.get_pos()
                    for row in range(grid_size):
                        for col in range(grid_size):
                            if grid[row][col].collidepoint(mouse_pos) and not revealed[row][col]:
                                revealed[row][col] = True
                                selected_card = (row, col)
                else:
                    # Get the second clicked card position
                    mouse_pos = pygame.mouse.get_pos()
                    for row in range(grid_size):
                        for col in range(grid_size):
                            if grid[row][col].collidepoint(mouse_pos) and not revealed[row][col]:
                                revealed[row][col] = True
                                if card_images.index(card_images[selected_card[0] * grid_size + selected_card[1]]) \
                                        == card_images.index(card_images[row * grid_size + col]):
                                    # Matched pair
                                    matched_pairs += 1
                                    if matched_pairs == cards_per_level:
                                        # Check if the current level is completed
                                        if current_level == max_level:
                                            # Game over condition
                                            message = "Congratulations! You completed all levels!"
                                            running = False
                                        else:
                                            # Move to the next level
                                            current_level += 1
                                            matched_pairs = 0
                                            turns = 0
                                            card_images = card_images[:cards_per_level * 2]
                                            random.shuffle(card_images)
                                            revealed = [[False] * grid_size for _ in range(grid_size)]
                                else:
                                    # Not a match
                                    pygame.time.wait(1000)
                                    revealed[selected_card[0]][selected_card[1]] = False
                                    revealed[row][col] = False
                                selected_card = None
                                turns += 1

    # Draw the background
    screen.fill(WHITE)

    # Draw the cards
    for row in range(grid_size):
        for col in range(grid_size):
            if revealed[row][col]:
                # Display the revealed card image
                card_image = card_images[row * grid_size + col]
                screen.blit(card_image, grid[row][col])
            else:
                # Display the back of the card
                pygame.draw.rect(screen, BLUE, grid[row][col])

    # Draw the game stats
    stats_text = font.render(f"Level: {current_level}    Turns: {turns}", True, BLACK)
    screen.blit(stats_text, (10, 10))

    # Update the game display
    pygame.display.flip()

    # Limit the frame rate
    clock.tick(60)

# Game over loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # Draw the game over message
    screen.fill(WHITE)
    if matched_pairs == cards_per_level:
        if current_level == max_level:
            message = "Congratulations! You completed all levels!"
        else:
            message = f"Level {current_level} completed! Proceed to the next level."
    else:
        message = "Game Over! You did not complete the level."
    message_text = font.render(message, True, BLACK)
    screen.blit(message_text, (window_width // 2 - message_text.get_width() // 2,
                               window_height // 2 - message_text.get_height() // 2))

    # Update the game over display
    pygame.display.flip()
