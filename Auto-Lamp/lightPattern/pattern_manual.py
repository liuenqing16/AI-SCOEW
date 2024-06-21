import pygame as pg
from pygame.locals import *
import sys

pg.init()

pttern = (255, 255, 255)      # set the backgroud color
bg = (0, 0, 0)     # set the pattern color

size = width, height = 580,580       # the size of background
pt_size = width // 100     # the size of pattern
step = pt_size // 8     # the step length of pattern's moving

# screen initialization
screen = pg.display.set_mode(size, flags = RESIZABLE)
screen.fill(bg)
pg.display.update()

# define functions of pattern's moving control
def move_up(position, pt_size):
    x, y = position
    screen.fill(bg)
    # pg.draw.rect(screen, pttern, (x - pt_size, y, 2 * pt_size, 3*pt_size), 0)
    pg.draw.rect(screen, pttern, (0, y, width, pt_size), 0)                # draw pattern
    pg.display.flip()

def move_down(position, pt_size):
    x, y = position
    screen.fill(bg)
    # pg.draw.rect(screen, pttern, (x - pt_size, y - 2*pt_size, 2 * pt_size, 3*pt_size), 0)
    pg.draw.rect(screen, pttern, (0, y + step, width, pt_size), 0)
    pg.display.flip()

'''
def move_left(position, pt_size):
    x, y = position
    screen.fill(bg)
    # pg.draw.rect(screen, pttern, (x, y - pt_size, 2*pt_size, 4*pt_size), 0)
    pg.draw.rect(screen, pttern, (0, y - 2*pt_size, width, pt_size), 0)

    pg.display.flip()

def move_right(position, pt_size):
    x, y = position
    screen.fill(bg)
    # pg.draw.rect(screen, pttern, (x - 2*pt_size, y - pt_size, 2*pt_size, 4*pt_size), 0)
    pg.draw.rect(screen, pttern, (0, y - 2*pt_size, width, pt_size), 0)
    pg.display.flip()
'''
# the function of split mode: double pattern width
def split(position, pt_size):
    x, y = position
    screen.fill(bg)
    pg.draw.rect(screen, pttern, (x - pt_size, 0, 2*pt_size, height), 0)
    pg.display.flip()

# initial position of pattern
position = x_p, y_p =  (width // 2, height)

while True:
    pg.time.delay(50)
    x, y = position
    keys = pg.key.get_pressed()   # get pressed key
    # press the 'w' to widen the pattern
    if keys[pg.K_w]:
        pt_size *= 1.1
        screen.fill(bg)
        pg.draw.rect(screen, pttern, (x, 0, pt_size, height), 0)
    # press the 's' to slim the pattern
    elif keys[pg.K_s]:
        pt_size *= 0.9
        screen.fill(bg)
        pg.draw.rect(screen, pttern, (x, 0, pt_size, height), 0)
    # elif keys[pg.K_LEFT]:
    #     move_left(position, pt_size)
    #     x_p -= step
    # elif keys[pg.K_RIGHT]:
    #     move_right(position, pt_size)
    #     x_p += step
    elif keys[pg.K_LEFT]:
        move_up(position, pt_size)
        y_p -= step
    elif keys[pg.K_RIGHT]:
        move_down(position, pt_size)
        y_p += step
    # print space key entry split mode
    elif keys[pg.K_SPACE]:
        split(position, pt_size)

    # set the state when pattern reach the edge of screen
    if x_p < pt_size:
        x_p = pt_size
    elif x_p > width - pt_size:
        x_p = width - pt_size
    elif y_p < pt_size:
        y_p = pt_size
    elif y_p > height - pt_size:
        y_p = height - pt_size

    # update the position
    position = (x_p, y_p)

    # exit the program
    pg.display.update()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()





