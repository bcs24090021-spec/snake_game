#!/usr/bin/env python3
"""Snake game using pygame.

Features:
- Colored snake (green) and food (red)
- Pause (P), Restart (R), Quit (Q)
- Persistent high score stored in highscore.txt
"""

import pygame
import random
import os
import sys

# Grid configuration
GRID_W = 20
GRID_H = 20
CELL_SIZE = 30
INITIAL_DELAY = 120  # milliseconds per move
SPEEDUP_EVERY = 5    # speed up every N points

WINDOW_WIDTH = GRID_W * CELL_SIZE + 40
WINDOW_HEIGHT = GRID_H * CELL_SIZE + 120

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
DARK_GRAY = (50, 50, 50)

HIGH_SCORE_FILE = os.path.join("E:\\snake_game", "highscore.txt")


def load_highscore(path):
    try:
        with open(path, 'r') as f:
            return int(f.read().strip())
    except Exception:
        return 0


def save_highscore(path, score):
    try:
        with open(path, 'w') as f:
            f.write(str(score))
    except Exception:
        pass


def place_food(snake, height, width):
    while True:
        y = random.randint(0, height - 1)
        x = random.randint(0, width - 1)
        if (y, x) not in snake:
            return (y, x)


def run_game():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Snake Game")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    small_font = pygame.font.Font(None, 24)

    # Initial game state
    # Initial game state
    init_y = GRID_H // 2
    init_x = GRID_W // 2
    snake = [(init_y, init_x), (init_y, init_x - 1), (init_y, init_x - 2)]
    direction = (0, 1)  # moving right
    food = place_food(snake, GRID_H, GRID_W)
    score = 0
    paused = False
    game_over = False
    
    delay = INITIAL_DELAY
    last_move = pygame.time.get_ticks()
    hs_cached = load_highscore(HIGH_SCORE_FILE)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    if direction != (1, 0):
                        direction = (-1, 0)
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    if direction != (-1, 0):
                        direction = (1, 0)
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    if direction != (0, 1):
                        direction = (0, -1)
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    if direction != (0, -1):
                        direction = (0, 1)
                elif event.key == pygame.K_p:
                    paused = not paused
                elif event.key == pygame.K_r:
                    return run_game()
                elif event.key == pygame.K_q:
                    running = False

        if not paused and not game_over:
            now = pygame.time.get_ticks()
            if now - last_move >= delay:
                last_move = now
                head_y, head_x = snake[0]
                dy, dx = direction
                new_head = (head_y + dy, head_x + dx)

                # Collision checks (walls and self)
                if not (0 <= new_head[0] < GRID_H and 0 <= new_head[1] < GRID_W) or new_head in snake:
                    game_over = True
                else:
                    # Move snake
                    snake.insert(0, new_head)
                    if new_head == food:
                        score += 1
                        food = place_food(snake, GRID_H, GRID_W)
                        if score % SPEEDUP_EVERY == 0:
                            delay = max(30, int(delay * 0.9))
                    else:
                        snake.pop()

        # Draw everything
        screen.fill(BLACK)
        
        # Draw grid border
        grid_x = 20
        grid_y = 60
        grid_width = GRID_W * CELL_SIZE
        grid_height = GRID_H * CELL_SIZE
        pygame.draw.rect(screen, CYAN, (grid_x, grid_y, grid_width, grid_height), 2)

        # Draw snake
        for y, x in snake:
            pygame.draw.rect(screen, GREEN, (grid_x + x * CELL_SIZE, grid_y + y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # Draw food
        fy, fx = food
        pygame.draw.rect(screen, RED, (grid_x + fx * CELL_SIZE, grid_y + fy * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # Draw status
        current_high = load_highscore(HIGH_SCORE_FILE)
        status_text = font.render(f"Score: {score}  High: {current_high}", True, WHITE)
        screen.blit(status_text, (20, 20))

        # Draw pause text
        if paused:
            pause_text = font.render("PAUSED", True, YELLOW)
            text_rect = pause_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            screen.blit(pause_text, text_rect)

        # Draw game over text
        if game_over:
            game_over_text = font.render("GAME OVER", True, RED)
            text_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            screen.blit(game_over_text, text_rect)
            
            # Update high score if needed
            if score > hs_cached:
                save_highscore(HIGH_SCORE_FILE, score)
                hs_cached = score

        # Draw instructions
        instruction_text = small_font.render("Arrow/WASD: Move | P: Pause | R: Restart | Q: Quit", True, WHITE)
        screen.blit(instruction_text, (20, WINDOW_HEIGHT - 30))

        pygame.display.flip()
        clock.tick(60)  # 60 FPS

    pygame.quit()


def main():
    run_game()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print("Error running snake game:", e)
        sys.exit(1)
