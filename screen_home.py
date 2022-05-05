import time
import os
from quick import qk, draw, screen, data
from screens import ScreenTypes


def screen_home(input, deltatime):
    size = qk.percent_to_pixel((100, 100))
    draw.rectangle(0, 0, size[0], size[1], (50, 50, 50))

    if os.environ['USERNAME'] and len(os.environ['USERNAME']) <= 25:
        draw.text('Wellcome {0} to SpaceShip !'.format(
            os.environ['USERNAME'].capitalize()), qk.pc_x(50), qk.pc_y(10), 8, (255, 255, 255), True)
    else:
        draw.text('Wellcome to SpaceShip !', qk.pc_x(50),
                  qk.pc_y(10), 10, (255, 255, 255), True)

    if data.btn_play.draw(input, deltatime):
        data.start_time = time.time()
        screen.set_screen(ScreenTypes.GAME)

    if data.btn_settings.draw(input, deltatime):
        screen.set_screen(ScreenTypes.SETTINGS)

    if data.btn_quit.draw(input, deltatime):
        qk.exit()

    if len(data.score_board) != 0:
        i = 1
        startX = 50
        startY = 50
        colorBoard = (200, 200, 200)
        boardData = [['Score', 'Time']]+data.score_board
        for score in boardData:
            i += 1
            draw.border(startX,
                        startY + i*qk.pc_y(5),
                        qk.pc_x(20),
                        qk.pc_y(5),
                        colorBoard)

            draw.line(startX+qk.pc_x(10),
                      startY+i*qk.pc_y(5),
                      startX + qk.pc_x(10),
                      startY + (i+1)*qk.pc_y(5),
                      colorBoard)

            tsize = draw.text_size(str(score[0]), 2)

            draw.text(str(score[0]),
                      startX + qk.pc_x(5) - (tsize[0]/2),
                      startY + i * qk.pc_y(5) + (tsize[1]/2),
                      2,
                      colorBoard)

            tsize = draw.text_size(str(score[1]), 2)
            draw.text(str(score[1]),
                      startX + qk.pc_x(15) - (tsize[0]/2),
                      startY+ i * qk.pc_y(5) + (tsize[1]/2),
                      2, colorBoard)

    return 0
