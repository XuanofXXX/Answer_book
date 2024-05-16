import pygame
import random

# 定义 Bubble 类
class Bubble:
    def __init__(self, screen_width, screen_height):
        self.x = random.randint(0, screen_width)
        # self.y = random.randint(screen_height-200, screen_height)  # 初始 y 坐标设为屏幕底部附近
        self.y = random.randint(0, screen_height)  # 初始 y 坐标设为屏幕底部附近
        self.active = True
        self.color = (random.randint(200, 255), random.randint(200, 255), random.randint(200, 255))
        self.r = random.randint(30, 80)
        self.speed = random.uniform(1, 3)
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.alpha = random.randint(0, 255) 

    def update(self):
        if self.active:
            self.y -= self.speed
            if self.y < 0:
                self.x = random.randint(0, self.screen_width)
                self.y = random.randint(self.screen_height-200, self.screen_height)

    def show(self, screen):
        if self.active:
            temp_surface = pygame.Surface((self.r*2, self.r*2), pygame.SRCALPHA)  # 创建一个新的Surface对象
            pygame.draw.circle(temp_surface, self.color + (self.alpha,), (self.r, self.r), self.r)  # 在新的Surface对象上绘制圆形
            screen.blit(temp_surface, (self.x-self.r, self.y-self.r))  # 将新的Surface对象绘制到屏幕上

# 定义 Drip 类
class Drip:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.begin_x = random.randint(0, self.screen_width)
        self.begin_y = random.randint(0, int(self.screen_height * 0.3))
        self.x = self.begin_x
        self.y = self.begin_y
        self.r = random.randint(10, 50)
        self.active = True
        self.color = (random.randint(200, 255), random.randint(200, 255), random.randint(200, 255))
        self.speed = random.uniform(1, 3)
        self.time_tick = 0
        self.alpha = random.randint(0, 255) 

    def update(self):
        self.y += self.speed
        self.time_tick += 1
        if self.y > self.screen_height:
            self.x = random.randint(0, self.screen_width)
            self.y = random.randint(0, int(self.screen_height * 0.3))
            self.time_tick = 0

    def show(self, screen):
        if self.active:
            temp_surface = pygame.Surface((self.r*2, self.r*2), pygame.SRCALPHA)  # 创建一个新的Surface对象
            temp_surface.fill((0, 0, 0, 0))  # 设置背景为完全透明
            pygame.draw.circle(temp_surface, self.color + (self.alpha,), (self.r, self.r), self.r)  # 在新的Surface对象上绘制圆形
            screen.blit(temp_surface, (self.x-self.r, self.y-self.r))  # 将新的Surface对象绘制到屏幕上


# 定义 Flower 类
class Flower:
    def __init__(self, screen_width, screen_height):
        self.r = random.randint(15, 50)
        self.x = random.randint(0, screen_width)
        self.y = random.randint(0, screen_height)
        self.active = True
        self.color = (random.randint(200, 255), random.randint(200, 255), random.randint(200, 255), random.randint(200, 220))
        self.center_color = (random.randint(230, 255), random.randint(220, 225), random.randint(105, 115), 150)
        self.speed = random.uniform(1, 3)
        self.angle = 0
        self.screen_width = screen_width
        self.screen_height = screen_height

    def update(self):
        # if self.y < 0:
        #     self.x = random.randint(0, self.screen_width)
        #     self.y = self.screen_height + self.r
        # self.y -= self.speed
        # self.angle += 0.01
        self.y -= self.speed
        self.angle += 0.5
        if self.y < -self.r * 2:
            self.y = self.screen_height + self.r * 2
            self.x = random.randint(0, self.screen_width)

    def show(self, screen):
        # 启用透明度支持
        
        flower_surf = pygame.Surface((self.r * 4, self.r * 4), pygame.SRCALPHA)
        
        # 绘制花瓣
        pygame.draw.ellipse(flower_surf, self.color, (self.r, 0, self.r * 2, self.r))
        pygame.draw.ellipse(flower_surf, self.color, (self.r, self.r * 3, self.r * 2, self.r))
        pygame.draw.ellipse(flower_surf, self.color, (0, self.r, self.r, self.r * 2))
        pygame.draw.ellipse(flower_surf, self.color, (self.r * 3, self.r, self.r, self.r * 2))

        # 绘制中心点
        pygame.draw.circle(flower_surf, self.center_color, (self.r * 2, self.r * 2), self.r)
        
        # 旋转花朵
        rotated_surf = pygame.transform.rotate(flower_surf, self.angle)
        rect = rotated_surf.get_rect(center=(self.x, self.y))
        
        screen.blit(rotated_surf, rect.topleft)

        # flower_surf = pygame.transform.rotate(flower_surf, self.angle)
        # screen.blit(flower_surf, (self.x - self.r * 2, self.y - self.r * 2))


class Line():
    def __init__(self, screen_width,
                 screen_height,
                 screen_width_offset_co = 0.1,
                 screen_height_offset_co = 0.1,
                 line_width = None) -> None:
        """
        Generate a line with given the screen_size, width and random color.
        This line will be around the window.
        
        Returns:
            None
        """
        if line_width is None:
            self.width = random.randint(1, 3)
        
        self.screen_width = screen_width
        self.screen_height = screen_height
        

        self.screen_width_offset = int(screen_width * screen_width_offset_co)
        self.screen_height_offset = int(screen_height * screen_height_offset_co)
        
        self.color = (random.randint(200, 255), random.randint(200, 255), random.randint(200, 255), random.randint(150, 200))
        
        self.line_pos = random.choice([
            ((random.randint(0, self.screen_width_offset), random.randint(0, self.screen_height)), (random.randint(0, self.screen_width_offset), random.randint(0, self.screen_height))),
            ((random.randint(self.screen_width - self.screen_width_offset, self.screen_width), random.randint(0, self.screen_height)), (random.randint(self.screen_width - self.screen_width_offset, self.screen_width), random.randint(0, self.screen_height))),
            ((random.randint(0, self.screen_width), random.randint(0, self.screen_height_offset)), (random.randint(0, self.screen_width), random.randint(0, self.screen_height_offset))),
            ((random.randint(0, self.screen_width), random.randint(self.screen_height - self.screen_height_offset, self.screen_height)), (random.randint(0, self.screen_width), random.randint(self.screen_height - self.screen_height_offset, self.screen_height))),
        ])
        
        
    def update(self):
        pass
    
    def show(screen):
        pass