import pygame

class Snake_Tail(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, facing, speed):
        super().__init__()
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.facing = facing
        if self.facing == "up" or self.facing == "down":
            self.image = pygame.image.load("utils/snake_tail_top_down.png").convert_alpha()
        elif self.facing == "right" or self.facing == "left":
            self.image = pygame.image.load("utils/snake_tail_left_right.png").convert_alpha()
        self.image.set_colorkey("white")
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x_pos, self.y_pos)
        self.speed = speed
    
    def get_pos(self):
        return (self.x_pos, self.y_pos)
    
    def move(self):
        if self.facing == "up":
            self.y_pos -= self.speed
            self.rect.topleft = (self.x_pos, self.y_pos)                           
        elif self.facing == "down":
            self.y_pos += self.speed
            self.rect.topleft = (self.x_pos, self.y_pos)            
        elif self.facing == "right":
            self.x_pos += self.speed
            self.rect.topleft = (self.x_pos, self.y_pos)                
        elif self.facing == "left":
            self.x_pos -= self.speed
            self.rect.topleft = (self.x_pos, self.y_pos)

    def get_direction(self):
        return self.facing
    
    def set_direction(self, facing):
        self.facing = facing
        if facing == "up" or facing == "down":
            self.image = pygame.image.load("utils/snake_tail_top_down.png").convert_alpha()
            self.image.set_colorkey("white")
        if facing == "left" or facing == "right":
            self.image = pygame.image.load("utils/snake_tail_left_right.png").convert_alpha()
            self.image.set_colorkey("white")