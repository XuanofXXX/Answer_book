import pygame
import random
import sys
import json
import yaml

from typing import List

from src.visual_background import Line, Bubble, Drip, Flower

with open('config.yaml', 'r') as file:
    CONFIG = yaml.safe_load(file)

pygame.init()

FONT_PATH = CONFIG['font_path']
# Define text properties

# Set up the font
FONT_PATH = CONFIG['font_path']  # Use None for default font
FONT_SIZE = CONFIG['font_size']

FONT = pygame.font.Font(FONT_PATH, FONT_SIZE)
BUTTON_FONT_SIZE = CONFIG['button_font_size']
BUTTON_FONT = pygame.font.Font(FONT_PATH, BUTTON_FONT_SIZE)

# Set up the display
WIDTH, HEIGHT = CONFIG['width'], CONFIG['height']
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")

# Set up colors
BACKGROUND_COLOR = tuple(CONFIG['background_color'])
TEXT_COLOR = tuple(CONFIG['text_color'])  # Black color for text
BUTTON_COLOR = tuple(CONFIG['button_color'])  # Bright yellow for the button
BUTTON_TEXT_COLOR = tuple(CONFIG['button_text_color'])  # White for text on the button

# Control the frame rate
clock = pygame.time.Clock()

ANSWER_PATH = CONFIG['answersbook_path']
answers = []
with open(ANSWER_PATH, 'r', encoding='utf-8') as f:
    answers = json.load(f)
    answers = [value['answer'] for value in answers.values()]

lines = []

