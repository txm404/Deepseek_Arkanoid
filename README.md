arkanoid_pygame.py - 简单的打砖块游戏

这是一个使用 Pygame 库创建的经典打砖块游戏的简单实现。
玩家控制一个挡板来反弹小球，击碎屏幕上方的砖块。

**文件结构:**

*   arkanoid_pygame.py (本文件): 包含游戏的所有代码。

**依赖:**

*   Pygame: 用于游戏开发的 Python 库。
    您可以使用 pip 安装 Pygame: `pip install pygame`

**如何运行:**

1.  确保您已经安装了 Python 和 Pygame。
2.  保存此文件为 `arkanoid_pygame.py`。
3.  在命令行或终端中，导航到文件所在的目录。
4.  运行命令: `python arkanoid_pygame.py`

**游戏控制:**

*   **左方向键 或 A 键:**  向左移动挡板。
*   **右方向键 或 D 键:**  向右移动挡板。
*   **上方向键:**  增加球的垂直速度 (加速球)。
*   **R 键:**  在游戏结束时，重新开始游戏。

**代码概览:**

*   **初始化 Pygame:**  设置 Pygame 库。
*   **游戏配置:**  定义游戏窗口尺寸、挡板速度、砖块布局、颜色和字体等常量。
*   **颜色定义:**  预定义游戏中使用的颜色。
*   **设置窗口:**  创建游戏窗口并设置标题。
*   **加载字体:**  加载用于显示得分、生命和游戏结束信息的字体。
*   **游戏对象:**  创建和初始化游戏中的主要对象，包括挡板、球和砖块。
*   **`create_bricks()` 函数:**  生成砖块的布局。
*   **`reset_game()` 函数:**  重置游戏状态，开始新游戏。
*   **`draw()` 函数:**  绘制游戏的所有元素到屏幕上。
*   **`update()` 函数:**  更新游戏逻辑，包括移动物体、碰撞检测、得分和生命管理。
*   **游戏循环:**  主游戏循环，处理事件、更新游戏状态和绘制画面。

