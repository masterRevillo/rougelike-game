class Camera:
    def __init__(self, x: int, y: int, width: int, height: int, map_width: int, map_height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.map_width = map_width
        self.map_height = map_height

    def apply(self, x, y):
        x = x + self.x
        y = y + self.y
        return (x, y)

    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def update(self, entity):
        x = -entity.x + int(self.width / 2)
        y = -entity.y + int(self.height / 2)

        # TODO add limits to stop camera near map edges

        self.x, self.y = (x, y)