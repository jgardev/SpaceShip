import math
import time
import inspect
import types
import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
import pygame
from pygame.constants import *
from pygame import display, mouse, event, transform, gfxdraw

os.environ['SDL_VIDEO_CENTERED'] = '1'

os.environ['QUICK_TEST'] = '0'


class Input:

    CLICK_TIME = 0.0
    DOUBLE_CLICK_INTERVAL = 10
    KEY_TAP_TIME = 0.0
    MOUSE_SIZE = 10

    def __init__(self, width, height):

        self._width = width
        self._height = height
        self._isfocused = True
        self._ishidden = False

        self.clicked = False
        self.double_clicked = False
        self.mouse_press = False
        self.mouse_release = False
        self.valid_interval = False
        self.click_pos = [0, 0]

        self.click_time = 0
        self.interval_time = 0

        self.tapped_keys = []
        self.pressed_keys = []
        self.released_keys = []

        self.recording = False
        self.record_keys = []
        self.record_time = 0

    def start_record(self):
        if not self.recording:
            self.recording = True
            self.record_keys = []
            self.record_time = 0
            return True
        return False

    def get_record(self):
        return [self.record_keys, self.record_time]

    def stop_record(self):
        self.recording = False

        keys = self.record_keys

        self.record_keys = []
        self.record_time = 0

        return keys

    def mouse_down(self):
        return self.mouse_press

    def mouse_up(self):
        v = self.mouse_release
        self.mouse_release = False
        return v

    def mouse_move(self):
        v = self.mouse_moved
        self.mouse_moved = False
        return v

    def mouse_position(self):
        return mouse.get_pos()

    def click(self):
        v = self.clicked
        self.clicked = False
        return v

    def click_position(self):
        return self.click_pos

    def double_click(self):
        v = self.double_clicked
        self.double_clicked = False
        return v

    def key_tap(self, key):
        for k in self.tapped_keys:
            if k == key:
                self.tapped_keys.remove(k)
                return True
        return False

    def key_down(self, key):
        for k in self.pressed_keys:
            if k[0] == key:
                return True
        return False

    def key_up(self, key):
        for k in self.released_keys:
            if k == key:
                self.released_keys.remove(k)
                return True
        return False

    def is_hover(self, width, height, x, y, mx=-1, my=-1):
        if mx == -1:
            mx = mouse.get_pos()[0]
        if my == -1:
            my = mouse.get_pos()[1]

        if x < mx + Input.MOUSE_SIZE and x + width > mx:
            if y < my + Input.MOUSE_SIZE and y + height > my:
                return True
        return False

    def update(self, deltatime):
        if self.interval_time > 0:
            self.interval_time -= deltatime * 100
            if self.interval_time < 0:
                self.interval_time = 0

        if self.recording:
            self.record_time += deltatime * 100

        for evt in event.get():
            if evt.type == pygame.QUIT:
                return False

            if evt.type == pygame.WINDOWRESIZED:
                self._width = evt.x
                self._height = evt.y

            if evt.type == pygame.WINDOWFOCUSGAINED:
                self._isfocused = True
            elif evt.type == pygame.WINDOWFOCUSLOST:
                self._isfocused = False

            if evt.type == pygame.WINDOWSHOWN:
                self._ishidden = False
            elif evt.type == pygame.WINDOWHIDDEN:
                self._ishidden = True

            if evt.type == MOUSEMOTION:
                self.mouse_moved = True
            else:
                self.mouse_moved = False

            if evt.type == MOUSEBUTTONDOWN:
                x, y = mouse.get_pos()
                self.click_pos = [x, y]
                self.mouse_release = False
                self.mouse_press = True

                self.click_time += deltatime * 100

                if self.interval_time > 0:
                    self.valid_interval = True
                    self.interval_time = 0

            elif evt.type == MOUSEBUTTONUP:
                self.mouse_release = True

                if self.click_time >= Input.CLICK_TIME:
                    if self.valid_interval:
                        self.double_clicked = True
                        self.valid_interval = False
                    else:
                        self.interval_time = Input.DOUBLE_CLICK_INTERVAL

                    self.clicked = True

                self.mouse_press = False
                self.click_time = 0

            if evt.type == KEYDOWN:
                exists = False
                for key in self.pressed_keys:
                    if key[0] == evt.key:
                        key[1] += deltatime * 100
                        exists = True
                        break
                if not exists:
                    self.pressed_keys.append([evt.key, deltatime * 100])
            elif evt.type == KEYUP:
                if self.recording:
                    self.record_keys.append(evt.key)

                for key in self.pressed_keys:
                    if key[0] == evt.key:
                        self.released_keys.append(evt.key)
                        if key[1] >= Input.KEY_TAP_TIME:
                            self.tapped_keys.append(evt.key)
                        self.pressed_keys.remove(key)
                        break
        return True


