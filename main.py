import sys
import pygame
import math
import random
import time
import asyncio

class Game():
    def __init__(self):
        
        pygame.init()
        self.screen = pygame.display.set_mode((900, 600), pygame.RESIZABLE)
        pygame.display.set_caption("Snake")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font("utils/astroids-pixel-font.ttf", 30)
        self.font_groß = pygame.font.Font("utils/astroids-pixel-font.ttf", 60)
        self.gamestatus = "pause"
        self.game_map = Map(self.screen)
        self.snake = Snake_Head(100, 400, self.screen)
        self.next_move = "up"
        self.move_count = 0
        self.apple = Apple(400, 300, self.screen)
        self.last_move = "up"
        self.start_text = self.font.render("PRESS ENTER TO START", False, "White")
        self.score = 0
        self.score_text = self.font_groß.render(f"SCORE: {self.score}", False, [0, 155, 0])
    async def gameloop(self):
        while True:
            while self.gamestatus == "pause":
                self.pause_events()
                self.game_map.draw()
                self.screen.blit(self.score_text, (220, 400))
                self.snake.draw()
                self.apple.draw()
                self.screen.blit(self.start_text, (170, 200))
                pygame.display.update()
                self.clock.tick(60)
                await asyncio.sleep(0)
            while self.gamestatus == "play":
                self.play_events()
                self.game_map.draw()
                self.screen.blit(self.score_text, (220, 400))
                if self.move_count >= 10:
                    self.snake.set_facing(self.next_move)
                    self.move_count = 0
                    self.last_move = self.next_move
                self.snake.move()
                self.move_count += 1
                
                self.snake.check_tails()
                self.snake.draw()
                self.apple.draw()
                
                
                #Collision Snake
                if pygame.sprite.spritecollideany(self.snake, [self.apple]):
                    self.snake.add_tail()
                    self.spawn_apple()
                    self.score += 1
                    self.score_text = self.font_groß.render(f"SCORE: {self.score}", False, [0, 155, 0])
                if pygame.sprite.spritecollideany(self.snake, self.snake.get_tails()) and pygame.sprite.spritecollideany(self.snake, self.snake.get_tails()) != self.snake.get_tails().sprites()[0]:
                    self.gamestatus = "pause"                   
                if pygame.sprite.spritecollideany(self.snake, self.game_map.get_borders()):
                    self.gamestatus = "pause"
                
                
                
                pygame.display.update()
                self.clock.tick(60)
                await asyncio.sleep(0)
        
        
    def pause_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:    
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_RETURN:
                    self.gamestatus = "play"
                    self.reset()                                        
    def play_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                   
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    if self.last_move != "down":
                        self.next_move = "up"   
                       
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    if self.last_move != "up":
                        self.next_move = "down"  
                        
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    if self.last_move != "left":
                        self.next_move = "right" 
                        
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    if self.last_move != "right":
                        self.next_move = "left"
                        
    def reset(self):
        self.snake = Snake_Head(100, 400, self.screen)
        self.next_move = "up"
        self.last_move = "up"
        self.move_count = 10
        self.score = 0
        self.score_text = self.font_groß.render(f"SCORE: {self.score}", False, [0, 155, 0])
    def spawn_apple(self):
        x = random.randint(1, 34)
        y = random.randint(1, 22)
        if (x, y) != self.snake.get_pos:
            self.apple = Apple(x*25, y*25, self.screen)
            if pygame.sprite.spritecollideany(self.apple, self.snake.get_tails()):
                return self.spawn_apple()          
        else:
            return self.spawn_apple()
class Border(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("utils/border.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        
 
class Map():
    def __init__(self, screen):
        self.borders = pygame.sprite.Group()
        self.screen = screen
        with open("utils/map.txt") as m:
            self.map_file = m.readlines()
        self.add_borders()
        self.background = pygame.image.load("utils/background.png")
        
        
    def add_borders(self):
        for i in range(len(self.map_file)):
            for j in range(len(self.map_file[i])):
                if self.map_file[i][j] == "x":
                    self.borders.add(Border(j * 25,i * 25))

    def draw(self):
        self.screen.blit(self.background , (0,0))
        self.borders.draw(self.screen)
    def get_borders(self):
        return self.borders
        

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
    def add_tail(self):
    #letzter tail facing checken
        if self.tails.sprites() == []:
            if self.facing == "up":            
                self.tails.add(Snake_Tail(self.x_pos, self.y_pos + 25, "up"))
            
            elif self.facing == "down":
                self.tails.add(Snake_Tail(self.x_pos, self.y_pos - 25, "down"))
            elif self.facing == "right":            
                self.tails.add(Snake_Tail(self.x_pos - 25, self.y_pos, "right"))
            elif self.facing == "left":        
                self.tails.add(Snake_Tail(self.x_pos + 25, self.y_pos, "left"))
        else:
            if self.tails.sprites()[-1].get_direction() == "up":
                self.tails.add(Snake_Tail(self.tails.sprites()[-1].get_pos()[0], self.tails.sprites()[-1].get_pos()[1] + 25, self.tails.sprites()[-1].get_direction()))
            elif self.tails.sprites()[-1].get_direction() == "down":
                self.tails.add(Snake_Tail(self.tails.sprites()[-1].get_pos()[0], self.tails.sprites()[-1].get_pos()[1] - 25, self.tails.sprites()[-1].get_direction()))
            elif self.tails.sprites()[-1].get_direction() == "right":
                self.tails.add(Snake_Tail(self.tails.sprites()[-1].get_pos()[0] - 25, self.tails.sprites()[-1].get_pos()[1], self.tails.sprites()[-1].get_direction()))
            elif self.tails.sprites()[-1].get_direction() == "left":
                self.tails.add(Snake_Tail(self.tails.sprites()[-1].get_pos()[0] + 25, self.tails.sprites()[-1].get_pos()[1], self.tails.sprites()[-1].get_direction()))
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
            self.y_pos -= 2.5
            self.rect.topleft = (self.x_pos, self.y_pos)                            
        elif self.facing == "down":
            self.y_pos += 2.5
            self.rect.topleft = (self.x_pos, self.y_pos)                    
        elif self.facing == "right":
            self.x_pos += 2.5
            self.rect.topleft = (self.x_pos, self.y_pos)               
        elif self.facing == "left":
            self.x_pos -= 2.5
            self.rect.topleft = (self.x_pos, self.y_pos)           
        for tail in self.tails:
            tail.move()

    def set_facing(self, facing):
        if self.x_pos % 25 == 0 and self.y_pos % 25 == 0:
            self.facing = facing
            self.image = pygame.image.load(f"utils/snake_head_{self.facing}.png").convert_alpha()
            self.image.set_colorkey("white")

    def draw(self):
        self.screen.blit(self.image, self.rect)
        self.tails.draw(self.screen)
    def get_pos(self):
        return (self.x_pos, self.y_pos)
    def get_tails(self):
        return self.tails
    
class Snake_Tail(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, facing):
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
    def get_pos(self):
        return (self.x_pos, self.y_pos)
    def move(self):
        if self.facing == "up":
            self.y_pos -= 2.5
            self.rect.topleft = (self.x_pos, self.y_pos)                           
        elif self.facing == "down":
            self.y_pos += 2.5
            self.rect.topleft = (self.x_pos, self.y_pos)            
        elif self.facing == "right":
            self.x_pos += 2.5
            self.rect.topleft = (self.x_pos, self.y_pos)                
        elif self.facing == "left":
            self.x_pos -= 2.5
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
                                    
if __name__ == "__main__":
    game = Game()
    asyncio.run(game.gameloop())

#Tail Spawn an letzten dran