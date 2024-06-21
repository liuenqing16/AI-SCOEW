import sys

sys.path.append("D:\install\DLAM-color\lightPattern")
from astar import *
import pygame as pg

GRAY = (169, 169, 169)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
bg = (255, 255, 255)


class AutoPattern():
    def __init__(self, width, height, radius):
        self.bg = bg
        self.pattern = BLACK
        self.pt_size = radius
        self.r = radius
        self.width = width
        self.delay = 100
        self.height = height
        self.path_width = int(radius * 3)
        self.step = max(1, self.pt_size // 20)
        self.terminal = (width, height)
        self.position = self.x, self.y = (self.width, self.height // 2)
        pg.init()
        self.screen = pg.display.set_mode((width, height))
        self.screen.fill(bg)
        pg.display.update()

    def pattern_reset(self, x, y, width):
        self.position = self.x, self.y = (x, y)
        self.pt_size = int(width)
        self.step = max(1, self.pt_size // 20)

    def set_terminal(self, terminal):
        self.terminal = terminal

    def draw_pattern(self, block_center, block_size, delay=False):
        self.screen.fill(bg)
        draw_size = block_size
        while True:
            pg.draw.rect(self.screen, BLACK,
                         (self.x - self.pt_size // 2, 0, self.pt_size, self.height), 0)
            pg.draw.rect(self.screen, GRAY,
                         (block_center[0] - draw_size, block_center[1] - draw_size, draw_size * 2, draw_size * 2), 0)
            pg.display.flip()
            keys = pg.key.get_pressed()  # get pressed key
            # press the 'w' to widen the pattern
            if keys[pg.K_q]:
                break
            if delay:
                pg.time.delay(delay)
                break
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    sys.exit()

    '''def transport_pattern(self, map, block_center, block_size):
        if self.y > self.terminal[1]:
            while True:
                self.draw_xpath(map, self.y, block_center, block_size)
                self.y -= self.step
                if self.y <= self.terminal[1]:
                    break
                pg.time.delay(100)
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        sys.exit()
        else:
            while True:
                self.draw_xpath(map, self.y, block_center, block_size)
                self.y += self.step
                if self.y >= self.terminal[1]:
                    break
                pg.time.delay(100)
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        sys.exit()'''

    def draw_pattern_x(self, block_center, block_size, delay=False):
        self.screen.fill(bg)
        x, y = self.x, self.y
        self.screen.fill(bg)
        draw_size = block_size
        keys = pg.key.get_pressed()
        if x + self.pt_size//2 < block_center[0] - draw_size or \
                x - self.pt_size//2 > block_center[0] + draw_size:
            pg.draw.rect(self.screen, BLACK, (x - self.pt_size//2, 0, self.pt_size, self.height), 0)  # draw pattern
            pg.draw.rect(self.screen, GRAY,
                         (block_center[0] - draw_size, block_center[1] - draw_size, draw_size * 2, draw_size * 2),
                         0)
            #keys = pg.key.get_pressed()  # get pressed key
            # press the 'w' to widen the pattern
        elif x + self.pt_size//2 > block_center[0] - draw_size and x < block_center[0]:
            pg.draw.rect(self.screen, BLACK, (x - self.pt_size//2, 0,
                                              self.pt_size, block_center[1] - draw_size), 0)
            pg.draw.rect(self.screen, BLACK,
                         (block_center[0] - self.pt_size - draw_size, block_center[1] - self.pt_size - draw_size,
                          x - self.pt_size//2 - (block_center[0] - self.pt_size - draw_size), self.pt_size), 0)
            pg.draw.rect(self.screen, BLACK,
                         (block_center[0] - self.pt_size - draw_size, block_center[1] - draw_size,
                          self.pt_size, self.pt_size + draw_size * 2), 0)
            pg.draw.rect(self.screen, BLACK,
                         (block_center[0] - draw_size, block_center[1] + draw_size,
                          x + self.pt_size//2 - (block_center[0] - draw_size), self.pt_size), 0)
            pg.draw.rect(self.screen, BLACK, (x - self.pt_size//2, block_center[1] + draw_size + self.pt_size,
                            self.pt_size, self.height - (block_center[1] + draw_size + self.pt_size)), 0)
            pg.draw.rect(self.screen, GRAY,
                         (block_center[0] - draw_size, block_center[1] - draw_size,
                          draw_size * 2, draw_size * 2), 0)

        elif x - self.pt_size//2 < block_center[0] + draw_size and x > block_center[0]:
            pg.draw.rect(self.screen, BLACK, (x - self.pt_size//2, 0,
                                              self.pt_size, block_center[1] - draw_size), 0)
            pg.draw.rect(self.screen, BLACK,
                         (x + self.pt_size//2, block_center[1] - draw_size - self.pt_size,
                          block_center[0] + self.pt_size + draw_size - (x + self.pt_size//2), self.pt_size), 0)
            pg.draw.rect(self.screen, BLACK, (block_center[0] + draw_size, block_center[1] - draw_size,
                                              self.pt_size, self.pt_size + draw_size * 2), 0)
            pg.draw.rect(self.screen, BLACK,
                         (x - self.pt_size//2, block_center[1] + draw_size,
                          block_center[0] + draw_size - (x - self.pt_size//2), self.pt_size), 0)
            pg.draw.rect(self.screen, BLACK, (x - self.pt_size//2, block_center[1] + draw_size + self.pt_size,
                                              self.pt_size, self.height - (block_center[1] + draw_size + self.pt_size)),
                         0)
            pg.draw.rect(self.screen, GRAY,
                         (block_center[0] - draw_size, block_center[1] - draw_size, draw_size * 2, draw_size * 2), 0)

        pg.display.flip()
            #keys = pg.key.get_pressed()

        '''elif keys[pg.K_q]:
            pass
        elif delay:
            pg.time.delay(delay)
            pass
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()'''

    def draw_pattern_y(self, delay=False):
        self.screen.fill(self.bg)
        x, y = self.x, self.y
        while True:
            pg.draw.rect(self.screen, self.pattern, (0, 0, x - self.pt_size * 3, y), 0)
            pg.draw.rect(self.screen, self.pattern, (
            x + self.pt_size * 3, y - self.pt_size, self.width - x - self.pt_size * 3, self.height - y + self.pt_size),
                         0)
            pg.draw.rect(self.screen, self.pattern,
                         (x - self.pt_size * 3, y - self.pt_size, self.pt_size * 6, self.pt_size), 0)
            pg.display.flip()
            keys = pg.key.get_pressed()  # get pressed key
            # press the 'w' to widen the pattern
            if keys[pg.K_q]:
                break
            if delay:
                pg.time.delay(delay)
                break
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    sys.exit()

    # define functions of pattern's moving control
    def move_left(self):
        x, y = self.x, self.y
        self.screen.fill(self.bg)
        # pg.draw.rect(screen, pttern, (x - pt_size, y, 2 * pt_size, 3 * pt_size), 0)
        pg.draw.rect(self.screen, self.pattern, (x, 0, self.pt_size, self.height), 0)  # draw pattern
        pg.display.flip()

    def move_right(self):
        x, y = self.x, self.y
        self.screen.fill(self.bg)
        # pg.draw.rect(screen, pttern, (x - pt_size, y - 2 * pt_size, 2 * pt_size, 3 * pt_size), 0)
        pg.draw.rect(self.screen, self.pattern, (x + self.step, 0, self.pt_size, self.height), 0)
        pg.display.flip()

    def move_up(self):
        x, y = self.x, self.y
        self.screen.fill(self.bg)
        # pg.draw.rect(screen, pttern, (x - pt_size, y - 2 * pt_size, 2 * pt_size, 3 * pt_size), 0)
        pg.draw.rect(self.screen, self.pattern, (0, 0, x - self.pt_size * 3, y + self.pt_size//2), 0)
        pg.draw.rect(self.screen, self.pattern,
                     (x + self.pt_size * 3, y - self.pt_size//2, self.width - x - self.pt_size * 3, self.height - (y - self.pt_size)), 0)
        pg.draw.rect(self.screen, self.pattern,
                     (x - self.pt_size * 3, y - self.pt_size//2, self.pt_size * 6, self.pt_size), 0)
        pg.display.flip()

    def move_down(self):
        x, y = self.x, self.y
        self.screen.fill(self.bg)
        # pg.draw.rect(screen, pttern, (x - pt_size, y - 2 * pt_size, 2 * pt_size, 3 * pt_size), 0)
        pg.draw.rect(self.screen, self.pattern, (0, 0, x - self.pt_size * 3, y + self.pt_size//2), 0)
        pg.draw.rect(self.screen, self.pattern,
                     (x + self.pt_size * 3, y - self.pt_size//2, self.width - x - self.pt_size * 3, self.height - (y - self.pt_size)), 0)
        pg.draw.rect(self.screen, self.pattern,
                     (x - self.pt_size * 3, y - self.pt_size//2, self.pt_size * 6, self.pt_size), 0)
        pg.display.flip()

    def draw_blank(self):
        self.screen.fill(self.bg)
        # pg.draw.rect(screen, pttern, (x - pt_size, y - 2 * pt_size, 2 * pt_size, 3 * pt_size), 0)
        #pg.draw.rect(self.screen, self.pattern, (0, 0, 1, 1), 0)
        pg.display.flip()


    def size_up(self):
        self.pt_size += 1
        self.screen.fill(self.bg)
        pg.draw.rect(self.screen, self.pattern, (self.x, 0, self.pt_size, self.height), 0)

    def size_down(self):
        self.pt_size -= 1
        self.screen.fill(self.bg)
        pg.draw.rect(self.screen, self.pattern, (self.x, 0, self.pt_size, self.height), 0)

    def speed_up(self):
        if self.delay > 20:
            self.delay -= 20

    def speed_down(self):
        if self.delay < 300:
            self.delay += 20

    def manual_set(self):
        keys = pg.key.get_pressed()  # get pressed key
        # press the 'w' to widen the pattern
        if keys[pg.K_w]:
            self.size_up()

        # press the 's' to slim the pattern
        elif keys[pg.K_s]:
            self.size_down()

        elif keys[pg.K_a]:
            self.speed_up()

        elif keys[pg.K_d]:
            self.speed_down()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()

        if keys[pg.K_e]:
            sys.exit()

    '''def draw_xpath(self, map, y, block_center, block_size):
        path_width = self.path_width
        screen = self.screen
        source = (block_center[0] - block_size, y)
        dest = (block_center[0] + block_size, y)
        best_path = AStarSearch(map, source, dest)
        self.screen.fill(bg)
        draw_size = block_size - path_width // 2
        # block_size = block_size - path_width // 2
        pg.draw.rect(screen, GRAY, (block_center[0] - draw_size, block_center[1] - draw_size, draw_size * 2, draw_size * 2), 0)  # draw all the droplets trapped before and turn gray

        pg.draw.rect(screen, BLACK,(0, y - path_width // 2, block_center[0] - block_size, path_width), 0)
        pg.draw.rect(screen, BLACK, (block_center[0] + block_size, y - path_width // 2, self.width - block_center[0] - block_size, path_width), 0)

        for j in range(len(best_path) - 1):
            path_x, path_y = best_path[j]
            pg.draw.rect(screen, BLACK, (path_x - path_width // 2, path_y - path_width // 2, path_width, path_width), 0)
        # pg.draw.circle(screen, BLUE, (x, y), r)
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
            radius = block_radius[i]
            pg.draw.rect(screen, GRAY, (block_x[i] - radius, block_y[i] - radius, radius * 2, radius * 2),
                         0)  # draw all the droplets trapped before and turn gray

        for j in range(len(best_path_1)):
            path_x, path_y = best_path_1[j]
            pg.draw.rect(screen, BLACK, (path_x - path_width, path_y - path_width, path_width * 2, path_width), 0)
        for k in range(len(best_path_2)):
            path_x, path_y = best_path_2[k]
            pg.draw.rect(screen, BLACK, (path_x - path_width, path_y - path_width, path_width * 2, path_width*2), 0)
        pg.draw.rect(screen, BLACK, (x - r * 2 - path_width, y- path_width, r * 4, path_width * 2), 0)
        pg.draw.circle(screen, BLUE, (x, y), r)
        pg.display.update()'''
