from graph import Graph
from character import Character
import ui_file
import astar
import random
import pygame
import time
import queue
from collections import deque
import os

# 顏色
BLACK = (0,0,0)
GRAY = (100,100,100)
WHITE = (255,255,255)
BROWN = (139, 69, 19)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
RED = (255,0,0)
BLUE = (0,0,255)
GREEN = (0,255,0)
YELLOW = (255,255,0)

JEWEL_COLORS = [
    (255, 0, 0),    # 紅色
    (255, 165, 0),  # 橙色
    (255, 255, 0),  # 黃色
    (0, 255, 0),    # 綠色
    (0, 0, 255),    # 藍色
    (128, 0, 128)   # 紫色
]

class Character:
    def __init__(self, screen, side_length, border_width, vertices, start_point, end_point, current_point, color, bg_color):
        self.screen = screen
        self.side_length = side_length
        self.border_width = border_width
        self.vertices = vertices
        self.start_point = start_point
        self.end_point = end_point
        self.current_point = current_point
        self.bg_color = bg_color
        self.score = 0
        self.color = BROWN
        self.rainbow_mode = False
        self.last_color_change = time.time()
        self.color_index = 0

    def get_current_position(self):
        return self.current_point

    def move_character_smooth(self, next_point, steps):
        self.draw_position(self.bg_color)  # 清除前一個位置
        self.current_point = next_point
        self.draw_position()  # 在新位置繪製

    def draw_position(self, color=None):
        if color is None:
            color = self.color
        pygame.draw.rect(self.screen, color,
                        [self.border_width + (self.side_length + self.border_width) * self.current_point[0],
                         self.border_width + (self.side_length + self.border_width) * self.current_point[1],
                         self.side_length, self.side_length])

    def reached_goal(self):
        return self.current_point == self.end_point

    def update_color(self):
        if self.score >= 45:  
            self.rainbow_mode = True
            
        if self.rainbow_mode:
            current_time = time.time()
            if current_time - self.last_color_change >= 0.2:
                self.color_index = (self.color_index + 1) % len(JEWEL_COLORS)
                self.color = JEWEL_COLORS[self.color_index]
                self.last_color_change = current_time
        else:
            if self.score >= 30:
                self.color = PURPLE
            elif self.score >= 20:
                self.color = BLUE
            elif self.score >= 15:
                self.color = GRAY
            elif self.score >= 10:
                self.color = YELLOW
            elif self.score >= 5:
                self.color = (211, 211, 211)

class Jewel:
    def __init__(self, pos, screen, side_length, border_width):
        self.pos = pos
        self.screen = screen
        self.side_length = side_length
        self.border_width = border_width
        self.color_index = 0
        self.last_change = time.time()
        
    def draw(self):
        current_time = time.time()
        if current_time - self.last_change >= 0.2:
            self.color_index = (self.color_index + 1) % len(JEWEL_COLORS)
            self.last_change = current_time
            
        pygame.draw.rect(self.screen, JEWEL_COLORS[self.color_index], 
                        [self.border_width + (self.side_length + self.border_width) * self.pos[0],
                         self.border_width + (self.side_length + self.border_width) * self.pos[1],
                         self.side_length, self.side_length])

def set_window_position(x, y):
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)

def create_grid(size):
    grid = Graph()
    for i in range(size):
        for j in range(size):
            grid.add_vertex((i,j))
    return grid

def create_maze(grid, vertex, completed=None, vertices=None):
    if vertices is None:
        vertices = grid.get_vertices()
    if completed is None:
        completed = [vertex]

    paths = list(int(i) for i in range(4))
    random.shuffle(paths)

    up = (vertex[0],vertex[1]-1)
    down = (vertex[0],vertex[1]+1)
    left = (vertex[0]-1,vertex[1])
    right = (vertex[0]+1,vertex[1])

    for direction in paths:
        if direction == 0:
            if up in vertices and up not in completed:
                grid.add_edge((vertex,up))
                grid.add_edge((up,vertex))
                completed.append(up)
                create_maze(grid, up, completed, vertices)
        elif direction == 1:
            if down in vertices and down not in completed:
                grid.add_edge((vertex,down))
                grid.add_edge((down,vertex))
                completed.append(down)
                create_maze(grid, down, completed, vertices)
        elif direction == 2:
            if left in vertices and left not in completed:
                grid.add_edge((vertex,left))
                grid.add_edge((left,vertex))
                completed.append(left)
                create_maze(grid, left, completed, vertices)
        elif direction == 3:
            if right in vertices and right not in completed:
                grid.add_edge((vertex,right))
                grid.add_edge((right,vertex))
                completed.append(right)
                create_maze(grid, right, completed, vertices)

    return grid

def draw_maze(screen, maze, size, colour, side_length, border_width):
    for i in range(size):
        for j in range(size):
            if (i != 0):
                if maze.is_edge(((i,j),(i-1,j))):
                    pygame.draw.rect(screen,colour,[(side_length+border_width)*i, border_width+(side_length+border_width)*j,\
                                     side_length+border_width, side_length])
            if (i != size-1):
                if maze.is_edge(((i,j),(i+1,j))):
                    pygame.draw.rect(screen,colour,[border_width+(side_length+border_width)*i,\
                                     border_width+(side_length+border_width)*j, side_length+border_width, side_length])
            if (j != 0):
                if maze.is_edge(((i,j),(i,j-1))):
                    pygame.draw.rect(screen,colour,[border_width+(side_length+border_width)*i,\
                                     (side_length+border_width)*j, side_length, side_length+border_width])
            if (j != size-1):
                if maze.is_edge(((i,j),(i,j+1))):
                    pygame.draw.rect(screen,colour,[border_width+(side_length+border_width)*i,\
                                     border_width+(side_length+border_width)*j, side_length, side_length+border_width])

