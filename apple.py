import pygame

class Apple(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, screen):
        super().__init__()
        self.screen = screen
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.image = pygame.image.load("utils/apple.png").convert_alpha()
        self.image.set_colorkey("white")
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x_pos, self.y_pos)
    def draw(self):
        self.screen.blit(self.image, self.rect)