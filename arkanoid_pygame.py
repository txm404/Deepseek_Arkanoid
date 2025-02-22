import pygame
import random
import json

# 游戏状态
GAME_STATE_MENU = 0
GAME_STATE_PLAYING = 1
GAME_STATE_GAME_OVER = 2
GAME_STATE_HIGH_SCORES = 3

# 颜色定义
COLORS = [
    (255, 0, 0),  # 红
    (255, 165, 0),  # 橙
    (255, 255, 0),  # 黄
    (0, 255, 0),  # 绿
    (0, 0, 255)  # 蓝
]

class Brick:
    def __init__(self, x, y, width, height, color, durability):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.durability = durability

    def draw(self, screen, font):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surface = font.render(str(self.durability), True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

class Paddle:
    def __init__(self, x, y, width, height, speed):
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = speed

    def move_left(self):
        self.rect.x = max(0, self.rect.x - self.speed)

    def move_right(self, width):
        self.rect.x = min(width - self.rect.width, self.rect.x + self.speed)

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 255, 255), self.rect)

class Ball:
    def __init__(self, x, y, size, speed_x, speed_y):
        self.rect = pygame.Rect(x, y, size, size)
        self.speed_x = speed_x
        self.speed_y = speed_y

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), self.rect)

    def bounce_x(self):
        self.speed_x *= -1

    def bounce_y(self):
        self.speed_y *= -1

