import pygame
from border import Border

class Map():
    """
    A class representing a map containing borders.

    Attributes:
        borders (pygame.sprite.Group): A group containing all the border objects on the map.
        screen (pygame.Surface): The surface where the map will be drawn.
        map_file (list): A list containing the map layout read from a text file.
        background (pygame.Surface): The background image of the map.
    """
    def __init__(self, screen:pygame.Surface) -> None:
        """
        Initializes a Map object.

        Parameters:
            screen (pygame.Surface): The surface where the map will be drawn.
        """
        self.borders = pygame.sprite.Group()
        self.screen = screen
        with open("utils/map.txt") as m:
            self.map_file = m.readlines()
        self.add_borders()
        self.background = pygame.image.load("utils/background.png")
        

    def add_borders(self) -> None:
        """
        Adds borders to the map based on the layout read from a text file.
        """
        for i in range(len(self.map_file)):
            for j in range(len(self.map_file[i])-1):
                if self.map_file[i][j] == "x":
                    self.borders.add(Border(j * 25,i * 25))


    def draw(self) -> None:
        """
        Draws the map on the screen.
        """
        self.screen.blit(self.background , (0,0))
        self.borders.draw(self.screen)


    def get_borders(self) -> pygame.sprite.Group:
        """
        Returns the group of borders on the map.

        Returns:
            pygame.sprite.Group: The group of border objects.
        """
        return self.borders