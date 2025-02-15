import pgzrun
from random import choice

# == 游戏配置 ==
WIDTH = 800     # 窗口宽度
HEIGHT = 600    # 窗口高度
PADDLE_SPEED = 8  # 挡板移动速度
BRICK_ROWS = 5  # 砖块行数
BRICK_COLS = 10 # 砖块列数
score = 0       # 明确全局分数
lives = 4       # 生命值
game_over = False
bricks = []     # 存储砖块
ball_speed_x = 0
ball_speed_y = 0
# == 颜色定义 ==
COLORS = [
    (255, 0, 0),    # 红
    (255, 165, 0),  # 橙
    (255, 255, 0),  # 黄
    (0, 255, 0),    # 绿
    (0, 0, 255)     # 蓝
]

# == 游戏对象初始化 ==
def reset_game():
    global paddle, ball, bricks, game_over
    global score, lives, ball_speed_x, ball_speed_y
    score = 0 
    lives = 4
    # 挡板初始位置
    paddle = Rect((WIDTH/2-60, HEIGHT-30), (120, 10))
    
    # 球初始状态
    ball = Rect((WIDTH/2-6, HEIGHT-50), (12, 12))
    ball_speed_x = choice([-5, 5])  # 随机初始横向速度
    ball_speed_y = -5               # 垂直速度
    
    # 砖块生成（带颜色和耐久度）
    bricks = []
    brick_width = WIDTH // BRICK_COLS - 5
    brick_height = 15
    for row in range(BRICK_ROWS):
        for col in range(BRICK_COLS):
            brick = Rect(
                (col*(brick_width+5)+3, row*(brick_height+5)+50),
                (brick_width, brick_height)
            )
            bricks.append({
                "rect": brick,
                "color": COLORS[row],
                "durability": row+1  # 耐久度随行数增加
            })
    
    # 游戏状态
    game_over = False
    score = 0
    lives = 1
ball_speed_x = 0  # 初始值
ball_speed_y = 0  # 初始值
reset_game()  # 初始化游戏

# == 游戏绘制 ==
def draw():
    FONT_NAME = "simhei.ttf"
    screen.clear()
    # 绘制挡板（青色）
    screen.draw.filled_rect(paddle, (0, 255, 255))
    
    # 绘制球（白色）
    screen.draw.filled_rect(ball, (255, 255, 255))
    
    # 绘制砖块（带耐久度显示）
    for brick in bricks:
        screen.draw.filled_rect(brick["rect"], brick["color"])
        # 显示耐久度（数字居中）
        screen.draw.text(
            str(brick["durability"]),
            center=brick["rect"].center,
            color=(0,0,0)
        )
    
    # 显示得分和生命（左上角）
    screen.draw.text(
        f"socre: {score}\nlives: {lives}",
        topleft=(10, 10),
        fontsize=30,
        color=(255,255,0)
    )
    
    # 游戏结束提示（中英双语）
    if game_over:
        screen.draw.text(
            "victory!" if not bricks else "Game Over, type R to restart",
            center=(WIDTH//2, HEIGHT//2),
            fontsize=60,
            color=(255,0,0)
        )

# == 游戏逻辑更新 ==
def update():
    global game_over, lives
    global ball_speed_x, ball_speed_y
    global score  
    if game_over: return
    
    # 挡板移动控制（支持方向键和A/D键）
    if keyboard.left or keyboard.a:
        paddle.x = max(0, paddle.x - PADDLE_SPEED)
    if keyboard.right or keyboard.d:
        paddle.x = min(WIDTH - paddle.width, paddle.x + PADDLE_SPEED)
    
    # 球移动
    ball.x += ball_speed_x
    ball.y += ball_speed_y
    
    # 边界碰撞检测
    if ball.left < 0 or ball.right > WIDTH:
        ball_speed_x *= -1
    if ball.top < 0:
        ball_speed_y *= -1
        
    # 底部坠落检测
    if ball.bottom > HEIGHT:
        lives -= 1
        if lives <= 0:
            game_over = True
        else:
            ball.center = (paddle.centerx, paddle.top - 10)
            ball_speed_y = -5
            ball_speed_x = choice([-5, 5])
    
    # 挡板碰撞检测（反弹角度变化）
    if ball.colliderect(paddle):
        offset = (paddle.centerx - ball.centerx) / (paddle.width/2)
        ball_speed_x = offset * 7  # 根据接触位置改变横向速度
        ball_speed_y *= -1
        ball.bottom = paddle.top  # 防止穿透
    
    # 砖块碰撞检测
    for brick in bricks[:]:  # 遍历副本以便删除
        if ball.colliderect(brick["rect"]):
            # 减少砖块耐久
            brick["durability"] -= 1
            if brick["durability"] <= 0:
                bricks.remove(brick)
                score += 100
            # 根据碰撞位置反弹
            ball_dx = ball_speed_x
            ball_dy = ball_speed_y
            if abs(ball.centerx - brick["rect"].centerx) > (brick["rect"].width/2 + ball.width/2):
                ball_speed_x *= -1  # 左右碰撞
            else:
                ball_speed_y *= -1  # 上下碰撞
            break  # 一次帧只处理一个碰撞
    
    # 胜利判断
    if not bricks:
        game_over = True

# == 按键控制 ==
def on_key_down(key):
    # 重新开始游戏
    if key == keys.R:
        reset_game()

pgzrun.go()  # 启动游戏
