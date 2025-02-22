# -*- coding: utf-8 -*-
import pygame
import random
import json

# 游戏状态
GAME_STATE_MENU = 0
GAME_STATE_PLAYING = 1
GAME_STATE_GAME_OVER = 2
GAME_STATE_HIGH_SCORES = 3

# 初始化 Pygame
pygame.init()

# 游戏配置
WIDTH = 1400
HEIGHT = 800
PADDLE_SPEED = 8
BRICK_ROWS = 5
BRICK_COLS = 10
FONT_NAME = "simhei.ttc"  # 假设 simhei.ttc 在同一目录或系统字体目录中

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
pygame.display.set_caption("打砖块")

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
game_state = GAME_STATE_MENU  # 初始状态为菜单

def show_start_menu(selected_option):
    screen.fill((0, 0, 0))
    title_font = pygame.font.SysFont("simhei", 72)  # 使用 Font 加载字体文件
    title_text = title_font.render("打砖块v1.0.1", True, (255, 255, 255)) # 使用中文
    title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
    screen.blit(title_text, title_rect)

    instruction_font = pygame.font.SysFont("simhei", 36) # 使用 Font 加载字体文件
    options = ["开始游戏", "退出游戏", "查看历史得分榜"]

    for i, option in enumerate(options):
        if i == 2:  # "查看历史得分榜" 选项
            text_color = (255, 255, 255)  # 蓝色
        else:
            text_color = (255, 255, 0) if i == selected_option and i == 0 else (255, 0, 0) if i == selected_option and i == 1 else (255, 255, 255)
        if i == selected_option:
            text_color = (0, 0, 255)
        text = instruction_font.render(option, True, text_color)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + i * 50))
        screen.blit(text, text_rect)

    pygame.display.flip()

def load_high_scores():
    try:
        with open("scores.txt", "r") as f:
            high_scores = json.load(f)
    except FileNotFoundError:
        high_scores = []
    return high_scores

def save_high_score(name, score):
    high_scores = load_high_scores()
    high_scores.append({"name": name, "score": score})
    high_scores.sort(key=lambda x: x["score"], reverse=True)
    high_scores = high_scores[:10]  # Keep only top 10 scores

    with open("scores.txt", "w") as f:
        json.dump(high_scores, f)

def show_high_scores():
    screen.fill((0, 0, 0))
    title_font = pygame.font.SysFont("simhei", 55)
    title_text = title_font.render("历史得分榜", True, (255, 255, 255)) # 蓝色
    title_rect = title_text.get_rect(center=(WIDTH // 2, 100))
    screen.blit(title_text, title_rect)

    high_scores = load_high_scores()

    score_font = pygame.font.SysFont("simhei", 36)
    y = 200
    for i, entry in enumerate(high_scores):
        text = f"{i + 1}. {entry['name']}: {entry['score']}"
        score_text = score_font.render(text, True, (255, 255, 255)) # 蓝色
        score_rect = score_text.get_rect(center=(WIDTH // 2, y))
        screen.blit(score_text, score_rect)
        y += 50

    back_text = score_font.render("按 B 键返回主菜单", True, (255, 0, 0))
    back_rect = back_text.get_rect(center=(WIDTH // 2, HEIGHT - 70))
    screen.blit(back_text, back_rect)


    pygame.display.flip()

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

def reset_game(reset_score=True):
    global paddle, ball, bricks, game_over, score, lives, ball_speed_x, ball_speed_y
    paddle = pygame.Rect(WIDTH // 2 - 60, HEIGHT - 30, 120, 10)
    ball = pygame.Rect(WIDTH // 2 - 6, HEIGHT - 50, 12, 12)
    ball_speed_x = random.choice([-5, 5])
    ball_speed_y = -5
    bricks.clear()  # 清空列表
    create_bricks()
    if reset_score:
        score = 0
        lives = 4
    game_over = False

def get_player_name():
    name = ""
    input_active = True
    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    name += event.unicode

        screen.fill((0, 0, 0))
        title_font = pygame.font.SysFont("simhei", 55)
        title_text = title_font.render("输入你的名字，你的分数将被记入历史得分榜", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
        screen.blit(title_text, title_rect)

        name_font = pygame.font.SysFont("simhei", 36)
        name_text = name_font.render(name, True, (255, 255, 255))
        name_rect = name_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(name_text, name_rect)
        pygame.display.flip()
    return name

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
    if game_state == GAME_STATE_GAME_OVER:
        if not bricks:
            game_over_text = game_over_font.render("胜利！", True, (255, 0, 0))
        else:
            game_over_text = game_over_font.render("游戏结束，按 R 键返回主菜单", True, (255, 0, 0))

        text_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(game_over_text, text_rect)
    elif game_over: # 兼容旧逻辑
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
            game_state = GAME_STATE_GAME_OVER
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
        game_state = GAME_STATE_GAME_OVER

    if game_over:
        name = get_player_name()
        save_high_score(name, score)

# 游戏循环
clock = pygame.time.Clock()
running = True
options = ["开始游戏", "退出游戏", "查看历史得分榜"]
selected_option = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_state == GAME_STATE_MENU:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if selected_option == 0:
                        game_state = GAME_STATE_PLAYING
                    elif selected_option == 1:
                        running = False
                    elif selected_option == 2:
                        game_state = GAME_STATE_HIGH_SCORES
        elif game_state == GAME_STATE_PLAYING:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_game()
                    game_state = GAME_STATE_MENU  # 重置后返回菜单
        elif game_state == GAME_STATE_HIGH_SCORES:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:  # B for Back
                    game_state = GAME_STATE_MENU
                    reset_game(reset_score=False)

    if game_state == GAME_STATE_MENU:
        show_start_menu(selected_option)
    elif game_state == GAME_STATE_PLAYING:
        update()
        draw()
    elif game_state == GAME_STATE_HIGH_SCORES:
        show_high_scores()

    clock.tick(75)

pygame.quit()