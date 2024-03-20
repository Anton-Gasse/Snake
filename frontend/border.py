import pygame

class Border(pygame.sprite.Sprite):
    """
    A class representing a border object.

    Attributes:
        x (int): The x-coordinate position of the border on the screen.
        y (int): The y-coordinate position of the border on the screen.
        image (pygame.Surface): The image representing the border.
        rect (pygame.Rect): The rectangular area occupied by the border image on the screen.
    """
    def __init__(self, x:int, y:int) -> None:
        """
        Initializes a Border object.

        Parameters:
            x (int): The x-coordinate position of the border on the screen.
            y (int): The y-coordinate position of the border on the screen.
        """
        super().__init__()
        self.image = pygame.image.load("utils/border.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
    

    def get_pos(self) -> tuple[int, int]:
        """
        Returns the position of the border.

        Returns:
            tuple: The x and y coordinates of the top-left corner of the border.
        """
        return self.rect.topleft