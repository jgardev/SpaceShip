from screens import ScreenTypes
from quick import qk, draw, screen, data
from util import dbg

def screen_settings(input, deltatime):
    size = qk.percent_to_pixel((100, 100))
    draw.rectangle(0, 0, size[0], size[1], (50, 50, 50))

    if data.btn_back_home.draw(input, deltatime):
        screen.set_screen(ScreenTypes.HOME)

    upperTextSize = draw.text_size('A', 4)[1]

    draw.text('LEFT',
              qk.pc_x(50) - data.left_key.size[0],
              data.left_key.position[1] + upperTextSize/2,
              4, (255, 255, 255))
    draw.text('RIGHT',
              qk.pc_x(50) - data.right_key.size[0],
              data.right_key.position[1] + upperTextSize/2,
              4, (255, 255, 255))
    draw.text('FIRE',
              qk.pc_x(50) - data.fire_key.size[0],
              data.fire_key.position[1] + upperTextSize/2,
              4, (255, 255, 255))
    draw.text('DEBUG',
              qk.pc_x(50) - data.debug_key.size[0],
              data.debug_key.position[1] + upperTextSize/2,
              4, (255, 255, 255))

    # TODO save key to file
    if data.left_key.draw(input) != None:
        dbg('Change left key to {0}'.format(
            data.left_key.key), 'SettingsUpdate')

    if data.right_key.draw(input) != None:
        dbg('Change right key to {0}'.format(
            data.right_key.key), 'SettingsUpdate')

    if data.fire_key.draw(input) != None:
        dbg('Change fire key to {0}'.format(
            data.fire_key.key), 'SettingsUpdate')

    if data.debug_key.draw(input) != None:
        dbg('Change debug key to {0}'.format(
            data.debug_key.key), 'SettingsUpdate')

    return 0