
import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Breakout")

# Define constant of the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLORS = [(255, 0, 0), (255, 165, 0), (255, 255, 0), (0, 255, 0), (0, 255, 255), (0, 0, 255), (255, 0, 255)]

# Define the paddle
PADDLE_WIDTH, PADDLE_HEIGHT = 100, 10
paddle = pygame.Rect(WIDTH // 2 - PADDLE_WIDTH // 2, HEIGHT - 30, PADDLE_WIDTH, PADDLE_HEIGHT)
paddle_speed = 10

# Define the ball
BALL_RADIUS = 10
ball = pygame.Rect(WIDTH // 2, HEIGHT // 2, BALL_RADIUS * 2, BALL_RADIUS * 2)
ball_speed_x = 5 * random.choice((1, -1))
ball_speed_y = -5

# Define the bricks
BRICK_WIDTH = 60
BRICK_HEIGHT = 30
BRICK_ROWS = 5
BRICK_COLUMNS = WIDTH // BRICK_WIDTH
bricks = []

for row in range(BRICK_ROWS):
    for col in range(BRICK_COLUMNS):
        brick = pygame.Rect(col * BRICK_WIDTH, row * BRICK_HEIGHT, BRICK_WIDTH, BRICK_HEIGHT)
        bricks.append(brick)

# Initialize scoreboard
score = 0
high_score = 0

def draw():
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, paddle)
    pygame.draw.ellipse(screen, WHITE, ball)
    
    for i, brick in enumerate(bricks):
        color = COLORS[i % len(COLORS)]
        pygame.draw.rect(screen, color, brick)

    # Draw the score
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, WHITE)
    high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(high_score_text, (10, 50))
    
    pygame.display.flip()

def move_paddle():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle.left > 0:
        paddle.left -= paddle_speed
    if keys[pygame.K_RIGHT] and paddle.right < WIDTH:
        paddle.right += paddle_speed

def move_ball():
    global ball_speed_x, ball_speed_y, game_over, score, high_score

    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.left <= 0 or ball.right >= WIDTH:
        ball_speed_x = -ball_speed_x
    if ball.top <= 0:
        ball_speed_y = -ball_speed_y
    if ball.colliderect(paddle):
        ball_speed_y = -ball_speed_y

    for brick in bricks[:]:
        if ball.colliderect(brick):
            bricks.remove(brick)
            ball_speed_y = -ball_speed_y
            score += 1
            if score > high_score:
                high_score = score
            break

    if ball.bottom >= HEIGHT:
        game_over = True

def draw_game_over():
    font = pygame.font.Font(None, 74)
    text = font.render("Game Over", True, WHITE)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 3))

    font = pygame.font.Font(None, 36)
    play_again_text = font.render("Play Again", True, WHITE)
    quit_text = font.render("Quit", True, WHITE)
    
    play_again_rect = play_again_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    quit_rect = quit_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
    
    pygame.draw.rect(screen, COLORS[0], play_again_rect.inflate(20, 20))
    pygame.draw.rect(screen, COLORS[1], quit_rect.inflate(20, 20))
    
    screen.blit(play_again_text, play_again_rect)
    screen.blit(quit_text, quit_rect)
    
    pygame.display.flip()
    
    return play_again_rect, quit_rect

def reset_game():
    global paddle, ball, ball_speed_x, ball_speed_y, bricks, game_over, score
    paddle = pygame.Rect(WIDTH // 2 - PADDLE_WIDTH // 2, HEIGHT - 30, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = pygame.Rect(WIDTH // 2, HEIGHT // 2, BALL_RADIUS * 2, BALL_RADIUS * 2)
    ball_speed_x = 5 * random.choice((1, -1))
    ball_speed_y = -5
    bricks = []
    for row in range(BRICK_ROWS):
        for col in range(BRICK_COLUMNS):
            brick = pygame.Rect(col * BRICK_WIDTH, row * BRICK_HEIGHT, BRICK_WIDTH, BRICK_HEIGHT)
            bricks.append(brick)
    score = 0
    game_over = False

# Game loop
game_over = False
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if game_over:
        play_again_rect, quit_rect = draw_game_over()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_again_rect.collidepoint(event.pos):
                    reset_game()
                elif quit_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
    else:
        move_paddle()
        move_ball()
        draw()
    
    pygame.time.Clock().tick(60)