def runGame(grid_size, side_length, mode):
    pygame.init()
    
    border_width = side_length // 5
    grid = create_grid(grid_size)
    maze = create_maze(grid, (grid_size // 2, grid_size // 2))
    
    size = (grid_size * (side_length + border_width) + border_width,
            grid_size * (side_length + border_width) + border_width + 50)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("迷宮遊戲")
    
    vertices = maze.get_vertices()
    
    # 創建寶石
    jewels = []
    available_positions = [(x, y) for x in range(grid_size) for y in range(grid_size)]
    available_positions.remove((0, 0))
    available_positions.remove((grid_size - 1, grid_size - 1))
    jewel_positions = random.sample(available_positions, 45)
    
    for pos in jewel_positions:
        jewels.append(Jewel(pos, screen, side_length, border_width))
    
    player = Character(screen, side_length, border_width, vertices,
                       (0, 0), (grid_size - 1, grid_size - 1), (0, 0), BROWN, WHITE)
    
    carryOn = True
    clock = pygame.time.Clock()
    cooldown = 100
    start_timer = pygame.time.get_ticks()
    game_start_time = pygame.time.get_ticks()  # 記錄遊戲開始時間
    
    victory_time = None  # 用於記錄玩家獲勝的時間
    game_over_time = None  # 用於記錄遊戲失敗的時間
    game_won = False  # 標記玩家是否贏得了遊戲
    game_failed = False  # 標記玩家是否失敗
    
    while carryOn:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                carryOn = False
                mode = -1
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    carryOn = False
                    mode = -1
        
        keys = pygame.key.get_pressed()
        
        if pygame.time.get_ticks() - start_timer > cooldown and not game_failed:
            current_point = player.get_current_position()
            if keys[pygame.K_RIGHT]:
                if (current_point[0] + 1, current_point[1]) in vertices:
                    next_point = (current_point[0] + 1, current_point[1])
                    if maze.is_edge((current_point, next_point)):
                        player.move_character_smooth(next_point, 5)
                start_timer = pygame.time.get_ticks()
            elif keys[pygame.K_LEFT]:
                if (current_point[0] - 1, current_point[1]) in vertices:
                    next_point = (current_point[0] - 1, current_point[1])
                    if maze.is_edge((current_point, next_point)):
                        player.move_character_smooth(next_point, 5)
                start_timer = pygame.time.get_ticks()
            elif keys[pygame.K_UP]:
                if (current_point[0], current_point[1] - 1) in vertices:
                    next_point = (current_point[0], current_point[1] - 1)
                    if maze.is_edge((current_point, next_point)):
                        player.move_character_smooth(next_point, 5)
                start_timer = pygame.time.get_ticks()
            elif keys[pygame.K_DOWN]:
                if (current_point[0], current_point[1] + 1) in vertices:
                    next_point = (current_point[0], current_point[1] + 1)
                    if maze.is_edge((current_point, next_point)):
                        player.move_character_smooth(next_point, 5)
                start_timer = pygame.time.get_ticks()
        
        screen.fill(BLACK)
        draw_maze(screen, maze, grid_size, WHITE, side_length, border_width)
        
        # 繪製寶石並檢查收集
        for jewel in jewels[:]:
            if jewel.pos == player.get_current_position():
                player.score += 1
                jewels.remove(jewel)
            else:
                jewel.draw()
        
        # 更新並繪製玩家
        player.update_color()
        player.draw_position()
        
        # 繪製得分
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {player.score}/45', True, WHITE)
        screen.blit(score_text, (10, size[1] - 40))
        
        # 計算經過時間
        elapsed_time = (pygame.time.get_ticks() - game_start_time) / 1000  # 秒為單位
        
        # 顯示計時器
        if not game_failed:
            timer_text = font.render(f'Time: {elapsed_time:.1f}s', True, WHITE)
            screen.blit(timer_text, (size[0] - 150, size[1] - 40))
        
        # 檢查遊戲結束（超過時間限制）
        if elapsed_time >= 180 and not game_failed and not game_won:
            game_failed = True
            game_over_time = pygame.time.get_ticks()
        
        # 顯示 "遊戲結束" 如果超過時間限制
        if game_failed:
            game_over_text = pygame.font.Font(None, 72).render("Game Over", True, RED)
            screen.blit(game_over_text, (size[0] // 2 - game_over_text.get_width() // 2, size[1] // 2))
            pygame.display.flip()
            
            # 等待 3 秒，然後顯示失敗圖片
            if pygame.time.get_ticks() - game_over_time > 3000:
                carryOn = False
                failure_image = pygame.image.load("failure_image.png")  # 替換為失敗圖片路徑
                failure_image = pygame.transform.scale(failure_image, (size[0], size[1]))
                screen.blit(failure_image, (0, 0))
                pygame.display.flip()
                pygame.time.delay(1000)
        
        # 檢查勝利
        if player.score == 45 and not game_failed:
            game_won = True
            victory_time = pygame.time.get_ticks()  # 記錄勝利時的時間
            victory_text = pygame.font.Font(None, 72).render("Victory!", True, GREEN)
            screen.blit(victory_text, (size[0] // 2 - victory_text.get_width() // 2, size[1] // 2))
            pygame.display.flip()
            
            # 凍結計時器並退出遊戲
            pygame.time.delay(3000)  # 等待 3 秒
            carryOn = False
                
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    return mode, player.score

def main():
    set_window_position(50,50)
    grid_size = 20
    side_length = 20
    mode = 0
    runGame(grid_size, side_length, mode)

if __name__ == "__main__":
    main()
