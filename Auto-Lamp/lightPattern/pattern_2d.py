import pygame as pg
from pygame.locals import *
import sys

x = r = path_width = 20
y = 50
size = width, height = 580, 1000
# block_x, block_y, block_radius = map.createBlock((75, 50), 10, path_width)
step = 2

pg.init()

GRAY = (169, 169, 169)
BLACK = (0, 0, 0)
bg = (255, 255, 255)

screen = pg.display.set_mode(size)
screen.fill(bg)

pg.display.update()
pg.time.delay(100)

def draw_xpath(x):
    screen.fill(bg)
    pg.draw.rect(screen, BLACK, (x, 0, path_width, height), 0)
    pg.draw.rect(screen, BLACK, (0, 0, width, 100), 0)
    pg.draw.rect(screen, BLACK, (0, 200, width, 100), 0)
    pg.draw.rect(screen, BLACK, (0, 400, width, 100), 0)


    pg.display.update()

def draw_ypath(x, y):
    screen.fill(bg)
    pg.draw.rect(screen, BLACK, (0, 0, x-path_width*4, y), 0)
    pg.draw.rect(screen, BLACK, (x + path_width * 4, y-path_width , width-x-path_width*4, height-y), 0)
    pg.draw.rect(screen, BLACK, (x - path_width*4, y-path_width, path_width * 8, path_width), 0)
    pg.display.update()

while True:
    pg.time.delay(100)
    keys = pg.key.get_pressed()
    if keys[pg.K_LEFT]:
        x -= step
        draw_xpath(x)
    elif keys[pg.K_RIGHT]:
        x += step
        draw_xpath(x)
    elif keys[pg.K_UP]:
        draw_ypath(x, y)
        y -= step
    elif keys[pg.K_DOWN]:
        draw_ypath(x, y)
        y += step

    if keys[pg.K_w]:
        path_width += 1
    elif keys[pg.K_s]:
        path_width -= 1
    if x > width - path_width:
        x = width - path_width
    elif x < path_width:
        x = path_width
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()
