import random
import time
import numpy as np
import gymnasium
import math
from gymnasium import spaces
from typing import Any, SupportsFloat
from snake_env import Snake
from tail_env import Tail
from apple_env import Apple

class SnakeEnv(gymnasium.Env):
    MAP_WIDTH: int = 10#36
    MAP_HEIGHT: int = 10#24
    def __init__(self, env_config: dict):
        self.action_space: spaces.Discrete = spaces.Discrete(3)
        self.observation_space: spaces.Box = spaces.Box(low=np.array([0, -self.MAP_WIDTH-1, -self.MAP_HEIGHT-1, -1, -1, 1, 1, 1]), high=np.array([self.MAP_HEIGHT*self.MAP_WIDTH, self.MAP_WIDTH-1, self.MAP_HEIGHT-1, 1, 1, max(self.MAP_HEIGHT, self.MAP_WIDTH)-2, max(self.MAP_HEIGHT, self.MAP_WIDTH)-2, max(self.MAP_HEIGHT, self.MAP_WIDTH)-2]), shape=(8,), dtype=int)
        self.map: list[list[str]] = [[" " for _ in range(self.MAP_WIDTH)] for _ in range(self.MAP_HEIGHT)]
        
    def reset(self, seed: int=None, options: dict[str, Any]=None) -> tuple[Any, dict[str, Any]]:
        self.snake: Snake = Snake(4, 4)
        self.apple: Apple = Apple(6, 6)
        self.step_counter: int = 0
        self.update_apple()
        self.update_map()
        snake_x, snake_y = self.snake.get_pos()
        apple_x, apple_y = self.apple.get_pos()
        d1, d2, d3 = self.get_distance_next_obj()
        obs = np.array([len(self.snake.tails), snake_x-apple_x, snake_y-apple_y, self.snake.direct[0], self.snake.direct[1], d1, d2, d3])
        info = {}
        return obs, info
    
    def step(self, action: int) -> tuple[Any, SupportsFloat, bool, bool, dict[str, Any]]:
        reward: int = 0
        terminated: bool = False
        truncated: bool = False
        actions: dict[int, str] = {
            0: "straight",
            1: "left-turn",
            2: "right-turn"
        }
        self.snake.change_direct(actions[action])
        self.snake.move()
        self.snake.update_tail_directs()

        if self.check_apple_colission():
            self.snake.append_tail()
            self.update_apple()
            self.step_counter = 0
            reward += 100
            if len(self.snake.tails) == 20: print("20 BIGG")
        else:
            snake_x, snake_y = self.snake.get_pos()
            apple_x, apple_y = self.apple.get_pos()
            reward += 1/(math.sqrt((snake_x-apple_x)**2 + (snake_y-apple_y)**2) * 0.1) - (self.step_counter*0.1)
        
        self.update_map()
        if self.check_border_colission():
            terminated = True
            reward -= 100
        if self.check_tail_collission():
            terminated = True
            reward -= 100
        self.step_counter += 1
        if self.step_counter >= 1000:
            truncated = True
            reward -= 100

        info = {}
        snake_x, snake_y = self.snake.get_pos()
        apple_x, apple_y = self.apple.get_pos()

        d1, d2, d3 = self.get_distance_next_obj()
        obs = np.array([len(self.snake.tails), snake_x-apple_x, snake_y-apple_y, self.snake.direct[0], self.snake.direct[1], d1, d2, d3])
        return obs, reward, terminated, truncated, info

    def update_map(self) -> None:
        self.map: list[list[str]] = [[" " for _ in range(self.MAP_WIDTH)] for _ in range(self.MAP_HEIGHT)]
        tmp_x, tmp_y = self.apple.get_pos()
        self.map[tmp_y][tmp_x] = "a"
        tmp_x, tmp_y = self.snake.get_pos()
        self.map[tmp_y][tmp_x] = "s"
        tail: Tail
        for tail in self.snake.get_tails():
            tmp_x, tmp_y = tail.get_pos()
            self.map[tmp_y][tmp_x] = "t"
        

    def update_apple(self) -> None:
        tmp_x, tmp_y = random.choice(self.get_possible_apple_positions())
        self.apple.set_pos(tmp_x, tmp_y)
        

    def get_possible_apple_positions(self) -> list[tuple[int, int]]:
        positions: list[tuple[int, int]] = []
        for y in range(self.MAP_HEIGHT-1):
            for x in range(1, self.MAP_WIDTH-1):
                if self.map[y][x] not in ['t', 's']:
                    positions.append((x, y))
                
        return positions
        
    def render(self) -> None:
        for m in self.map:
            print(m)
        time.sleep(0.3)

    def check_apple_colission(self) -> bool:
        snake_x, snake_y = self.snake.get_pos()
        apple_x, apple_y = self.apple.get_pos()
        return snake_x==apple_x and snake_y==apple_y

    def check_border_colission(self) -> bool:
        snake_x, snake_y = self.snake.get_pos()
        return snake_x == 0 or snake_x == self.MAP_WIDTH-1 or snake_y == 0 or snake_y == self.MAP_HEIGHT-1
    
    def check_tail_collission(self) -> bool:
        snake_x, snake_y = self.snake.get_pos()
        for tail in self.snake.get_tails():
            tail_x, tail_y = tail.get_pos()
            if snake_x == tail_x and snake_y == tail_y:
                return True
        return False
    
    def get_distance_next_obj(self) -> list[int, int, int]:
        snake_x, snake_y = self.snake.get_pos()
        snake_direct = self.snake.get_direct()

        distances = [snake_x, snake_y, self.MAP_WIDTH-snake_x-1, self.MAP_HEIGHT-snake_y-1]
        #going left
        for x in range(snake_x):
            if self.map[snake_y][snake_x-x] == 't':
                distances[0] = x
        #going up
        for y in range(snake_y):
            if self.map[snake_y-y][snake_x] == 't':
                distances[1] = y
        #going right
        for x in range(self.MAP_WIDTH-snake_x):
            if self.map[snake_y][snake_x+x] == 't':
                distances[2] = x
        
        #going down
        for y in range(self.MAP_HEIGHT-snake_y):
            if self.map[snake_y+y][snake_x] == 't':
                distances[3] = y

        if snake_direct == (-1, 0):
            return distances[3], distances[0], distances[1]
        elif snake_direct == (0, -1):
            return distances[0], distances[1], distances[2]
        elif snake_direct == (1, 0):
            return distances[1], distances[2], distances[3]
        elif snake_direct == (0, 1):
            return distances[2], distances[3], distances[0]       

if __name__ == "__main__":
    test_env = SnakeEnv({})
    test_env.reset()
    
    for i in range(4):
        test_env.snake.append_tail()
    
    for i in range(10):
        done = False
        while not done:
            action = random.randint(0, 2)
            print("ACTION", action)
            obs, reward, done, truncated, _ = test_env.step(action)
            print("REWARD", reward)
            print("OBS", obs)
            test_env.render_map()
            
        test_env.reset()
        print("RESET")