class Draw:

    def __init__(self, quick):
        self.quick = quick
        self.current_color = (255, 255, 255)
        self.sprites = []
        self.fonts = self.get_font('arial')
        self.set_font(self.fonts)

    def get_font(self, fontName_pathFont, fontLen=6, fontStep=12):
        fonts = []

        if fontName_pathFont in pygame.font.get_fonts():
            for i in range(1, fontLen+1):
                font = pygame.font.SysFont(fontName_pathFont, i*fontStep)
                fonts.append(font)
        elif os.path.exists(fontName_pathFont):
            for i in range(1, fontLen+1):
                font = pygame.font.Font(fontName_pathFont, i*fontStep)
                fonts.append(font)

        return fonts

    def set_font(self, fonts=[]):
        self.fonts = fonts

    def _notset_color(self, color):
        if color is None:
            return self.current_color
        if len(color) < 3:
            return self.current_color
        if color[0] == -1 and color[1] == -1 and color[2] == -1:
            return self.current_color
        return color

    def color(self, color):
        self.current_color = color

    def _findimage(self, image):
        for s in self.sprites:
            if s[0] == image:
                return s[1]
        return None

    def text(self, value, x, y, size=1, color=(0, 0, 0), center=False, fonts=[]):
        if len(self.fonts) == 0 and len(fonts) == 0:
            return

        font = self.fonts[size % len(self.fonts)]
        if len(fonts) != 0:
            font = fonts[size % len(fonts)]

        text = font.render(value, True, color)

        textRect = text.get_rect()
        if center:
            textRect.center = (x, y)
        else:
            textRect.top = y
            textRect.left = x

        self.quick.renderer.blit(text, textRect)
        return font.size(value)

    def text_size(self, value, size, fonts=[]):
        if len(self.fonts) == 0 and len(fonts) == 0:
            return
        font = self.fonts[size % len(self.fonts)]
        if len(fonts) != 0:
            font = fonts[size % len(fonts)]
        return font.size(value)

    def effect(self, surface, x, y, size=(-1, -1), rotation=0, scale=1, flip=(False, False)):
        texture = None
        position = (x, y)
        if size[0] < 0 and size[1] < 0:
            size[0] = surface.get_width()
            size[1] = surface.get_height()

        texture = transform.scale(surface, (int(size[0] * scale),
                                            int(size[1] * scale)))
        if rotation != 0:
            texture = transform.rotate(texture, rotation)
            position = texture.get_rect(center=(x, y))

        if flip[0]:
            texture = pygame.transform.flip(texture, True, False)

        if flip[1]:
            texture = pygame.transform.flip(texture, False, True)

        self.quick.renderer.blit(
            texture, position)

    def image(self, image, x, y):
        texture = image
        if type(texture) == str:
            texture = self._findimage(image)
            if texture is None:
                texture = pygame.image.load(image)
                self.sprites.append([image, texture])

        self.quick.renderer.blit(texture, (x, y))

    def line(self, x1, y1, x2, y2, color=(-1, -1, -1), width=1):
        c = self._notset_color(color)
        pygame.draw.line(self.quick.renderer, c, (x1, y1), (x2, y2), width)

    def rectangle(self, x, y, width, height, color=(-1, -1, -1), borderRadius=0):
        c = self._notset_color(color)
        rect = pygame.Rect(x, y, width, height)

        border_rad = borderRadius
        if rect.width < border_rad*2 or rect.height < 2*border_rad:
            border_rad = 0
        
        if border_rad == 0:
            pygame.draw.rect(self.quick.renderer, c, rect)
        else:
            pygame.gfxdraw.aacircle(
                self.quick.renderer, rect.left+border_rad, rect.top+border_rad, border_rad, c)
            pygame.gfxdraw.aacircle(
                self.quick.renderer, rect.right-border_rad-1, rect.top+border_rad, border_rad, c)
            pygame.gfxdraw.aacircle(
                self.quick.renderer, rect.left+border_rad, rect.bottom-border_rad-1, border_rad, c)
            pygame.gfxdraw.aacircle(
                self.quick.renderer, rect.right-border_rad-1, rect.bottom-border_rad-1, border_rad, c)

            pygame.gfxdraw.filled_circle(
                self.quick.renderer, rect.left+border_rad, rect.top+border_rad, border_rad, c)
            pygame.gfxdraw.filled_circle(
                self.quick.renderer, rect.right-border_rad-1, rect.top+border_rad, border_rad, c)
            pygame.gfxdraw.filled_circle(
                self.quick.renderer, rect.left+border_rad, rect.bottom-border_rad-1, border_rad, c)
            pygame.gfxdraw.filled_circle(
                self.quick.renderer, rect.right-border_rad-1, rect.bottom-border_rad-1, border_rad, c)

            rect_tmp = pygame.Rect(rect)

            rect_tmp.width -= 2 * border_rad
            rect_tmp.center = rect.center
            pygame.draw.rect(self.quick.renderer, c, rect_tmp)

            rect_tmp.width = rect.width
            rect_tmp.height -= 2 * border_rad
            rect_tmp.center = rect.center
            pygame.draw.rect(self.quick.renderer, c, rect_tmp)

    def border(self, x, y, width, height, color=(-1, -1, -1), size=1):
        c = self._notset_color(color)

        # top
        self.line(x, y, x+width, y, c, size)

        # right
        self.line(x+width, y, x+width, y+height, c, size)

        # bottom
        self.line(x, y+height, x+width, y+height, c, size)

        # left
        self.line(x, y, x, y+height, c, size)

    def circle(self, x, y, radius, color=(-1, -1, -1), border=0):
        c = self._notset_color(color)
        pygame.draw.circle(self.quick.renderer, c, (x, y), radius, border)


