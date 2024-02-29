import sys
import pygame
import random
import asyncio
from map import Map
from snake import Snake_Head
from apple import Apple

class Game():
    """
    A class representing the game logic and mechanics.

    Attributes:
        screen (pygame.Surface): The surface where the game will be displayed.
        pixels (int): The size of each game block.
        clock (pygame.time.Clock): A clock object to control the game's frame rate.
        font (pygame.font.Font): The font used for text rendering in the game.
        large_font (pygame.font.Font): The font used for larger text rendering in the game.
        gamestatus (str): The current status of the game ("pause" or "play").
        game_map (Map): The map object containing game borders.
        border_free_positions (list): A list of free positions on the game map not occupied by borders.
        snake (Snake_Head): The snake head object.
        next_moves (list): A list of directions for the snake to move next.
        apple (Apple): The apple object.
        last_move (str): The last direction the snake moved.
        start_text (pygame.Surface): The text displayed when the game is paused, prompting the player to start.
        score (int): The player's score.
        score_text (pygame.Surface): The text displaying the player's score.
    """
    def __init__(self) -> None:
        """
        Initializes the Game object.
        """
        pygame.init()
        self.screen = pygame.display.set_mode((900, 600), pygame.RESIZABLE)
        pygame.display.set_caption("Snake")
        self.pixels = 25
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font("utils/astroids-pixel-font.ttf", 30)
        self.large_font = pygame.font.Font("utils/astroids-pixel-font.ttf", 60)
        self.gamestatus = "pause"
        self.game_map = Map(self.screen)
        self.border_free_positions = self.get_border_free_positions()
        self.snake = Snake_Head(100, 400, self.screen)
        self.next_moves = []
        self.apple = Apple(400, 300, self.screen)
        self.last_move = "up"
        self.start_text = self.font.render("PRESS ENTER OR TAP TO START", False, "White")
        self.score = 0
        self.score_text = self.large_font.render(f"SCORE: {self.score}", False, [0, 155, 0])
        

    async def gameloop(self) -> None:
        """
        The main game loop.
        """
        while True:
            while self.gamestatus == "pause":
                self.pause_events()
                self.game_map.draw()
                self.screen.blit(self.score_text, (220, 400))
                self.snake.draw()
                self.apple.draw()
                self.screen.blit(self.start_text, (95, 200))
                pygame.display.update()
                self.clock.tick(60)
                await asyncio.sleep(0)
            
            while self.gamestatus == "play":
                self.play_events()
                self.game_map.draw()
                self.screen.blit(self.score_text, (220, 400))
                
                if len(self.next_moves) >= 1 and self.snake.x_pos % 25 == 0 and self.snake.y_pos % 25 == 0:
                    self.snake.set_facing(self.next_moves.pop(0))
                self.snake.move()    
                self.snake.check_tails()
                self.teleportation()
                self.snake.draw()
                self.apple.draw()
                
                if pygame.sprite.spritecollideany(self.snake, [self.apple]):
                    self.snake.add_tail()
                    self.spawn_apple()
                    self.score += 1
                    self.score_text = self.large_font.render(f"SCORE: {self.score}", False, [0, 155, 0])
                if pygame.sprite.spritecollideany(self.snake, self.snake.get_tails()) and pygame.sprite.spritecollideany(self.snake, self.snake.get_tails()) != self.snake.get_tails().sprites()[0]:
                    self.gamestatus = "pause"                   
                if pygame.sprite.spritecollideany(self.snake, self.game_map.get_borders()):
                    self.gamestatus = "pause"
                
                pygame.display.update()
                self.clock.tick(60)
                await asyncio.sleep(0)
        

    def pause_events(self) -> None:
        """
        Handles events while the game is paused.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.gamestatus = "play"
                    self.reset()  
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.gamestatus = "play"
                self.reset()


    def play_events(self) -> None:
        """
        Handles events while the game is playing.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    if self.last_move != "down":
                        self.next_moves.append("up") 
                        self.last_move = "up"  
                       
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    if self.last_move != "up":
                        self.next_moves.append("down") 
                        self.last_move = "down" 
                        
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    if self.last_move != "left":
                        self.next_moves.append("right")
                        self.last_move = "right" 
                        
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    if self.last_move != "right":
                        self.next_moves.append("left")
                        self.last_move = "left"

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if 300 <= x <= 600 and 0 <= y <= 300:
                    if self.last_move != "down":
                        self.next_moves.append("up") 
                        self.last_move = "up" 
                if 300 <= x <= 600 and 301 <= y <= 600:
                    if self.last_move != "up":
                        self.next_moves.append("down") 
                        self.last_move = "down" 
                
                if 601 <= x <= 900 and 0 <= y <= 600:
                    if self.last_move != "left":
                        self.next_moves.append("right")
                        self.last_move = "right" 

                if 0 <= x <= 299 and 0 <= y <= 600:
                    if self.last_move != "right":
                        self.next_moves.append("left")
                        self.last_move = "left"
        

    def reset(self) -> None:
        """
        Resets the game to its initial state.
        """
        self.snake = Snake_Head(100, 400, self.screen)
        self.next_moves = []
        self.last_move = "up"
        self.score = 0
        self.score_text = self.large_font.render(f"SCORE: {self.score}", False, [0, 155, 0])
    

    def spawn_apple(self) -> None:
        """
        Spawns the apple in a random free position
        """
        x, y = random.choice(self.get_possible_apple_positions())
        self.apple = Apple(x*self.pixels, y*self.pixels, self.screen)
        

    def get_possible_apple_positions(self) -> list[tuple[int, int]]:
        """
        Determines possible positions to spawn an apple.

        Returns:
            list[tuple[int, int]]: A list of possible positions.
        """
        positions = []
        for x, y in self.border_free_positions:
            tmp_rect = pygame.Rect(self.pixels*x, self.pixels*y, self.pixels, self.pixels)
            colission = False
            if tmp_rect.collidepoint(self.snake.get_pos()):
                colission = True
                
            for tail in self.snake.get_tails():
                if tmp_rect.collidepoint(tail.get_pos()):
                    colission = True
            if colission == False:
                positions.append((x, y))
        
        return positions
    

    def get_border_free_positions(self) -> list[tuple[int, int]]:
        """
        Determines the free positions on the game map not occupied by borders.

        Returns:
            list[tuple[int, int]]: A list of free positions.
        """
        positions = []
        border_positions= [border.get_pos() for border in self.game_map.get_borders()]
        with open("utils/map.txt", "r") as m:
            file = m.readlines()
            heigth = len(file)
            width = len(file[0])-1
        for y in range(heigth):
            for x in range(width):
                if (x*self.pixels, y*self.pixels) in border_positions:
                    continue
                positions.append((x,y))

        return positions
      
    def teleportation(self):
        """
        Teleports the snake to the other side when going off the map
        """
        if self.snake.x_pos >= 900 and self.snake.facing == 'right':
            self.snake.set_pos(0, self.snake.y_pos)
        if self.snake.x_pos <= 0 and self.snake.facing == 'left':
            self.snake.set_pos(900, self.snake.y_pos)
        if self.snake.y_pos >= 600 and self.snake.facing == 'down':
            self.snake.set_pos(self.snake.x_pos, 0)
        if self.snake.y_pos <= 0 and self.snake.facing == 'up':
            self.snake.set_pos(self.snake.x_pos, 600)

        for tail in self.snake.get_tails():
            if tail.x_pos >= 900 and tail.facing == 'right':
                tail.set_pos(0, tail.y_pos)
            if tail.x_pos <= 0 and tail.facing == 'left':
                tail.set_pos(900, tail.y_pos)
            if tail.y_pos >= 600 and tail.facing == 'down':
                tail.set_pos(tail.x_pos, 0)
            if tail.y_pos <= 0 and tail.facing == 'up':
                tail.set_pos(tail.x_pos, 600)

if __name__ == "__main__":
    game = Game()
    asyncio.run(game.gameloop())
