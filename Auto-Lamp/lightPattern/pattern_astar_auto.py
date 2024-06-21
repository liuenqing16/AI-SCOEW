from astar import *
import pygame as pg
import sys

GRAY = (169, 169, 169)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
bg = (255, 255, 255)
factor = 5


class AutoPattern():
    def __init__(self, width, height, path_width, radius):
        self.r = radius
        self.width = width
        self.height = height
        self.path_width = path_width * factor
        self.size = width * factor, height * factor
        pg.init()
        self.screen = pg.display.set_mode(self.size)
        self.screen.fill(bg)
        pg.display.update()

    def transport_pattern(self, map, path):
        for i in range(len(path) - 1, 0, -1):
            loc_n = path[i]
            loc_last = path[i-1]
            x, y = loc_n[0], loc_n[1]
            if x > loc_last[0]:
                self.draw_xpath(map, x, y)
            elif x < loc_last[0]:
                self.draw_xpath(map, x, y)
            elif y > loc_last[1]:
                self.draw_ypath(map, x, y - self.r)
            elif y < loc_last[1]:
                self.draw_ypath(map, x, y + self.r)
            pg.time.delay(200)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    sys.exit()

    def draw_xpath(self, map, x, y):
        path_width = self.path_width
        screen = self.screen
        r = self.r
        source = (x, 0)
        dest = (x, self.height - 1)
        best_path = AStarSearch(map, source, dest)
        self.screen.fill(bg)
        for i in range(len(block_x)):
            radius = block_radius[i] * factor
            pg.draw.rect(screen, GRAY, (block_x[i] * factor - radius, block_y[i] * factor - radius, radius * 2, radius * 2),
                         0)  # draw all the droplets trapped before and turn gray

        for j in range(len(best_path)):
            path_x, path_y = best_path[j]
            path_x *= factor
            path_y *= factor
            pg.draw.rect(screen, BLACK, (path_x - path_width, path_y - path_width, path_width * 2, max(factor, path_width*2)), 0)
        pg.draw.circle(screen, BLUE, (x * factor, y * factor), r * factor)
        pg.display.update()

    def draw_ypath(self, map, x, y):
        path_width = self.path_width
        screen = self.screen
        r = self.r
        source_1 = (x - r*2, 0)
        dest_1 = (x - r*2, y - 1)
        source_2 = (x + r*2, y)
        dest_2 = (x + r*2, self.height - 1)
        best_path_1 = AStarSearch(map, source_1, dest_1)
        best_path_2 = AStarSearch(map, source_2, dest_2)
        screen.fill(bg)
        for i in range(len(block_x)):
            radius = block_radius[i] * factor
            pg.draw.rect(screen, GRAY, (block_x[i] * factor - radius, block_y[i] * factor - radius, radius * 2, radius * 2),
                         0)  # draw all the droplets trapped before and turn gray

        for j in range(len(best_path_1)):
            path_x, path_y = best_path_1[j]
            path_x *= factor
            path_y *= factor
            pg.draw.rect(screen, BLACK, (path_x - path_width, path_y - path_width, path_width * 2, max(factor, path_width*2)), 0)
        for k in range(len(best_path_2)):
            path_x, path_y = best_path_2[k]
            path_x *= factor
            path_y *= factor
            pg.draw.rect(screen, BLACK, (path_x - path_width, path_y - path_width, path_width * 2, max(factor, path_width*2)), 0)
        pg.draw.rect(screen, BLACK, (x * factor - r * 2 * factor - path_width, y * factor - path_width, r * 4 * factor, path_width * 2), 0)
        pg.draw.circle(screen, BLUE, (x * factor, y * factor), r * factor)
        pg.display.update()