from quick import qk, draw, screen, data
import os
import datetime



def dbg(message, title='INFO'):
    if os.environ['SPACESHIP_DEBUG'] == '1':
        print('({3}) {0}/{1}: {2}'.format(datetime.datetime.now(),
              title, message, os.getpid()))








