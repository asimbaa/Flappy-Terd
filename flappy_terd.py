import pygame
import random
import json

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Flappy Terd : Pooper Hero"
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
FPS = 60

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(SCREEN_TITLE)

# Fonts
font_size = 36
default_font = pygame.font.Font(None, int(font_size * 1.44))  # Increase font size by 20% twice

# Load images
poo_image = pygame.image.load("poo_emoji.png")
poo_image = pygame.transform.scale(poo_image, (50, 50))  # Scale the image to appropriate size
background_image_dreamscape = pygame.image.load("dreamscape.webp")
background_image_dreamscape = pygame.transform.scale(background_image_dreamscape, (SCREEN_WIDTH, SCREEN_HEIGHT))
background_image_shooting_star = pygame.image.load("shooting_star.png")
background_image_shooting_star = pygame.transform.scale(background_image_shooting_star, (SCREEN_WIDTH, SCREEN_HEIGHT))
pooper_hero_image = pygame.image.load("pooper_hero.webp")
pooper_hero_image = pygame.transform.scale(pooper_hero_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Load sounds
pygame.mixer.music.load("background_music.mp3")
pygame.mixer.music.play(-1)  # Play background music in a loop
flap_sound = pygame.mixer.Sound("flap.mp3")
collision_sound = pygame.mixer.Sound("collision.mp3")
score_sound = pygame.mixer.Sound("score.mp3")

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

def render_text_3d(text, font, color, shadow_color, x, y):
    shadow_offset = 2
    shadow_surface = font.render(text, True, shadow_color)
    text_surface = font.render(text, True, color)
    screen.blit(shadow_surface, (x + shadow_offset, y + shadow_offset))
    screen.blit(text_surface, (x, y))

def countdown_timer():
    for i in range(3, 0, -1):
        screen.blit(background_image_dreamscape, (0, 0))  # Draw the dreamscape background image
        render_text_3d(str(i), default_font, BLACK, WHITE, SCREEN_WIDTH // 2 - default_font.size(str(i))[0] // 2, SCREEN_HEIGHT // 2 - default_font.size(str(i))[1] // 2)
        pygame.display.flip()
        pygame.time.wait(1000)  # Wait for 1 second

def get_player_name():
    global input_active, player_name
    input_active = True
    while input_active:
        screen.blit(background_image_dreamscape, (0, 0))  # Draw the dreamscape background image
        render_text_3d("Enter your name: ", default_font, BLACK, WHITE, SCREEN_WIDTH // 2 - default_font.size("Enter your name: ")[0] // 2, 200)

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
        screen.blit(txt_surface, (SCREEN_WIDTH // 2 - txt_surface.get_width() // 2, 300))

        pygame.display.flip()

def main_menu():
    global input_active, player_name
    menu_active = True
    while menu_active:
        screen.blit(background_image_dreamscape, (0, 0))  # Draw the dreamscape background image
        render_text_3d("Flappy Terd : Pooper Hero", default_font, BLACK, WHITE, SCREEN_WIDTH // 2 - default_font.size("Flappy Terd : Pooper Hero")[0] // 2, 100)
        new_game_surface = default_font.render("New Game", True, BLACK)
        highscores_surface = default_font.render("Highscores", True, BLACK)
        exit_surface = default_font.render("Exit", True, BLACK)

        screen.blit(poo_image, (SCREEN_WIDTH // 2 + default_font.size("Flappy Terd : Pooper Hero")[0] // 2 + 10, 85))  # Position the poo emoji image next to the title
        render_text_3d("New Game", default_font, BLACK, WHITE, SCREEN_WIDTH // 2 - new_game_surface.get_width() // 2, 200)
        render_text_3d("Highscores", default_font, BLACK, WHITE, SCREEN_WIDTH // 2 - highscores_surface.get_width() // 2, 300)
        render_text_3d("Exit", default_font, BLACK, WHITE, SCREEN_WIDTH // 2 - exit_surface.get_width() // 2, 400)

        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        if new_game_surface.get_rect(topleft=(SCREEN_WIDTH // 2 - new_game_surface.get_width() // 2, 200)).collidepoint(mouse_pos):
            if mouse_click[0]:
                countdown_timer()
                new_game()
        if highscores_surface.get_rect(topleft=(SCREEN_WIDTH // 2 - highscores_surface.get_width() // 2, 300)).collidepoint(mouse_pos):
            if mouse_click[0]:
                show_highscores()
        if exit_surface.get_rect(topleft=(SCREEN_WIDTH // 2 - exit_surface.get_width() // 2, 400)).collidepoint(mouse_pos):
            if mouse_click[0]:
                pygame.quit()
                exit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        pygame.display.flip()

def new_game():
    global highscores
    clock = pygame.time.Clock()
    poo_x = 100
    poo_y = SCREEN_HEIGHT // 2
    poo_speed = 0

    # Hard mode settings
    gravity = 0.4
    pipe_speed = 4

    score = 0
    pipes = []
    pipe_width = 70
    pipe_gap = 200 * 1.2  # Increase the gap by 20%
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
                    flap_sound.play()

        poo_speed += gravity
        poo_y += poo_speed

        if len(pipes) == 0 or pipes[-1][0] < SCREEN_WIDTH - 300:
            pipes.append(create_pipe())

        pipes = [[pipe[0] - pipe_speed, pipe[1]] for pipe in pipes if pipe[0] > -pipe_width]

        if check_collision(pipes, poo_x, poo_y):
            collision_sound.play()
            lives -= 1
            if lives == 0:
                highscores.append({"name": player_name, "score": score})
                highscores = sorted(highscores, key=lambda x: x["score"], reverse=True)[:10]
                save_highscores()
                if highscores[0]['name'] == player_name and highscores[0]['score'] == score:
                    show_congrats_screen()
                break
            else:
                poo_x = 100
                poo_y = SCREEN_HEIGHT // 2
                poo_speed = 0
                pipes = []  # Reset pipes

        screen.blit(background_image_shooting_star, (0, 0))  # Draw the shooting star background image
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
            score_sound.play()

        color_change_timer += 1
        if color_change_timer >= FPS * 3:
            color_change_timer = 0

def show_congrats_screen():
    screen.blit(pooper_hero_image, (0, 0))  # Draw the pooper hero image
    render_text_3d("Congrats! You've got the High Score! :)", default_font, BLACK, WHITE, SCREEN_WIDTH // 2 - default_font.size("Congrats! You've got the High Score! :)")[0] // 2, SCREEN_HEIGHT // 2)
    pygame.display.flip()
    pygame.time.wait(3000)  # Display for 3 seconds

def show_highscores():
    while True:
        screen.blit(background_image_dreamscape, (0, 0))  # Draw the dreamscape background image
        render_text_3d("Highscores", default_font, BLACK, WHITE, SCREEN_WIDTH // 2 - default_font.size("Highscores")[0] // 2, 100)

        for i, score in enumerate(highscores):
            score_surface = default_font.render(f"{i+1}. {score['name']} - {score['score']}", True, BLACK)
            screen.blit(score_surface, (SCREEN_WIDTH // 2 - score_surface.get_width() // 2, 150 + i * 30))

        back_surface = default_font.render("Back", True, BLACK)
        screen.blit(back_surface, (SCREEN_WIDTH // 2 - back_surface.get_width() // 2, 500))

        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        if back_surface.get_rect(topleft=(SCREEN_WIDTH // 2 - back_surface.get_width() // 2, 500)).collidepoint(mouse_pos):
            if mouse_click[0]:
                return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        pygame.display.flip()

if __name__ == "__main__":
    get_player_name()
    main_menu()