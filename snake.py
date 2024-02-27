import pygame
from tail import Snake_Tail

class Snake_Head(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, screen):
        super().__init__()
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.tails = pygame.sprite.Group()
        self.facing = "up"
        self.image = pygame.image.load(f"utils/snake_head_{self.facing}.png").convert_alpha()
        self.image.set_colorkey("white")
        self.rect = self.image.get_rect()
        self.rect.topleft = (x_pos, y_pos)
        self.screen = screen
        self.speed = 5
    def add_tail(self):
        if self.tails.sprites() == []:
            if self.facing == "up":            
                self.tails.add(Snake_Tail(self.x_pos, self.y_pos + 25, "up", self.speed))
            
            elif self.facing == "down":
                self.tails.add(Snake_Tail(self.x_pos, self.y_pos - 25, "down", self.speed))
            elif self.facing == "right":            
                self.tails.add(Snake_Tail(self.x_pos - 25, self.y_pos, "right", self.speed))
            elif self.facing == "left":        
                self.tails.add(Snake_Tail(self.x_pos + 25, self.y_pos, "left", self.speed))
        else:
            if self.tails.sprites()[-1].get_direction() == "up":
                self.tails.add(Snake_Tail(self.tails.sprites()[-1].get_pos()[0], self.tails.sprites()[-1].get_pos()[1] + 25, self.tails.sprites()[-1].get_direction(), self.speed))
            elif self.tails.sprites()[-1].get_direction() == "down":
                self.tails.add(Snake_Tail(self.tails.sprites()[-1].get_pos()[0], self.tails.sprites()[-1].get_pos()[1] - 25, self.tails.sprites()[-1].get_direction(), self.speed))
            elif self.tails.sprites()[-1].get_direction() == "right":
                self.tails.add(Snake_Tail(self.tails.sprites()[-1].get_pos()[0] - 25, self.tails.sprites()[-1].get_pos()[1], self.tails.sprites()[-1].get_direction(), self.speed))
            elif self.tails.sprites()[-1].get_direction() == "left":
                self.tails.add(Snake_Tail(self.tails.sprites()[-1].get_pos()[0] + 25, self.tails.sprites()[-1].get_pos()[1], self.tails.sprites()[-1].get_direction(), self.speed))
    
    def check_tails(self):
        if self.x_pos % 25 == 0 and self.y_pos % 25 == 0:
            for i, tail in enumerate(self.tails):
                if i == 0:                   
                    tail.set_direction(self.compare_tails(tail.get_pos()[0], tail.get_pos()[1], self.x_pos, self.y_pos))                                        
                else:
                    tail.set_direction(self.compare_tails(tail.get_pos()[0], tail.get_pos()[1] , self.tails.sprites()[i-1].get_pos()[0], self.tails.sprites()[i-1].get_pos()[1]))
                    
    def compare_tails(self, x1, y1, x2, y2): 
        if x1 == x2 and y1 < y2:
            return "down"
        if x1 == x2 and y1 > y2:
            return "up"    
        if x1 < x2 and y1 == y2:
            return "right"
        if x1 > x2 and y1 == y2:
            return "left"
    
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
        for tail in self.tails:
            tail.move()

    def set_facing(self, facing):
        self.facing = facing
        self.image = pygame.image.load(f"utils/snake_head_{self.facing}.png").convert_alpha()
        self.image.set_colorkey("white")

    def draw(self):
        self.tails.draw(self.screen)
        self.screen.blit(self.image, self.rect)
        
    def get_pos(self):
        return (self.x_pos, self.y_pos)
    
    def get_tails(self):
        return self.tails
    