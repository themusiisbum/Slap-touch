import pygame
import socket
import threading
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Tag Game')

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Sprites (placeholders for now, replace with your actual sprite images)
green_tagger = pygame.Surface((50, 50))
green_tagger.fill((0, 255, 0))
blue_player = pygame.Surface((50, 50))
blue_player.fill((0, 0, 255))

# Game variables
mode = "Classic"
current_screen = "Home"
players = []
username = input("Enter your username: ")

# Network setup
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 12345))

def receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == 'USERNAME':
                client.send(username.encode('utf-8'))
            else:
                print(message)
        except:
            print("An error occurred!")
            client.close()
            break

def send_message(message):
    client.send(message.encode('utf-8'))

receive_thread = threading.Thread(target=receive)
receive_thread.start()

# Function to display text on the screen
def display_text(text, size, color, x, y):
    font = pygame.font.Font(None, size)
    surface = font.render(text, True, color)
    screen.blit(surface, (x, y))

# Home screen
def home_screen():
    global current_screen
    screen.fill(WHITE)
    display_text("Welcome to the Tag Game", 50, BLACK, 200, 100)
    display_text("1. Start Game", 40, BLACK, 300, 200)
    display_text("2. Help", 40, BLACK, 300, 300)
    display_text("3. Modes", 40, BLACK, 300, 400)
    pygame.display.update()

# Help screen
def help_screen():
    global current_screen
    screen.fill(WHITE)
    display_text("Controls for the mobile-friendly game:", 40, BLACK, 50, 100)
    display_text("Move: Swipe in the direction you want to move", 30, BLACK, 50, 200)
    display_text("Tag: Tap the screen", 30, BLACK, 50, 300)
    display_text("Press any key to go back", 30, BLACK, 50, 400)
    pygame.display.update()

# Modes screen
def modes_screen():
    global current_screen
    screen.fill(WHITE)
    display_text("Select Mode:", 50, BLACK, 300, 100)
    display_text("1. Classic", 40, BLACK, 300, 200)
    display_text("2. Battle Royal", 40, BLACK, 300, 300)
    display_text("3. Ranked", 40, BLACK, 300, 400)
    pygame.display.update()

# Game screen (dummy)
def game_screen():
    global current_screen
    screen.fill(WHITE)
    display_text(f"Game started in {mode} mode", 50, BLACK, 200, 100)
    # Just displaying sprites for now, replace with actual game logic
    screen.blit(green_tagger, (100, 100))
    screen.blit(blue_player, (200, 200))
    pygame.display.update()

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            client.close()
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if current_screen == "Home":
                if event.key == pygame.K_1:
                    current_screen = "Game"
                    send_message(f'{username} started the game.')
                elif event.key == pygame.K_2:
                    current_screen = "Help"
                elif event.key == pygame.K_3:
                    current_screen = "Modes"
            elif current_screen == "Help":
                current_screen = "Home"
            elif current_screen == "Modes":
                if event.key == pygame.K_1:
                    mode = "Classic"
                elif event.key == pygame.K_2:
                    mode = "Battle Royal"
                elif event.key == pygame.K_3:
                    mode = "Ranked"
                current_screen = "Home"

    if current_screen == "Home":
        home_screen()
    elif current_screen == "Help":
        help_screen()
    elif current_screen == "Modes":
        modes_screen()
    elif current_screen == "Game":
        game_screen()

pygame.quit()
sys.exit()
