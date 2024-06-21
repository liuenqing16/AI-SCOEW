import pygame as pg
from pygame.locals import *
import sys

pg.init()

bg = (255, 255, 255)      # set the backgroud color
pttern = (0, 0, 0)     # set the pattern color

size = width, height = 580,580# the size of background
pt_size = width // 20     # the size of pattern
step = pt_size // 20     # the step length of pattern's moving

# screen initialization
screen = pg.display.set_mode(size, flags = RESIZABLE)
screen.fill(bg)
pg.display.update()


# initial position of pattern
position_1 = x1_p, y1_p =  (0, height)
position_2 = x2_p, y2_p =  (0, 0)

while True:
    pg.time.delay(50)
    x1_p, y1_p = position_1
    x2_p, y2_p = position_2
    keys = pg.key.get_pressed()   # get pressed key
    # press the 'w' to widen the pattern
    if keys[pg.K_w]:
        pt_size *= 1.1

    # press the 's' to slim the pattern
    elif keys[pg.K_s]:
        pt_size *= 0.9


    if keys[pg.K_LEFT]:
        y1_p -= step
    elif keys[pg.K_RIGHT]:
        y1_p += step
    if keys[pg.K_a]:
        y2_p -= step
    elif keys[pg.K_d]:
        y2_p += step

    if y1_p < pt_size:
        y1_p = pt_size
    elif y1_p > height - pt_size:
        y1_p = height - pt_size
    if y2_p < pt_size:
        y2_p = pt_size
    elif y2_p > height - pt_size:
        y2_p = height - pt_size
    # update the position
    position_1 = (x1_p, y1_p)
    position_2 = (x2_p, y2_p)
    screen.fill(bg)
    pg.draw.rect(screen, pttern, (0, y1_p + step, width, pt_size), 0)
    pg.draw.rect(screen, pttern, (0, y2_p + step, width, pt_size), 0)
    # exit the program
    pg.display.update()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()
