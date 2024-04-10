from env_tail import Tail

class Snake():
    def __init__(self, x: int, y: int, direct: tuple[int, int]=(0,-1)) -> None:
        self.x: int = x
        self.y: int = y
        self.direct: tuple[int, int] = direct
        self.tails:list[Tail] = []
        for i in range(3):
            self.append_tail()


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
            tail: Tail
            for i, tail in enumerate(self.tails[::-1]):
                if i == len(self.tails)-1:
                    tail.set_direct(self.direct)
                else:
                    tail.set_direct(self.tails[::-1][i+1].direct)


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