class Animation:

    def __init__(self, draw):
        self.dr = draw

        self.animations = []

    def create_animation(self, images, duration, start_index=1, loop=1):
        self.animations.append(
            # stop  image   duration  index       time  loop
            [False, images, duration, start_index, 0, loop])
        return len(self.animations)-1

    def reset_animation(self, id, start_index=1, loop=1):
        self.animations[id][0] = False
        self.animations[id][3] = start_index
        self.animations[id][4] = 0
        self.animations[id][5] = loop

    def draw_animation(self, id, position, deltatime, size=(-1, -1), ratotation=0, scale=1):
        if id >= len(self.animations):
            return

        animation = self.animations[id]
        if not animation[0]:
            animation[4] += deltatime * 100

            if animation[4] > animation[2]:
                animation[4] = 0
                animation[3] += 1

                if animation[3] > len(animation[1]) - 1:
                    animation[3] = animation[4]

                    if animation[5] != -1:
                        animation[5] -= 1

                        if animation[5] <= 0:
                            animation[0] = True

            index = animation[3]
            image = animation[1][index]
            self.dr.effect(image, position[0],
                           position[1], size, ratotation, scale)


class Screen:

    def __init__(self):
        self.screens = []
        self.current_screen = None

    def add_screen(self, screen):
        self.screens.append(screen)
        return len(self.screens)-1

    def set_screen(self, id):
        self.current_screen = self.screens[id]

    def game(self, input, deltatime):
        if self.current_screen:
            if isinstance(self.current_screen, types.FunctionType):
                if len(inspect.getargspec(self.current_screen).args) >= 2:
                    self.current_screen(input, deltatime)


