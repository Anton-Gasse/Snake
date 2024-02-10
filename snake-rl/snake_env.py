from typing import Any, SupportsFloat
import gymnasium
from gymnasium import spaces
import random
import time

class Tail():

    def __init__(self, x: int, y: int, direct: tuple[int, int]) -> None:
        self.x: int = x
        self.y: int = y
        self.direct: tuple[int, int] = direct

    def get_pos(self) -> tuple[int, int]:
        return self.x, self.y
    
    def get_direct(self) -> tuple[int, int]:
        return self.direct

    def set_direct(self, direct: tuple[int, int]) -> None:
        self.direct = direct

    def move(self) -> None:
        self.x += self.direct[0]
        self.y += self.direct[1]

class Snake():

    def __init__(self, x: int, y: int, direct: tuple[int, int]=(0,-1)) -> None:
        self.x: int = x
        self.y: int = y
        self.direct: tuple[int, int] = direct
        self.tails:list[Tail] = []

    def get_pos(self) -> tuple[int, int]:
        return self.x, self.y
    
    def get_direct(self) -> tuple[int, int]:
        return self.direct

    def change_direct(self, movement: str) -> None:
        if movement == "straight":
            pass
        
        elif movement == "left-turn":
            if self.direct == (0, -1):
                self.direct = (-1, 0)
            elif self.direct == (1, 0):
                self.direct = (0, -1)
            elif self.direct == (0, 1):
                self.direct = (1, 0)
            elif self.direct == (-1, 0):
                self.direct = (0, 1)
        
        elif movement == "right-turn":
            if self.direct == (0, -1):
                self.direct = (1, 0)
            elif self.direct == (1, 0):
                self.direct = (0, 1)
            elif self.direct == (0, 1):
                self.direct = (-1, 0)
            elif self.direct == (-1, 0):
                self.direct = (0, -1)

    def move(self) -> None:
        self.x += self.direct[0]
        self.y += self.direct[1]
        for tail in self.tails:
            tail.move()
            
    def get_tails(self) -> list[Tail]:
        return self.tails
    
    def update_tail_directs(self) -> None:
        if len(self.tails) != 0:
            self.tails[0].set_direct(self.direct)
            tail: Tail
            for i, tail in enumerate(self.tails[1:-1]):
                tail.set_direct(self.tails[i])
    
    def append_tail(self):
        if len(self.tails) == 0:
            if self.direct == (0, -1):
                self.tails.append(Tail(self.x, self.y+1, self.direct))
            elif self.direct == (-1, 0):
                self.tails.append(Tail(self.x+1, self.y, self.direct))
            elif self.direct == (0, 1):
                self.tails.append(Tail(self.x, self.y-1, self.direct))
            elif self.direct == (1, 0):
                self.tails.append(Tail(self.x-1, self.y, self.direct))
        
        else:
            tmp_x, tmp_y = self.tails[-1].get_pos()
            tmp_direct = self.tails[-1].get_direct()
            if tmp_direct == (0, -1):
                self.tails.append(Tail(tmp_x, tmp_y+1, tmp_direct))
            elif tmp_direct == (-1, 0):
                self.tails.append(Tail(tmp_x+1, tmp_y, tmp_direct))
            elif tmp_direct == (0, 1):
                self.tails.append(Tail(tmp_x, tmp_y-1, tmp_direct))
            elif tmp_direct == (1, 0):
                self.tails.append(Tail(tmp_x-1, tmp_y, tmp_direct))


class Apple():
    def __init__(self, x: int, y: int) -> None:
        self.x: int = x
        self.y: int = y
    
    def get_pos(self) -> tuple[int, int]:
        return self.x, self.y

    def set_pos(self, x: int, y: int):
        self.x = x
        self.y = y


class SnakeEnv(gymnasium.Env):
    MAP_WIDTH: int = 36
    MAP_HEIGHT: int = 24
    def __init__(self, env_config: dict):
        self.action_space: spaces.Discrete = spaces.Discrete(3)
        self.observation_space: spaces.Box = spaces.Dict({
            "snake_pos_x": spaces.Discrete(36),
            "snake_pos_y": spaces.Discrete(24),
            "apple_pos_x": spaces.Discrete(36),
            "apple_pos_y": spaces.Discrete(24)

        })
        
        
    def reset(self, seed: int=None, options: dict[str, Any]=None) -> tuple[Any, dict[str, Any]]:
        self.snake: Snake = Snake(4, 16)
        self.apple: Apple = Apple(6, 16)#Apple(16, 12)
        self.step_counter: int = 0
        self.update_map()
        
        info = {}
        return self.observation_space, info
    
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
            reward += 1
        self.update_map()
        if self.check_border_colission():
            terminated = True
        if self.check_tail_collission():
            terminated = True
        self.step_counter += 1
        if self.step_counter >= 100:
            truncated = True

        info = {}
        snake_x, snake_y = self.snake.get_pos()
        apple_x, apple_y = self.apple.get_pos()
        obs = {
            "snake_pos_x": snake_x,
            "snake_pos_y": snake_y,
            "apple_pos_x": apple_x,
            "apple_pos_y": apple_y
        }
        return obs, reward, terminated, truncated, info

    def update_map(self) -> None:
        self.map: list[list[str]] = [[" " for _ in range(self.MAP_WIDTH)] for _ in range(self.MAP_HEIGHT)]
        tmp_x, tmp_y = self.snake.get_pos()
        self.map[tmp_y][tmp_x] = "s"
        tail: Tail
        for tail in self.snake.get_tails():
            tmp_x, tmp_y = tail.get_pos()
            self.map[tmp_y][tmp_x] = "t"
        tmp_x, tmp_y = self.apple.get_pos()
        self.map[tmp_y][tmp_x] = "a"

    def update_apple(self) -> None:
        tmp_x: int = random.randint(1, self.MAP_WIDTH-2)
        tmp_y: int = random.randint(1, self.MAP_HEIGHT-2)
        self.apple.set_pos(tmp_x, tmp_y)
        
    def render_map(self) -> None:
        for m in self.map:
            print(m)

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

if __name__ == "__main__":
    e = SnakeEnv({})
    e.reset()


    for i in range(10):
        done = False
        while not done:
            action = random.randint(0, 2)
            print("ACTION", action)
            done = e.step(action)[2]
            e.render_map()
            time.sleep(1)
        e.reset()
        print("RESET")