**详细代码注释请参考代码内部注释。**
"""
import pygame
import random

# 初始化 Pygame
pygame.init()

# 游戏配置
WIDTH = 1400  # 窗口宽度
HEIGHT = 800 # 窗口高度
PADDLE_SPEED = 8 # 挡板移动速度
BRICK_ROWS = 5  # 砖块行数
BRICK_COLS = 10 # 砖块列数
FONT_NAME = "msyh"  # 字体名称 (假设 msyh.ttc 在同一目录或系统字体目录中)

# 颜色定义
COLORS = [
    (255, 0, 0),    # 红
    (255, 165, 0),  # 橙
    (255, 255, 0),  # 黄
    (0, 255, 0),    # 绿
    (0, 0, 255)     # 蓝
]

# 设置窗口
screen = pygame.display.set_mode((WIDTH, HEIGHT)) # 创建游戏窗口
pygame.display.set_caption("Arkanoid") # 设置窗口标题

# 加载字体 (如果字体文件在同一目录，可以直接使用文件名)
font = pygame.font.SysFont("simhei", 17) # 加载普通字体，用于显示得分和生命
game_over_font = pygame.font.SysFont("simhei", 40) # 加载较大字体，用于显示游戏结束信息

# 游戏对象
paddle = pygame.Rect(WIDTH // 2 - 60, HEIGHT - 30, 120, 10) # 挡板矩形对象 (x, y, width, height)
ball = pygame.Rect(WIDTH // 2 - 6, HEIGHT - 50, 12, 12) # 球矩形对象
ball_speed_x = random.choice([-5, 5]) # 球的水平速度，随机选择向左或向右
ball_speed_y = -5 # 球的垂直速度，向上
bricks = [] # 存储砖块信息的列表
score = 0 # 玩家得分
lives = 4 # 玩家生命数
game_over = False # 游戏结束标志

def create_bricks():
    """
    创建砖块布局。
    根据 BRICK_ROWS 和 BRICK_COLS 常量生成砖块，并设置颜色和耐久度。
    """
    brick_width = WIDTH // BRICK_COLS - 5 # 计算砖块宽度，减去间距
    brick_height = 15 # 砖块高度
    for row in range(BRICK_ROWS): # 遍历每一行
        for col in range(BRICK_COLS): # 遍历每一列
            brick = pygame.Rect(
                col * (brick_width + 5) + 3, # 计算砖块的 x 坐标，加上间距和偏移
                row * (brick_height + 5) + 50, # 计算砖块的 y 坐标，加上间距和偏移
                brick_width, # 砖块宽度
                brick_height # 砖块高度
            )
            bricks.append({ # 将砖块信息添加到 bricks 列表
                "rect": brick, # 砖块的矩形对象
                "color": COLORS[row], # 砖块的颜色，根据行数选择颜色
                "durability": row + 1 # 砖块的耐久度，等于行数 + 1
            })

create_bricks() # 调用函数创建初始砖块布局

def reset_game():
    """
    重置游戏状态，开始新游戏。
    重置挡板、球、砖块、得分、生命和游戏结束标志。
    """
    global paddle, ball, bricks, game_over, score, lives, ball_speed_x, ball_speed_y # 声明全局变量
    paddle = pygame.Rect(WIDTH // 2 - 60, HEIGHT - 30, 120, 10) # 重置挡板位置
    ball = pygame.Rect(WIDTH // 2 - 6, HEIGHT - 50, 12, 12) # 重置球位置
    ball_speed_x = random.choice([-5, 5]) # 重置球的水平速度
    ball_speed_y = -5 # 重置球的垂直速度
    bricks.clear()  # 清空砖块列表
    create_bricks() # 重新创建砖块
    score = 0 # 重置得分
    lives = 4 # 重置生命数
    game_over = False # 重置游戏结束标志

def draw():
    """
    绘制游戏的所有元素到屏幕上。
    包括背景、挡板、球、砖块、得分、生命和游戏结束提示。
    """
    screen.fill((0, 0, 0))  # 清屏为黑色背景

    # 绘制挡板
    pygame.draw.rect(screen, (0, 255, 255), paddle) # 绘制青色挡板

    # 绘制球
    pygame.draw.rect(screen, (255, 255, 255), ball) # 绘制白色球

    # 绘制砖块
    for brick in bricks: # 遍历砖块列表
        pygame.draw.rect(screen, brick["color"], brick["rect"]) # 绘制砖块，颜色从砖块信息中获取
        text_surface = font.render(str(brick["durability"]), True, (0, 0, 0)) # 创建耐久度文本表面
        text_rect = text_surface.get_rect(center=brick["rect"].center) # 获取文本矩形，并设置中心为砖块中心
        screen.blit(text_surface, text_rect) # 绘制耐久度文本到砖块中心

    # 显示得分和生命
    score_text = font.render(f"得分: {score}", True, (255, 255, 0)) # 创建得分文本表面
    lives_text = font.render(f"生命: {lives}", True, (255, 255, 0)) # 创建生命文本表面
    screen.blit(score_text, (10, 10)) # 绘制得分文本到屏幕左上角
    screen.blit(lives_text, (10, 40))  # 绘制生命文本到得分文本下方

    # 游戏结束提示
    if game_over: # 如果游戏结束
        if not bricks: # 如果砖块全部消除，则胜利
            game_over_text = game_over_font.render("胜利！", True, (255, 0, 0)) # 创建胜利文本
        else: # 否则，游戏失败
            game_over_text = game_over_font.render("游戏结束，按 R 键重新开始", True, (255, 0, 0)) # 创建游戏结束文本

        text_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2)) # 获取文本矩形，并设置中心为屏幕中心
        screen.blit(game_over_text, text_rect) # 绘制游戏结束文本到屏幕中心


    pygame.display.flip()  # 更新屏幕显示，将绘制内容显示出来


def update():
    """
    更新游戏逻辑。
    包括挡板移动、球移动、边界碰撞检测、挡板碰撞检测、砖块碰撞检测、得分和生命管理、游戏结束判断。
    """
    global game_over, lives, ball_speed_x, ball_speed_y, score # 声明全局变量

    if game_over: # 如果游戏已经结束，则不进行更新
        return

    # 挡板移动
    keys = pygame.key.get_pressed() # 获取当前按键状态
    if keys[pygame.K_LEFT] or keys[pygame.K_a]: # 如果按下左方向键或 A 键
        paddle.x = max(0, paddle.x - PADDLE_SPEED) # 向左移动挡板，并限制挡板不出左边界
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]: # 如果按下右方向键或 D 键
        paddle.x = min(WIDTH - paddle.width, paddle.x + PADDLE_SPEED) # 向右移动挡板，并限制挡板不出右边界

    # 上键加速 (调试或作弊用)
    if keys[pygame.K_UP]: # 如果按下上方向键
        ball_speed_y -= 1 # 增加球的垂直速度，使其更快

    # 球移动
    ball.x += ball_speed_x # 更新球的 x 坐标
    ball.y += ball_speed_y # 更新球的 y 坐标

    # 边界碰撞检测
    if ball.left < 0 or ball.right > WIDTH: # 如果球碰到左右边界
        ball_speed_x *= -1 # 水平速度反向，实现反弹
    if ball.top < 0: # 如果球碰到上边界
        ball_speed_y *= -1 # 垂直速度反向，实现反弹

    # 底部坠落检测
    if ball.bottom > HEIGHT: # 如果球超出下边界
        lives -= 1 # 生命数减 1
        if lives <= 0: # 如果生命数小于等于 0
            game_over = True # 设置游戏结束标志
        else: # 如果生命数大于 0，则重置球的位置和速度
            ball.center = (paddle.centerx, paddle.top - 10) # 将球放置在挡板上方
            ball_speed_y = -5 # 重置球的垂直速度
            ball_speed_x = random.choice([-5, 5]) # 随机重置球的水平速度

    # 挡板碰撞检测
    if ball.colliderect(paddle): # 如果球和挡板发生碰撞
        offset = (paddle.centerx - ball.centerx) / (paddle.width / 2) # 计算球与挡板中心的偏移量，范围 -1 到 1
        ball_speed_x = offset * 7 # 根据偏移量设置球的水平速度，使球反弹方向更自然
        ball_speed_y *= -1 # 垂直速度反向，实现反弹
        ball.bottom = paddle.top # 将球底部对齐到挡板顶部，防止球陷入挡板内部

    # 砖块碰撞检测
    for brick in bricks[:]: # 遍历砖块列表的副本，以便在循环中删除砖块
        if ball.colliderect(brick["rect"]): # 如果球和砖块发生碰撞
            brick["durability"] -= 1 # 砖块耐久度减 1
            if brick["durability"] <= 0: # 如果砖块耐久度小于等于 0
                bricks.remove(brick) # 从砖块列表中移除砖块
                score += 100 # 得分增加 100
            # 根据碰撞位置判断反弹方向，避免球卡在砖块中
            if abs(ball.centerx - brick["rect"].centerx) > (brick["rect"].width / 2 + ball.width / 2): # 如果球的中心 x 坐标与砖块中心 x 坐标的距离大于砖块宽度一半加上球宽度一半，说明是水平方向碰撞
                ball_speed_x *= -1 # 水平速度反向
            else: # 否则是垂直方向碰撞
                ball_speed_y *= -1 # 垂直速度反向
            break # 每次只处理一个砖块的碰撞，避免一次碰撞消除多个砖块的问题

    if not bricks: # 如果砖块列表为空，说明所有砖块都被消除
        game_over = True # 设置游戏结束标志，表示胜利

# 游戏循环
clock = pygame.time.Clock() # 创建游戏时钟对象，用于控制帧率
running = True # 游戏运行标志
while running: # 主游戏循环
    for event in pygame.event.get(): # 获取事件队列中的所有事件
        if event.type == pygame.QUIT: # 如果事件类型是退出
            running = False # 设置游戏运行标志为 False，退出游戏循环
        if event.type == pygame.KEYDOWN: # 如果事件类型是按键按下
            if event.key == pygame.K_r: # 如果按下的键是 R 键
                reset_game() # 重置游戏状态，重新开始游戏

    update() # 更新游戏逻辑
    draw() # 绘制游戏画面
    clock.tick(75)  # 控制游戏帧率为 75 FPS (帧每秒)

pygame.quit() # 退出 Pygame

### (此项目由deepseek生成)
