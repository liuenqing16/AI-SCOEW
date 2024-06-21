from astar import *
import pygame as pg
from pygame.locals import *
import sys

x = r = path_width = 2
y = 50
width, height = 150, 100
size = width * 10, height * 10
map = Map(width, height)
# block_x, block_y, block_radius = map.createBlock((75, 50), 10, path_width)
path_width *= 8
step = 1

pg.init()

GRAY = (169, 169, 169)
BLACK = (0, 0, 0)
bg = (255, 255, 255)


screen = pg.display.set_mode(size)
screen.fill(bg)

pg.display.update()
pg.time.delay(500)

def draw_xpath(x):
    source = (x, 0)
    dest = (x, height - 1)
    best_path = AStarSearch(map, source, dest)
    screen.fill(bg)
    '''
    for i in range(len(block_x)):
        radius = block_radius[i] * 10
        pg.draw.rect(screen, GRAY, (block_x[i] * 10 - radius, block_y[i] * 10 - radius, radius * 2, radius * 2),
                     0)  # draw all the droplets trapped before and turn gray
    '''
    for j in range(len(best_path)):
        path_x, path_y = best_path[j]
        path_x *= 10
        path_y *= 10
        pg.draw.rect(screen, BLACK, (path_x - path_width, path_y - path_width, path_width * 2, max(10, path_width*2)), 0)

    pg.display.update()

def draw_ypath(x, y):
    source_1 = (x - r*3, 0)
    dest_1 = (x - r*3, y - 1)
    source_2 = (x + r*3, y)
    dest_2 = (x + r*3, height - 1)
    best_path_1 = AStarSearch(map, source_1, dest_1)
    best_path_2 = AStarSearch(map, source_2, dest_2)
    screen.fill(bg)
    '''
    for i in range(len(block_x)):
        radius = block_radius[i] * 10
        pg.draw.rect(screen, GRAY, (block_x[i] * 10 - radius, block_y[i] * 10 - radius, radius * 2, radius * 2),
                     0)  # draw all the droplets trapped before and turn gray
    '''
    for j in range(len(best_path_1)):
        path_x, path_y = best_path_1[j]
        path_x *= 10
        path_y *= 10
        pg.draw.rect(screen, BLACK, (path_x - path_width, path_y - path_width, path_width * 2, max(10, path_width*2)), 0)
    for k in range(len(best_path_2)):
        path_x, path_y = best_path_2[k]
        path_x *= 10
        path_y *= 10
        pg.draw.rect(screen, BLACK, (path_x - path_width, path_y - path_width, path_width * 2, max(10, path_width*2)), 0)
    pg.draw.rect(screen, BLACK, (x * 10 - r*30 - path_width, y * 10 - path_width, r * 60, path_width * 2), 0)
    pg.display.update()

while True:
    best_path = []

    pg.time.delay(300)
    keys = pg.key.get_pressed()
    if keys[pg.K_LEFT]:
        x -= step
        draw_xpath(x)
    elif keys[pg.K_RIGHT]:
        x += step
        draw_xpath(x)
    elif keys[pg.K_UP]:
        draw_ypath(x, y + r)
        y -= step
    elif keys[pg.K_DOWN]:
        draw_ypath(x, y - r)
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



