import os
import sys
import pygame
import random
import asyncio
from map import Map
from snake import Snake_Head
from ai_snake import AI_Snake_Head
from apple import Apple
from ai_apple import AI_Apple
from button import Button
from webmodel import Webmodel

try:
    from stable_baselines3 import PPO
except:
    pass

class Game():
    """
    A class representing the game logic and mechanics.

    Attributes:
        WIDTH (int): Width of the game Map
        HEIGHT (int): Height of the game Map
        screen (pygame.Surface): The surface where the game will be displayed.
        pixels (int): The size of each game block.
        clock (pygame.time.Clock): A clock object to control the game's frame rate.
        font (pygame.font.Font): The font used for text rendering in the game.
        large_font (pygame.font.Font): The font used for larger text rendering in the game.
        gamestatus (str): The current status of the game ("pause" or "play").
        game_map (Map): The map object containing game borders.
        border_free_positions (list): A list of free positions on the game map not occupied by borders.
        snake (Snake_Head): The snake head of the Player.
        next_moves (list): A list of directions for the snake to move next.
        apple (Apple): The apple object.
        last_move (str): The last direction the snake moved.
        start_text (pygame.Surface): The text displayed when the game is paused, prompting the player to start.
        score (int): The player's score.
        score_text (pygame.Surface): The text displaying the player's score.
        ai_opponent (bool): Playing against AI or not.
        model (PPO | None): AI model trained to play snake.
        ai_button (pygame.Rect): Button to enable/disable AI opponent.
        gamemode_button (pygame.Rect): Button to switch gamemode.
        gamemodes (list): All Gamemodes.
        gamemode (int): Index of current Gamemode.
        ai_snake (AI_Snake_Head): The snake head of the AI.
        ai_apple (Apple): The seccond Apple for the AI.
        ai_colission (bool): Checks if the AI collided into something it should not.
        ai_next_move(int): Next move of the AI
        ai_colission_score(int): Score when AI collided with anything
        RESPAWN_AFTER(int): After how many eaten apples the AI respawns
        
    """
    with open("utils/map.txt", "r") as m:
            map_file = m.readlines()
            HEIGHT = len(map_file)
            WIDTH = len(map_file[0])-2
            
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
        self.ai_opponent = False
        self.edit_button = Button(50, 50, self.screen, "utils/edit_button.png")
        self.exit_button1 = Button(100, 400, self.screen, "utils/exit_button.png")
        self.exit_button2 = Button(775, 400, self.screen, "utils/exit_button.png")
        try:
            self.model = PPO.load(os.path.join("..", "backend", "snake-rl", "models", "model.zip"))
        except:
            self.model = Webmodel()
        self.ai_button = Button(800, 50, self.screen, "utils/ai_off_button.png")
        self.gamemode_button = Button(800, 125, self.screen, "utils/gamemode_chase_same_apple_button.png")#pygame.Rect(800, 125, 50, 50)
        self.gamemodes = ["chase_same_apple", "chase_different_apple"]
        self.gamemode = 0
        self.ai_snake = AI_Snake_Head(775, 400, self.screen)
        self.ai_apple = AI_Apple(400, 300, self.screen)
        self.ai_colission = False
        self.ai_next_move = 0
        self.ai_colission_score = 0
        self.RESPAWN_AFTER = 3
        

    async def gameloop(self) -> None:
        """
        The main game loop.
        """
        while True:
            while self.gamestatus == "pause":
                await self.pause_loop()
            
            while self.gamestatus == "play":
                await self.play_loop()
                
            while self.gamestatus == "edit":
                await self.edit_loop()
        
            
    async def pause_loop(self) -> None:
        """
        The pause game loop.
        """
        self.pause_events()
        self.game_map.draw()
        
        if self.ai_opponent:
            self.ai_snake.draw()
            if self.gamemodes[self.gamemode] == "chase_different_apple":
                self.ai_apple.draw()
        
        self.snake.draw()
        self.apple.draw()
        self.screen.blit(self.score_text, (220, 400))
        self.screen.blit(self.start_text, (95, 200))

        if self.model != None:
            self.ai_button.draw()   
            if self.ai_opponent:
                self.gamemode_button.draw() 
                
        self.edit_button.draw()
        pygame.display.update()
        self.clock.tick(30)
        await asyncio.sleep(0)


    async def play_loop(self) -> None:
        """
        The play game loop.
        """
        self.play_events()
        self.game_map.draw()
        self.screen.blit(self.score_text, (220, 400))
        
        if self.ai_opponent:
            if not self.ai_colission:
                
                await self.update_ai_next_move()
                
                if self.ai_snake.x_pos % self.pixels == 0 and self.ai_snake.y_pos % self.pixels == 0:
                    
                    while self.ai_next_move == None:
                        #getting the ai_move from the webmodel
                        if isinstance(self.model, Webmodel): 
                            tmp = await self.model.check_update()
                            if tmp:
                                if tmp != "nothing":
                                    self.ai_next_move = eval(tmp)['prediction']

                    action = self.ai_next_move
                    self.ai_next_move = None
                    if self.ai_snake.facing == "left":
                        if action == 1:
                            self.ai_snake.set_facing("down") 
                        elif action == 2:
                            self.ai_snake.set_facing("up")
                    elif self.ai_snake.facing == "up":
                        if action == 1:
                            self.ai_snake.set_facing("left") 
                        elif action == 2:
                            self.ai_snake.set_facing("right")
                    elif self.ai_snake.facing == "right":
                        if action == 1:
                            self.ai_snake.set_facing("up") 
                        elif action == 2:
                            self.ai_snake.set_facing("down")
                    elif self.ai_snake.facing == "down":
                        if action == 1:
                            self.ai_snake.set_facing("right") 
                        elif action == 2:
                            self.ai_snake.set_facing("left")

                self.ai_snake.move()
                self.ai_snake.check_tails()
                self.teleportation(self.ai_snake)
                self.ai_snake_colission_detection()
                
            else:
                if self.ai_colission_score + self.RESPAWN_AFTER == self.score:
                    self.ai_next_move = 0
                    self.ai_snake = AI_Snake_Head(775, 400, self.screen)
                    self.ai_colission = False

            self.ai_snake.draw()

            if self.gamemodes[self.gamemode] == "chase_different_apple":
                self.ai_apple.draw()

        if len(self.next_moves) >= 1 and self.snake.x_pos % self.pixels == 0 and self.snake.y_pos % self.pixels == 0:
            self.snake.set_facing(self.next_moves.pop(0))
        self.snake.move()    
        self.snake.check_tails()
        self.teleportation(self.snake)
        self.colission_detection()
        self.snake.draw()
        self.apple.draw()
        
        pygame.display.update()
        self.clock.tick(30)
        await asyncio.sleep(0)

    
    async def edit_loop(self) -> None:
        """
        The Edit mode loop.
        """
        self.edit_events()
        self.game_map.draw()
        self.exit_button1.draw()
        self.exit_button2.draw()

        pygame.display.update()
        self.clock.tick(30)
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
                if self.model != None:
                    if self.ai_button.rect.collidepoint(event.pos):
                        self.ai_opponent = not self.ai_opponent
                        if self.ai_opponent:
                            self.ai_button.image = pygame.image.load("utils/ai_on_button.png").convert_alpha()
                        else:
                            self.ai_button.image = pygame.image.load("utils/ai_off_button.png").convert_alpha()
                        self.ai_button.image.set_colorkey((127, 127, 127))

                    elif self.gamemode_button.rect.collidepoint(event.pos):
                        if self.gamemode == len(self.gamemodes)-1:
                            self.gamemode = 0
                        else:
                            self.gamemode += 1
                        self.gamemode_button.image = pygame.image.load(f"utils/gamemode_{self.gamemodes[self.gamemode]}_button.png").convert_alpha()
                        self.gamemode_button.image.set_colorkey((127, 127, 127))

                    elif self.edit_button.rect.collidepoint(event.pos):
                        self.gamestatus = "edit"

                    else:
                        self.gamestatus = "play"
                        self.reset()
                else:
                    if self.edit_button.rect.collidepoint(event.pos):
                        self.gamestatus = "edit"
                    else:
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
                max_next_move_legth = 2
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    if self.last_move != "down" and len(self.next_moves)<=max_next_move_legth:
                        self.next_moves.append("up") 
                        self.last_move = "up"  
                       
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    if self.last_move != "up" and len(self.next_moves)<=max_next_move_legth:
                        self.next_moves.append("down") 
                        self.last_move = "down" 
                        
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    if self.last_move != "left" and len(self.next_moves)<=max_next_move_legth:
                        self.next_moves.append("right")
                        self.last_move = "right" 
                        
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    if self.last_move != "right" and len(self.next_moves)<=max_next_move_legth:
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
        

    def edit_events(self) -> None:
        """
        Handles events while the game is in edit mode.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.exit_button1.rect.collidepoint(event.pos) or self.exit_button2.rect.collidepoint(event.pos):
                    self.gamestatus = "pause"
                else:
                    x = event.pos[0]//self.pixels
                    y = event.pos[1]//self.pixels
                    if self.map_file[y][x] == 'x':
                        self.map_file[y] = self.map_file[y][:x] + ' ' + self.map_file[y][x+1:]
                    else:
                        self.map_file[y] = self.map_file[y][:x] + 'x' + self.map_file[y][x+1:]
                    with open("utils/map.txt", "w") as m:
                        m.truncate()
                        for line in self.map_file:
                            m.writelines(line)

                    self.update_borders()


    def reset(self) -> None:
        """
        Resets the game to its initial state.
        """
        self.snake = Snake_Head(100, 400, self.screen)
        self.next_moves = []
        self.last_move = "up"
        self.ai_next_move = 0
        self.score = 0
        self.score_text = self.large_font.render(f"SCORE: {self.score}", False, [0, 155, 0])
        if self.model != None:
            self.ai_snake = AI_Snake_Head(775, 400, self.screen)
            self.ai_colission = False


    def colission_detection(self) -> None:
        """
        Checks for colissions of the Snake
        """
        if pygame.sprite.spritecollideany(self.snake, [self.apple]):
            self.snake.add_tail()
            self.spawn_apple()
            self.score += 1
            self.score_text = self.large_font.render(f"SCORE: {self.score}", False, [0, 155, 0])
        if pygame.sprite.spritecollideany(self.snake, self.snake.get_tails()) and pygame.sprite.spritecollideany(self.snake, self.snake.get_tails()) != self.snake.get_tails().sprites()[0]:
            self.gamestatus = "pause"                   
        if pygame.sprite.spritecollideany(self.snake, self.game_map.get_borders()):
            self.gamestatus = "pause"


    def ai_snake_colission_detection(self) -> None:
        """
        Checks for colissions of the AI Snake
        """
        if self.gamemodes[self.gamemode] == "chase_same_apple":
            tmp_apple = self.apple
        elif self.gamemodes[self.gamemode] == "chase_different_apple":
            tmp_apple = self.ai_apple
        if pygame.sprite.spritecollideany(self.ai_snake, [tmp_apple]):
            self.ai_snake.add_tail()
            self.spawn_apple(ai=self.gamemodes[self.gamemode] == "chase_different_apple")
            self.score -= 1
            self.score_text = self.large_font.render(f"SCORE: {self.score}", False, [0, 155, 0])
        if pygame.sprite.spritecollideany(self.ai_snake, self.ai_snake.get_tails()) and pygame.sprite.spritecollideany(self.ai_snake, self.ai_snake.get_tails()) != self.ai_snake.get_tails().sprites()[0]:
            self.ai_colission = True   
            self.ai_colission_score = self.score                
        if pygame.sprite.spritecollideany(self.ai_snake, self.game_map.get_borders()):
            self.ai_colission = True
            self.ai_colission_score = self.score


    def spawn_apple(self, ai=False) -> None:
        """
        Spawns the apple in a random free position
        """
        x, y = random.choice(self.get_possible_apple_positions())
        if not ai:
            self.apple = Apple(x*self.pixels, y*self.pixels, self.screen)
        else:
            self.ai_apple = AI_Apple(x*self.pixels, y*self.pixels, self.screen)


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
            
            if self.ai_opponent:
                if tmp_rect.collidepoint(self.ai_snake.get_pos()):
                    colission = True
                for tail in self.ai_snake.get_tails():
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
        
        for y in range(self.HEIGHT):
            for x in range(self.WIDTH):
                if (x*self.pixels, y*self.pixels) in border_positions:
                    continue
                positions.append((x,y))

        return positions


    def teleportation(self, snake: Snake_Head | AI_Snake_Head) -> None:
        """
        Teleports the snake to the other side when going off the map
        """
        if snake.x_pos > self.WIDTH*self.pixels-self.pixels and snake.facing == 'right':
            snake.set_pos(-self.pixels+snake.speed, snake.y_pos)
        if snake.x_pos < 0 and snake.facing == 'left':
            snake.set_pos(self.WIDTH*self.pixels-snake.speed, snake.y_pos)
        if snake.y_pos > self.HEIGHT*self.pixels-self.pixels and snake.facing == 'down':
            snake.set_pos(snake.x_pos, -self.pixels+snake.speed)
        if snake.y_pos < 0 and snake.facing == 'up':
            snake.set_pos(snake.x_pos, self.HEIGHT*self.pixels-snake.speed)

        for tail in snake.get_tails():
            if tail.x_pos > self.WIDTH*self.pixels-self.pixels and tail.facing == 'right':
                tail.set_pos(-self.pixels+tail.speed, tail.y_pos)
            if tail.x_pos < 0 and tail.facing == 'left':
                tail.set_pos(self.WIDTH*self.pixels-tail.speed, tail.y_pos)
            if tail.y_pos > self.HEIGHT*self.pixels-self.pixels and tail.facing == 'down':
                tail.set_pos(tail.x_pos, -self.pixels+tail.speed)
            if tail.y_pos < 0 and tail.facing == 'up':
                tail.set_pos(tail.x_pos, self.HEIGHT*self.pixels-snake.speed)
        
        
    async def update_ai_next_move(self) -> None:
        """
        Updates the next move of the AI
        """
        obs = None
        if (self.ai_snake.x_pos-self.ai_snake.speed) % self.pixels == 0 and self.ai_snake.y_pos % self.pixels == 0 and self.ai_snake.facing == 'right':
            obs = self.get_observation(self.ai_snake.x_pos+self.pixels-self.ai_snake.speed, self.ai_snake.y_pos)
        elif (self.ai_snake.x_pos+self.ai_snake.speed) % self.pixels == 0 and self.ai_snake.y_pos % self.pixels == 0 and self.ai_snake.facing == 'left':
            obs = self.get_observation(self.ai_snake.x_pos-self.pixels+self.ai_snake.speed, self.ai_snake.y_pos)
        elif self.ai_snake.x_pos % self.pixels == 0 and (self.ai_snake.y_pos-self.ai_snake.speed) % self.pixels == 0 and self.ai_snake.facing == 'down':
            obs = self.get_observation(self.ai_snake.x_pos, self.ai_snake.y_pos+self.pixels-self.ai_snake.speed)
        elif self.ai_snake.x_pos % self.pixels == 0 and (self.ai_snake.y_pos+self.ai_snake.speed) % self.pixels == 0 and self.ai_snake.facing == 'up':
            obs = self.get_observation(self.ai_snake.x_pos, self.ai_snake.y_pos-self.pixels+self.ai_snake.speed)

        if obs != None:
            if isinstance(self.model, Webmodel):
                await self.model.emit(obs)
                
            else:
                self.ai_next_move, _ = self.model.predict(obs)


    def get_observation(self, x:int, y:int) -> tuple[int, int, int, int, int, int, int]:
        """
        Gets the current observation for the AI snake.

        Parameters:
            x (int): The x-coordinate for the observation.
            y (int): The y-coordinate for the observation.

        Returns:
            tuple[int, int, int, int, int, int, int]: Current observation for the AI snake.
        """
        directs = {
            "up": (0, -1),
            "right": (1, 0),
            "down": (0, 1),
            "left": (-1, 0)
        }
        d1, d2, d3 = self.get_distances(x, y)
        if self.gamemodes[self.gamemode] == "chase_same_apple":
            tmp_apple = self.apple
        elif self.gamemodes[self.gamemode] == "chase_different_apple":
            tmp_apple = self.ai_apple
        return (x - tmp_apple.x_pos) //self.pixels, (y - tmp_apple.y_pos) // self.pixels, directs[self.ai_snake.facing][0], directs[self.ai_snake.facing][1], d1, d2, d3


    def get_distances(self, x_pos:int, y_pos:int) -> tuple[int, int, int]:
        """
        Gets the current distances (left, straight, right) to the next object the snake should not collide with

        Parameters:
            x (int): The x-coordinate from where the distances are calculated.
            y (int): The y-coordinate from where the distances are calculated.

        Returns:
            tuple[int, int, int]: The 3 distances
        """
        snake_x = int(x_pos)
        snake_y = int(y_pos)
        snake_facing = self.ai_snake.facing

        distances = [snake_x//self.pixels, snake_y//self.pixels, self.WIDTH-snake_x//self.pixels-1, self.HEIGHT-snake_y//self.pixels-1]
        tails = self.ai_snake.get_tails().sprites()
        borders = self.game_map.get_borders().sprites()
        
        for x in range(snake_x//self.pixels):
                tmp_rect = pygame.Rect(snake_x-x*self.pixels, snake_y, self.pixels, self.pixels)
                for tail in tails:
                    if tmp_rect.collidepoint(tail.get_pos()):
                        if x < distances[0]:
                            distances[0] = x
                            break

                for border in borders:
                    if tmp_rect.collidepoint(border.get_pos()):
                        if x < distances[0]:
                            distances[0] = x  
                            break          

        for y in range(snake_y//self.pixels):
                tmp_rect = pygame.Rect(snake_x, snake_y-y*self.pixels, self.pixels, self.pixels)
                for tail in tails:
                    if tmp_rect.collidepoint(tail.get_pos()):
                        if y < distances[1]:
                            distances[1] = y
                            break

                for border in borders:
                    if tmp_rect.collidepoint(border.get_pos()):
                        if y < distances[1]:
                            distances[1] = y
                            break


        for x in range(self.WIDTH - snake_x//self.pixels):
                tmp_rect = pygame.Rect(snake_x+x*self.pixels, snake_y, self.pixels, self.pixels)
                for tail in tails:
                    if tmp_rect.collidepoint(tail.get_pos()):
                        if x < distances[2]:
                            distances[2] = x
                            break

                for border in borders:
                    if tmp_rect.collidepoint(border.get_pos()):
                        if x < distances[2]:
                            distances[2] = x
                            break

        for y in range(self.HEIGHT - snake_y//self.pixels):
                tmp_rect = pygame.Rect(snake_x, snake_y+y*self.pixels, self.pixels, self.pixels)
                for tail in tails:
                    if tmp_rect.collidepoint(tail.get_pos()):
                        if y < distances[3]:
                            distances[3] = y
                            break

                for border in borders:
                    if tmp_rect.collidepoint(border.get_pos()):
                        if y < distances[3]:
                            distances[3] = y
                            break
        

        if snake_facing == "left":
            return distances[3], distances[0], distances[1]
        elif snake_facing == "up":
            return distances[0], distances[1], distances[2]
        elif snake_facing == "right":
            return distances[1], distances[2], distances[3]
        elif snake_facing == "down":
            return distances[2], distances[3], distances[0]


    def update_borders(self) -> None:
        """
        Updates the borders according to the map file
        """
        self.game_map.borders.empty()
        self.game_map.add_borders()
        self.spawn_apple()


if __name__ == "__main__":
    game = Game()
    asyncio.run(game.gameloop())
