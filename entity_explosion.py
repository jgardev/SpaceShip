from quick import qk, draw, data

class Explosion:
    sprites = []

    def __init__(self, position):
        self.position = position
        self.i = 0
        self.alive = True
        self.size = qk.percent_to_pixel((8, 8))

        if len(Explosion.sprites) == 0:
            Explosion.sprites = qk.split_image(
                './assets/spritesheets/explosion.png', (16, 16))

    def draw(self, deltatime):
        if self.alive:
            self.position[1] += deltatime * data.background_speed * 2

            image = Explosion.sprites[int(
                self.i) % len(Explosion.sprites)]
            draw.effect(
                image, self.position[0], self.position[1], self.size)

            self.i += deltatime * 10
            if self.i >= len(Explosion.sprites):
                self.alive = False