class HighScoreManager:
    def __init__(self, filename="scores.txt"):
        self.filename = filename

    def load_high_scores(self):
        try:
            with open(self.filename, "r") as f:
                high_scores = json.load(f)
        except FileNotFoundError:
            high_scores = []
        return high_scores

    def save_high_score(self, name, score):
        high_scores = self.load_high_scores()
        high_scores.append({"name": name, "score": score})
        high_scores.sort(key=lambda x: x["score"], reverse=True)
        high_scores = high_scores[:10]  # Keep only top 10 scores

        with open(self.filename, "w") as f:
            json.dump(high_scores, f)
            
    def show_high_scores(self, screen, width, height):
        screen.fill((0, 0, 0))
        title_font = pygame.font.SysFont("simhei", 55)
        title_text = title_font.render("历史得分榜", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(width // 2, 100))
        screen.blit(title_text, title_rect)

        high_scores = self.load_high_scores()

        score_font = pygame.font.SysFont("simhei", 36)
        y = 200
        for i, entry in enumerate(high_scores):
            text = f"{i + 1}. {entry['name']}: {entry['score']}"
            score_text = score_font.render(text, True, (255, 255, 255))
            score_rect = score_text.get_rect(center=(width // 2, y))
            screen.blit(score_text, score_rect)
            y += 50

        back_text = score_font.render("按 B 键返回主菜单, 按 C 键清除排行榜", True, (255, 0, 0))
        back_rect = back_text.get_rect(center=(width // 2, height - 70))
        screen.blit(back_text, back_rect)

        if not high_scores:
            empty_text = score_font.render("排行榜为空", True, (255,255,255))
            empty_rect = empty_text.get_rect(center=(width//2, height//2))
            screen.blit(empty_text, empty_rect)

        pygame.display.flip()


    def clear_high_scores(self):
        with open(self.filename, "w") as f:
            json.dump([], f)
        print("High scores cleared!") # 调试语句

class Game:
    def __init__(self, width, height):
        pygame.init()
        self.width = width
        self.height = height
        self.paddle_speed = 8
        self.brick_rows = 5
        self.brick_cols = 10
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("打砖块")
        self.font = pygame.font.SysFont("simhei", 17)
        self.game_over_font = pygame.font.SysFont("simhei", 40)
        self.reset_game(reset_score=True)
        self.game_state = GAME_STATE_MENU
        self.selected_option = 0
        self.options = ["开始游戏", "退出游戏", "查看历史得分榜"]
        self.high_score_manager = HighScoreManager()


    def create_bricks(self):
        brick_width = self.width // self.brick_cols - 5
        brick_height = 15
        bricks = []
        for row in range(self.brick_rows):
            for col in range(self.brick_cols):
                brick = Brick(
                    col * (brick_width + 5) + 3,
                    row * (brick_height + 5) + 50,
                    brick_width,
                    brick_height,
                    COLORS[row],
                    row + 1
                )
                bricks.append(brick)
        return bricks

    def reset_game(self, reset_score=True):
        self.paddle = Paddle(self.width // 2 - 60, self.height - 30, 120, 10, self.paddle_speed)
        self.ball = Ball(self.width // 2 - 6, self.height - 50, 12, random.choice([-5, 5]), -5)
        self.bricks = self.create_bricks()
        if reset_score:
            self.score = 0
            self.lives = 4
        self.game_over = False

    def get_player_name(self):
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

            self.screen.fill((0, 0, 0))
            title_font = pygame.font.SysFont("simhei", 55)
            title_text = title_font.render("输入你的名字，你的分数将被记入历史得分榜", True, (255, 255, 255))
            title_rect = title_text.get_rect(center=(self.width // 2, self.height // 3))
            self.screen.blit(title_text, title_rect)

            name_font = pygame.font.SysFont("simhei", 36)
            name_text = name_font.render(name, True, (255, 255, 255))
            name_rect = name_text.get_rect(center=(self.width // 2, self.height // 2))
            self.screen.blit(name_text, name_rect)
            pygame.display.flip()
        return name

    def draw(self):
        self.screen.fill((0, 0, 0))  # 清屏为黑色

        # 绘制挡板
        self.paddle.draw(self.screen)

        # 绘制球
        self.ball.draw(self.screen)

        # 绘制砖块
        for brick in self.bricks:
            brick.draw(self.screen, self.font)

        # 显示得分和生命
        score_text = self.font.render(f"得分: {self.score}", True, (255, 255, 0))
        lives_text = self.font.render(f"生命: {self.lives}", True, (255, 255, 0))
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(lives_text, (10, 40))  # 稍微向下移动一点

        # 游戏结束提示
        if self.game_state == GAME_STATE_GAME_OVER:
            if not self.bricks:
                game_over_text = self.game_over_font.render("胜利！按 R 键返回主菜单", True, (255, 0, 0))
            else:
                game_over_text = self.game_over_font.render("游戏结束，按 R 键返回主菜单", True, (255, 0, 0))

            text_rect = game_over_text.get_rect(center=(self.width // 2, self.height // 2))
            self.screen.blit(game_over_text, text_rect)
        elif self.game_over:  # 兼容旧逻辑
            game_over_text = self.game_over_font.render("游戏结束，按 R 键重新开始", True, (255, 0, 0))
            text_rect = game_over_text.get_rect(center=(self.width // 2, self.height // 2))
            self.screen.blit(game_over_text, text_rect)

        pygame.display.flip()  # 更新屏幕

    def update(self):
        if self.game_over:
            return

        # 挡板移动
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.paddle.move_left()
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.paddle.move_right(self.width)

        # 上键加速
        if keys[pygame.K_UP]:
            self.ball.speed_y -= 1

        # 球移动
        self.ball.move()

        # 边界碰撞
        if self.ball.rect.left < 0 or self.ball.rect.right > self.width:
            self.ball.bounce_x()
        if self.ball.rect.top < 0:
            self.ball.bounce_y()

        # 底部坠落
        if self.ball.rect.bottom > self.height:
            self.lives -= 1
            if self.lives <= 0:
                self.game_over = True
                self.game_state = GAME_STATE_GAME_OVER
            else:
                self.ball.rect.center = (self.paddle.rect.centerx, self.paddle.rect.top - 10)
                self.ball.speed_y = -5
                self.ball.speed_x = random.choice([-5, 5])

        # 挡板碰撞
        if self.ball.rect.colliderect(self.paddle.rect):
            offset = (self.paddle.rect.centerx - self.ball.rect.centerx) / (self.paddle.rect.width / 2)
            self.ball.speed_x = offset * 7
            self.ball.bounce_y()
            self.ball.rect.bottom = self.paddle.rect.top

        # 砖块碰撞
        for brick in self.bricks[:]:
            if self.ball.rect.colliderect(brick.rect):
                brick.durability -= 1
                if brick.durability <= 0:
                    self.bricks.remove(brick)
                    self.score += 100
                if abs(self.ball.rect.centerx - brick.rect.centerx) > (brick.rect.width / 2 + self.ball.rect.width / 2):
                    self.ball.bounce_x()
                else:
                    self.ball.bounce_y()
                break

        if not self.bricks:
            self.game_over = True
            self.game_state = GAME_STATE_GAME_OVER

        if self.game_over:
            name = self.get_player_name()
            self.high_score_manager.save_high_score(name, self.score)

    def show_start_menu(self):
        self.screen.fill((0, 0, 0))
        title_font = pygame.font.SysFont("simhei", 72)
        title_text = title_font.render("打砖块v1.0.2", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.width // 2, self.height // 3))
        self.screen.blit(title_text, title_rect)

        instruction_font = pygame.font.SysFont("simhei", 36)

        for i, option in enumerate(self.options):
            if i == 2:  # "查看历史得分榜" 选项
                text_color = (255, 255, 255)
            else:
                text_color = (255, 255, 0) if i == self.selected_option and i == 0 else (255, 0, 0) if i == self.selected_option and i == 1 else (255, 255, 255)
            if i == self.selected_option:
                text_color = (0, 0, 255)
            text = instruction_font.render(option, True, text_color)
            text_rect = text.get_rect(center=(self.width // 2, self.height // 2 + i * 50))
            self.screen.blit(text, text_rect)

        pygame.display.flip()

    def run(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if self.game_state == GAME_STATE_MENU:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            self.selected_option = (self.selected_option - 1) % len(self.options)
                        elif event.key == pygame.K_DOWN:
                            self.selected_option = (self.selected_option + 1) % len(self.options)
                        elif event.key == pygame.K_RETURN:
                            if self.selected_option == 0:
                                self.game_state = GAME_STATE_PLAYING
                            elif self.selected_option == 1:
                                running = False
                            elif self.selected_option == 2:
                                self.game_state = GAME_STATE_HIGH_SCORES
                elif self.game_state == GAME_STATE_PLAYING:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            self.reset_game()
                            self.game_state = GAME_STATE_MENU  # 重置后返回主菜单
                elif self.game_state == GAME_STATE_HIGH_SCORES:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_b:  # B for Back
                            self.game_state = GAME_STATE_MENU
                            self.reset_game(reset_score=False)
                        elif event.key == pygame.K_c:  # C for Clear
                            self.high_score_manager.clear_high_scores()
                            print("C key pressed!")  # 调试语句
                            self.high_score_manager.show_high_scores(self.screen, self.width, self.height)  # 重新加载并显示
                elif self.game_state == GAME_STATE_GAME_OVER:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            self.reset_game(reset_score=True)
                            self.game_state = GAME_STATE_MENU

            if self.game_state == GAME_STATE_MENU:
                self.show_start_menu()
            elif self.game_state == GAME_STATE_PLAYING:
                self.update()
                self.draw()
            elif self.game_state == GAME_STATE_HIGH_SCORES:
                self.high_score_manager.show_high_scores(self.screen, self.width, self.height)

            clock.tick(75)

        pygame.quit()

if __name__ == "__main__":
    game = Game(1400, 800)
    game.run()
