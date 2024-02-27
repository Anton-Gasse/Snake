import pygame
from border import Border

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
            for j in range(len(self.map_file[i])-1):
                if self.map_file[i][j] == "x":
                    self.borders.add(Border(j * 25,i * 25))

    def draw(self):
        self.screen.blit(self.background , (0,0))
        self.borders.draw(self.screen)
    def get_borders(self):
        return self.borders