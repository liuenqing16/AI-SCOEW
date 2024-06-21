import pygame as pg
from pygame.locals import *
import sys

pg.init()

circle = (255, 255, 255)      # set the backgroud color
bg = (0, 0, 0)     # set the pattern color

size = width, height = 1900, 1000       # the size of background
radius = 50     # the size of pattern
step = 5     # the step length of pattern's moving

# screen initialization
screen = pg.display.set_mode(size, flags = RESIZABLE)
screen.fill(bg)
pg.display.update()

# initial position of pattern
position = x, y =  (radius, height // 2)

while True:

    pg.time.delay(50)

    keys = pg.key.get_pressed()

    if keys[pg.K_LEFT]:
        x -= step
    elif keys[pg.K_RIGHT]:
        x += step
    elif keys[pg.K_UP]:
        y -= step
    elif keys[pg.K_DOWN]:
        y += step

    if keys[pg.K_s]:
        radius -= 2
    elif keys[pg.K_l]:
        radius += 2
    if x < radius:
        x = radius
    if x > width - radius:
        x = width - radius
    if y < radius:
        y = radius
    if y > height - radius:
        y = height - radius

    center = x, y

    screen.fill(bg)
    pg.draw.circle(screen, circle, center, radius)  # generate a new droplet
    pg.display.update()


    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()
