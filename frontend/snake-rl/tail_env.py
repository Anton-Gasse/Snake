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