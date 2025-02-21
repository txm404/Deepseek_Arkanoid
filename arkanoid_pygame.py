# -*- coding: utf-8 -*-
import pygame
import random

# 初始化 Pygame
pygame.init()

# 游戏配置
WIDTH = 1400
HEIGHT = 800
PADDLE_SPEED = 8
BRICK_ROWS = 5
BRICK_COLS = 10
FONT_NAME = "msyh"  # 假设 msyh.ttc 在同一目录或系统字体目录中

# 颜色定义
COLORS = [
    (255, 0, 0),    # 红
    (255, 165, 0),  # 橙
    (255, 255, 0),  # 黄
    (0, 255, 0),    # 绿
    (0, 0, 255)     # 蓝
]

# 设置窗口
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Arkanoid")

# 加载字体 (如果字体文件在同一目录，可以直接使用文件名)
font = pygame.font.SysFont("simhei", 17)
game_over_font = pygame.font.SysFont("simhei", 40)

# 游戏对象
paddle = pygame.Rect(WIDTH // 2 - 60, HEIGHT - 30, 120, 10)
ball = pygame.Rect(WIDTH // 2 - 6, HEIGHT - 50, 12, 12)
ball_speed_x = random.choice([-5, 5])
ball_speed_y = -5
bricks = []
score = 0
lives = 4
game_over = False

def create_bricks():
    brick_width = WIDTH // BRICK_COLS - 5
    brick_height = 15
    for row in range(BRICK_ROWS):
        for col in range(BRICK_COLS):
            brick = pygame.Rect(
                col * (brick_width + 5) + 3,
                row * (brick_height + 5) + 50,
                brick_width,
                brick_height
            )
            bricks.append({
                "rect": brick,
                "color": COLORS[row],
                "durability": row + 1
            })

create_bricks()

def reset_game():
    global paddle, ball, bricks, game_over, score, lives, ball_speed_x, ball_speed_y
    paddle = pygame.Rect(WIDTH // 2 - 60, HEIGHT - 30, 120, 10)
    ball = pygame.Rect(WIDTH // 2 - 6, HEIGHT - 50, 12, 12)
    ball_speed_x = random.choice([-5, 5])
    ball_speed_y = -5
    bricks.clear()  # 清空列表
    create_bricks()
    score = 0
    lives = 4
    game_over = False

def draw():
    screen.fill((0, 0, 0))  # 清屏为黑色

    # 绘制挡板
    pygame.draw.rect(screen, (0, 255, 255), paddle)

    # 绘制球
    pygame.draw.rect(screen, (255, 255, 255), ball)

    # 绘制砖块
    for brick in bricks:
        pygame.draw.rect(screen, brick["color"], brick["rect"])
        text_surface = font.render(str(brick["durability"]), True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=brick["rect"].center)
        screen.blit(text_surface, text_rect)

    # 显示得分和生命
    score_text = font.render(f"得分: {score}", True, (255, 255, 0))
    lives_text = font.render(f"生命: {lives}", True, (255, 255, 0))
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (10, 40))  # 稍微向下移动一点

    # 游戏结束提示
    if game_over:
        if not bricks:
            game_over_text = game_over_font.render("胜利！", True, (255, 0, 0))
        else:
            game_over_text = game_over_font.render("游戏结束，按 R 键重新开始", True, (255, 0, 0))

        text_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(game_over_text, text_rect)


    pygame.display.flip()  # 更新屏幕


def update():
    global game_over, lives, ball_speed_x, ball_speed_y, score

    if game_over:
        return

    # 挡板移动
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        paddle.x = max(0, paddle.x - PADDLE_SPEED)
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        paddle.x = min(WIDTH - paddle.width, paddle.x + PADDLE_SPEED)

    # 上键加速
    if keys[pygame.K_UP]:
        ball_speed_y -= 1

    # 球移动
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # 边界碰撞
    if ball.left < 0 or ball.right > WIDTH:
        ball_speed_x *= -1
    if ball.top < 0:
        ball_speed_y *= -1

    # 底部坠落
    if ball.bottom > HEIGHT:
        lives -= 1
        if lives <= 0:
            game_over = True
        else:
            ball.center = (paddle.centerx, paddle.top - 10)
            ball_speed_y = -5
            ball_speed_x = random.choice([-5, 5])

    # 挡板碰撞
    if ball.colliderect(paddle):
        offset = (paddle.centerx - ball.centerx) / (paddle.width / 2)
        ball_speed_x = offset * 7
        ball_speed_y *= -1
        ball.bottom = paddle.top

    # 砖块碰撞
    for brick in bricks[:]:
        if ball.colliderect(brick["rect"]):
            brick["durability"] -= 1
            if brick["durability"] <= 0:
                bricks.remove(brick)
                score += 100
            if abs(ball.centerx - brick["rect"].centerx) > (brick["rect"].width / 2 + ball.width / 2):
                ball_speed_x *= -1
            else:
                ball_speed_y *= -1
            break

    if not bricks:
        game_over = True

# 游戏循环
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                reset_game()

    update()
    draw()
    clock.tick(75)  # 限制帧率为 60 FPS

pygame.quit()