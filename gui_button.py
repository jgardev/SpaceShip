import copy
from gui_styles import Style
from quick import qk, draw, data


class Button:
    def __init__(self, default_style, hover_style, click_style):
        self.style = default_style
        self.hover = hover_style
        self.click = click_style

        self.current = default_style

    def draw(self, input, deltatime):
        if input.is_hover(self.current.size[0], self.current.size[1], self.current.position[0], self.current.position[1]):

            if input.mouse_down():
                self.current = self.click
            elif input.click():
                mx, my = input.click_position()
                if input.is_hover(self.current.size[0], self.current.size[1], self.current.position[0], self.current.position[1], mx, my):
                    return True
            else:
                self.current = self.hover
        else:
            self.current = self.style

        draw.rectangle(self.current.position[0], self.current.position[1],
                       self.current.size[0], self.current.size[1],
                       self.current.color)

        draw.border(self.current.position[0], self.current.position[1],
                    self.current.size[0], self.current.size[1],
                    self.current.borderColor, self.current.borderSize)
        draw.text(self.current.text,
                  self.current.position[0] + self.current.size[0] /
                  2, self.current.position[1] +
                  self.current.size[1]/2, self.current.textSize,
                  self.current.textColor, True)

        return False
    


def add_btn(var_name, text, position):
    default_s = Style()
    default_s.size = qk.percent_to_pixel((30, 8))
    default_s.position = qk.center(default_s.size)
    default_s.color = (200, 200, 200)
    default_s.borderColor = (0, 0, 0)
    default_s.borderSize = 1
    default_s.textColor = (0, 0, 0)
    default_s.textSize = 4
    default_s.text = text

    default_s.position[1] += position

    hover_s = copy.copy(default_s)
    hover_s.color = (180, 180, 180)

    data.set_var(var_name, Button(
        copy.copy(default_s), copy.copy(hover_s), copy.copy(default_s)))
