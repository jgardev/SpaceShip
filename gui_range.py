from quick import qk, draw, screen, data

class Range:

    def __init__(self, size, position, color, value=0):
        self.value = value
        self.size = size
        self.position = position
        self.color = color

    def add(self, v=1):
        self.value += v

    def sub(self, v=1):
        self.value -= v

    def draw(self):
        if self.value < 0:
            self.value = 0
        elif self.value > 100:
            self.value = 100

        size = (self.size[0]*self.value)/100

        draw.rectangle(
            self.position[0], self.position[1],
            size, self.size[1],
            self.color)

        draw.border(self.position[0], self.position[1],
                    self.size[0], self.size[1],
                    (0, 0, 0))