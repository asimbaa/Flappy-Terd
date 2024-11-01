import pygame
import pygame.freetype  # Import the freetype module
import random
import datetime
import json

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
FPS = 60  # Increased back to 60 for smoother framerate

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Terd 💩: Revenge of the Poo")

# Fonts
default_font = pygame.font.Font(None, 36)

# Load images
poo_image = pygame.image.load("poo_emoji.png")
poo_image = pygame.transform.scale(poo_image, (50, 50))  # Scale the image to appropriate size
background_image_dreamscape = pygame.image.load("dreamscape.webp")
background_image_dreamscape = pygame.transform.scale(background_image_dreamscape, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Game variables
player_name = ""
input_active = False
highscores = []
recent_players = []

# Load highscores
try:
    with open("highscores.json", "r") as f:
        highscores = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    highscores = []

# Load recent players
try:
    with open("recent_players.json", "r") as f:
        recent_players = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    recent_players = []

def save_highscores():
    with open("highscores.json", "w") as f:
        json.dump(highscores, f)

def save_recent_players():
    with open("recent_players.json", "w") as f:
        json.dump(recent_players, f)

def main_menu():
    global input_active, player_name
    menu_active = True
    while menu_active:
        screen.blit(background_image_dreamscape, (0, 0))  # Draw the dreamscape background image
        title_surface = default_font.render("Flappy Terd: Revenge of the Poo", True, BLACK)
        new_game_surface = default_font.render("1. New Game", True, BLACK)
        highscores_surface = default_font.render("2. Highscores", True, BLACK)
        exit_surface = default_font.render("3. Exit", True, BLACK)

        screen.blit(title_surface, (100, 100))
        screen.blit(poo_image, (title_surface.get_width() + 110, 85))  # Position the poo emoji image next to the title
        screen.blit(new_game_surface, (100, 200))
        screen.blit(highscores_surface, (100, 300))
        screen.blit(exit_surface, (100, 400))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    input_active = True
                    player_name = ""
                    get_player_name()
                    new_game()
                elif event.key == pygame.K_2:
                    show_highscores()
                elif event.key == pygame.K_3:
                    pygame.quit()
                    exit()

        pygame.display.flip()

def get_player_name():
    global input_active, player_name
    while input_active:
        screen.blit(background_image_dreamscape, (0, 0))  # Draw the dreamscape background image
        prompt_surface = default_font.render("Enter your name: ", True, BLACK)
        screen.blit(prompt_surface, (100, 200))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if player_name and player_name not in recent_players:
                        recent_players.append(player_name)
                        save_recent_players()
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                else:
                    player_name += event.unicode

        txt_surface = default_font.render(player_name, True, BLACK)
        screen.blit(txt_surface, (100, 300))

        pygame.display.flip()

def new_game():
    global highscores
    clock = pygame.time.Clock()
    poo_x = 100
    poo_y = SCREEN_HEIGHT // 2
    poo_speed = 0
    gravity = 0.5  # Adjusted for smoother framerate
    score = 0
    pipes = []
    pipe_width = 70
    pipe_gap = 200
    pipe_speed = 5  # Adjusted for smoother framerate
    difficulty = 1
    color_change_timer = 0
    lives = 3  # Player starts with 3 lives

    def create_pipe():
        height = random.randint(150, 450)
        return [SCREEN_WIDTH, height]

    def draw_pipes(pipes):
        for pipe in pipes:
            pygame.draw.rect(screen, GREEN, (pipe[0], 0, pipe_width, pipe[1]))
            pygame.draw.rect(screen, GREEN, (pipe[0], pipe[1] + pipe_gap, pipe_width, SCREEN_HEIGHT))

    def check_collision(pipes, poo_x, poo_y):
        for pipe in pipes:
            if poo_x + 30 > pipe[0] and poo_x < pipe[0] + pipe_width:
                if poo_y < pipe[1] or poo_y + 30 > pipe[1] + pipe_gap:
                    return True
        if poo_y < 0 or poo_y > SCREEN_HEIGHT:
            return True
        return False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    poo_speed = -10  # Adjusted for smoother framerate

        poo_speed += gravity
        poo_y += poo_speed

        if len(pipes) == 0 or pipes[-1][0] < SCREEN_WIDTH - 300:
            pipes.append(create_pipe())

        pipes = [[pipe[0] - pipe_speed, pipe[1]] for pipe in pipes if pipe[0] > -pipe_width]

        if check_collision(pipes, poo_x, poo_y):
            lives -= 1
            if lives == 0:
                highscores.append({"name": player_name, "score": score})
                highscores = sorted(highscores, key=lambda x: x["score"], reverse=True)[:10]
                save_highscores()
                break
            else:
                poo_x = 100
                poo_y = SCREEN_HEIGHT // 2
                poo_speed = 0
                pipes = []  # Reset pipes

        screen.fill(WHITE)  # Remove background image for gameplay
        screen.blit(poo_image, (poo_x, poo_y))
        draw_pipes(pipes)

        score_surface = default_font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_surface, (10, 10))

        # Draw lives
        for i in range(lives):
            screen.blit(poo_image, (SCREEN_WIDTH - (i + 1) * 60, 10))

        pygame.display.flip()
        clock.tick(FPS)

        score += 1
        if score % 100 == 0:
            difficulty += 1
            pipe_speed += 1

        color_change_timer += 1
        if color_change_timer >= FPS * 3:
            color_change_timer = 0

def show_highscores():
    while True:
        screen.blit(background_image_dreamscape, (0, 0))  # Draw the dreamscape background image
        title_surface = default_font.render("Highscores", True, BLACK)
        screen.blit(title_surface, (100, 100))

        for i, score in enumerate(highscores):
            score_surface = default_font.render(f"{i+1}. {score['name']} - {score['score']}", True, BLACK)
            screen.blit(score_surface, (100, 150 + i * 30))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

        pygame.display.flip()

if __name__ == "__main__":
    main_menu()