class Data:

    def __init__(self):
        pass

    def remove_var(self, name):
        if name in self.__dict__:
            delattr(self, name)

    def set_var(self, name, value):
        setattr(self, name, value)

    def get_var(self, name):
        if name in self.__dict__:
            return self.__dict__[name]
        else:
            return None


class Utility:
    def __init__(self):
        pass

    def load_images(self, dirname, extension=['png', 'jpg', 'jpeg']):
        images = []
        for file in os.listdir(dirname):
            if file.split('.')[-1] in extension:
                image = pygame.image.load(
                    os.path.join(dirname, file)).convert_alpha()
                images.append(image)
        return images

    def split_image(self, image, size):
        images = []
        img = self.get_image(image)
        for y in range(0, img.get_height(), size[1]):
            for x in range(0, img.get_width(), size[0]):
                images.append(img.subsurface((x, y, size[0], size[1])))
        return images

    def get_image(self, image):
        if isinstance(image, str):
            if os.path.exists(image):
                img = pygame.image.load(image).convert_alpha()
                return img
        return None

    def percent_to_pixel(self, size=(0, 0), objSize=(-1, -1)):
        w = self.width
        h = self.height
        if objSize[0] != -1 and objSize[1] != -1:
            w = int(objSize[0])
            h = int(objSize[1])
        return [int(size[0] * w / 100), int(size[1] * h / 100)]

    def pc_x(self, x, w=-1):
        if w == -1:
            w = self.width
        return int(x * w / 100)

    def pc_y(self, y, h=-1):
        if h == -1:
            h = self.height
        return int(y * h / 100)

    def px_x(self, x, w=-1):
        if w == -1:
            w = self.width
        return x * 100 / w

    def px_y(self, y, h=-1):
        if h == -1:
            h = self.height
        return y * 100 / h

    def pixel_to_percent(self, size=(0, 0), objSize=(-1, -1)):
        w = self.width
        h = self.height
        if objSize[0] != -1 and objSize[1] != -1:
            w = int(objSize[0])
            h = int(objSize[1])

        return [int(size[0]) * 100 / w, int(size[1]) * 100 / h]

    def center(self, size=(0, 0)):
        w, h = qk.percent_to_pixel((50, 50))
        return [w-size[0]/2, h-size[1]/2]


class Quick(Utility):

    def __init__(self):
        Utility.__init__(self)
        pygame.init()

        self.width = 0
        self.height = 0
        self.title = ''
        self.isfocused = True
        self.ishidden = False

        self.active = False
        self.isinitialized = False

        self.renderer = None
        self.input = None

    def set_title(self, title):
        display.set_caption(title)
        self.title = title

    def init(self, width=800, height=500, title='', fullscreen=False, resize=False):
        self.width = width
        self.height = height
        self.title = title

        self.active = True
        self.isinitialized = True

        self.input = Input(width, height)

        if fullscreen:
            self.renderer = display.set_mode((width, height), FULLSCREEN |
                                             DOUBLEBUF | HWSURFACE)
        else:
            attr = HWSURFACE | DOUBLEBUF
            if resize:
                attr = HWSURFACE | DOUBLEBUF | RESIZABLE

            self.renderer = display.set_mode(
                (self.width, self.height), attr)
        display.set_caption(self.title)

    def exit(self):
        self.active = False

    def run(self, game):
        last_time = 0
        current_time = 0

        while self.active:

            current_time = float(time.time())
            deltatime = (current_time - last_time)
            last_time = current_time

            self.renderer.fill((0, 0, 0))
            self.active = self.input.update(deltatime)

            if game:
                if isinstance(game, types.FunctionType):
                    if len(inspect.getargspec(game).args) >= 2:

                        self.isfocused = self.input._isfocused
                        self.ishidden = self.input._ishidden
                        self.width = self.input._width
                        self.height = self.input._height

                        game(self.input, deltatime)

            display.flip()
        pygame.quit()


class Database:

    def __init__(self):
        pass


qk = Quick()
draw = Draw(qk)
screen = Screen()
data = Data()
animation = Animation(draw)
db = Database()

if __name__ == '__main__' and os.environ['QUICK_TEST'] == '1':
    pass