class Main_page():
    def __init__(self, original_size, scale_factor) -> None:
        r"""
        init a main page. It should be called only once

        Args:
            original_size (tuple(int, int)): original size of the screen
            scale_factor (int): scale factor for the screen, for a clear view.
        """
        self.lines: List[Line] = []
        self.main_text = FONT.render('答案之书', True, TEXT_COLOR)
        
        self.width, self.height = original_size
        
        # Define button properties
        self.button_rect = pygame.Rect(self.width // 2 - 50, self.height // 2 + 50, 100, 50)
        self.button = BUTTON_FONT.render('查看答案', True, BUTTON_TEXT_COLOR)
        
        self.original_size = original_size
        self.scale_factor = scale_factor

    def update(self):
        self.lines.append(Line(*self.original_size))
        
        if len(self.lines) > 150:
            self.lines = self.lines[len(self.lines)-150:]

    def _display_text(self, screen):
        # pygame.draw.rect(screen, button_color, button_rect)
        screen.blit(self.main_text, (self.width // 2 - self.main_text.get_width() // 2, self.height // 2 - self.main_text.get_height() // 2))
        
    def _display_button(self, screen):
        pygame.draw.rect(screen, BUTTON_COLOR, self.button_rect)
        screen.blit(self.button, (self.button_rect.x + 5, self.button_rect.y + 10))

    def show(self, screen, transition=False):
        large_size = list(map(lambda x: x*self.scale_factor, self.original_size))
        
        large_surface = pygame.Surface(large_size, pygame.SRCALPHA)
        large_surface.fill((232, 246, 252, 0))  # Use a fully transparent fill (alpha = 0)
        
        # pygame.draw.line(large_surface, self.color, self.line_pos[0][0], self.line_pos[0][1], self.width)
        for line in self.lines:
            pygame.draw.line(large_surface, line.color, line.line_pos[0], line.line_pos[1], line.width)

        # Scale down the large surface to the original size with anti-aliasing effect
        smooth_surface = pygame.transform.smoothscale(large_surface, self.original_size)
        
        # Blit the smooth surface onto the screen
        screen.blit(smooth_surface, (0, 0))
        
        
        self._display_text(screen)
        self._display_button(screen)
        
        pygame.display.flip()
        if transition:
            fade_transition(screen, 255, 0, -5, 10)  # 淡入
        # screen.blit(self.main_text, (width // 2 - self.main_text.get_width() // 2, height // 2 - self.main_text.get_height() // 2))


class Answer_page():
    def __init__(self, original_size, effect = None) -> None:
        self.original_size = original_size
        self.width, self.height = original_size
        
        self.back_button_rect = pygame.Rect(self.width // 2 - 50, self.height // 2 + 150, 100, 50)
        self.button_font = pygame.font.Font(FONT_PATH, BUTTON_FONT_SIZE)
        self.back_button_text = self.button_font.render('返回', True, BUTTON_TEXT_COLOR)
        
        self.effect = effect
        
        self.stain_surface = pygame.Surface(original_size)
        self.stain_surface.fill(BACKGROUND_COLOR)
        
        self.answer = None
        self.vs_bg = []
        
    def _display_visual_background(self, screen):
        if self.effect == None:
            self.effect = random.choice(['bubble', 'drip', 'flower'])
            
        if self.effect == 'bubble' and not self.vs_bg:
            self.vs_bg = [Bubble(*self.original_size) for _ in range(50)]
        elif self.effect == 'flower' and not self.vs_bg:
            self.vs_bg = [Flower(*self.original_size) for _ in range(100)]
        elif self.effect == 'drip' and not self.vs_bg:
            self.vs_bg = [Drip(*self.original_size) for _ in range(50)]
        
        if self.effect == 'drip':
            for bg in self.vs_bg:
                bg.show(self.stain_surface)
                bg.update()
            screen.blit(self.stain_surface, (0, 0))
            return
        
        for bg in self.vs_bg:
            bg.show(screen)
            bg.update()


    def draw_rounded_rect(self, surface, color, rect, corner_radius):
        """
        Draw a rounded rectangle on a surface.
        """
        pygame.draw.rect(surface, color, rect, border_radius=corner_radius)

    def _display_text(self, screen):
        text_width = self.answer.get_width()
        text_height = self.answer.get_height()

        # 定义背景矩形
        background_rect = pygame.Rect(
            (self.width // 2 - text_width // 2 - 20, self.height // 2 - text_height // 2 - 10),
            (text_width + 40, text_height + 20)
        )

        # 绘制圆角矩形
        self.draw_rounded_rect(screen, (255, 250, 250), background_rect, 20)

        # 绘制文字
        screen.blit(self.answer, (self.width // 2 - text_width // 2, self.height // 2 - text_height // 2))
    
    def _display_button(self, screen):
        pygame.draw.rect(screen, BUTTON_COLOR, self.back_button_rect)
        
        # 计算文字位置，使其在按钮正中间
        text_rect = self.back_button_text.get_rect(center=self.back_button_rect.center)
        
        # 在按钮矩形内绘制文字
        screen.blit(self.back_button_text, text_rect.topleft)
        
    def update(self):
        self.effect = random.choice(['bubble', 'drip', 'flower'])
        # self.effect = 'flower'
        self.vs_bg = []
        self.answer = FONT.render(random.choice(answers), True, TEXT_COLOR)
        self.stain_surface = pygame.Surface(self.original_size)
        self.stain_surface.fill(BACKGROUND_COLOR)
    
    def show(self, screen, transition=False):
        screen.fill(BACKGROUND_COLOR)
        
        self._display_visual_background(screen)
        self._display_button(screen)
        self._display_text(screen)
        
        pygame.display.flip()
        if transition:
            fade_transition(screen, 255, 0, -5, 10)  # 淡入


def fade_transition(screen, initial_alpha, final_alpha, duration):
    fade_surface = pygame.Surface((WIDTH, HEIGHT))
    fade_surface.fill(BACKGROUND_COLOR)
    for alpha in range(initial_alpha, final_alpha, int((final_alpha - initial_alpha) / duration)):
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0,0))
        pygame.display.update()
        pygame.time.delay(10)  # 控制过渡速度


current_page = 'main'  # Start on the main page
running = True
suspend = False
main_page = Main_page((WIDTH, HEIGHT), 1)
answer_page = Answer_page((WIDTH, HEIGHT))

stain_surface = pygame.Surface(screen.get_size())
stain_surface.fill(BACKGROUND_COLOR)



while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print(lines)
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if main_page.button_rect.collidepoint(event.pos) and current_page == 'main':
                fade_transition(screen, 0, 255, 30)  # 淡出
                current_page = 'answer'
                answer_page.update()
                fade_transition(screen, 255, 0, 30)  # 淡入
            elif answer_page.back_button_rect.collidepoint(event.pos) and current_page == 'answer':
                fade_transition(screen, 0, 255, 30)  # 淡出
                current_page = 'main'
                fade_transition(screen, 255, 0, 30)  # 淡入

    screen.fill(BACKGROUND_COLOR)
    
    if current_page == 'main':
        main_page.update()
        main_page.show(screen)
    elif current_page == 'answer':
        answer_page.show(screen)
    
    # pygame.display.flip()
    clock.tick(90)

pygame.quit()
sys.exit()
