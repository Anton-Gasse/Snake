class Apple():
    def __init__(self, x: int, y: int) -> None:
        self.x: int = x
        self.y: int = y
    
    def get_pos(self) -> tuple[int, int]:
        return self.x, self.y

    def set_pos(self, x: int, y: int):
        self.x = x
        self.y = y