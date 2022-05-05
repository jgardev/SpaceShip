from quick import draw


class InputKeyBoard:

    def __init__(self, key, position, size, color, color_active):
        self.key = key
        self.position = position
        self.size = size
        self.color = color
        self.color_active = color_active
        self.active = False

    def draw(self, input):

        if not self.active:
            if input.is_hover(self.size[0], self.size[1], self.position[0], self.position[1]):
                if input.click():

                    mx, my = input.click_position()
                    if input.is_hover(self.size[0], self.size[1], self.position[0], self.position[1], mx, my):
                        self.active = True
        else:
            if input.click():
                input.stop_record()
                self.active = False

            if not input.start_record():
                if len(input.get_record()[0]) > 0:
                    key = input.stop_record()[0]
                    if key >= 65 and key <= 122:
                        self.key = key
                        self.active = False
                        return self.key

        draw.rectangle(self.position[0], self.position[1],
                       self.size[0], self.size[1],
                       self.color_active if self.active else self.color)

        draw.border(self.position[0], self.position[1],
                    self.size[0], self.size[1],
                    (0, 0, 0))

        draw.text(chr(self.key).upper(),
                  self.position[0] + self.size[0] / 2,
                  self.position[1] + self.size[1]/2, 5,
                  (0, 0, 0), True)

        return None