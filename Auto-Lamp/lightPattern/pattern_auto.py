import pygame as pg
from pygame.locals import *
import sys


class Pattern():
    def __init__(self, pt_size):
        pg.init()
        self.bg = (255, 255, 255)      # set the backgroud color
        self.pttern = (0, 0, 0)     # set the pattern color
        self.delay = 300         # initial time delay
        self.size = self.width, self.height = 740, 740       # the size of background
        self.pt_size = pt_size  # the size of pattern
        self.step = self.pt_size // 20      # the step length of pattern's moving
        self.position = self.x, self.y = (self.width // 2, self.height)  # initial position of pattern

        # screen initialization
        self.screen = pg.display.set_mode(self.size, flags = RESIZABLE)
        self.screen.fill(self.bg)
        pg.display.update()

    def pattern_reset(self, x, y, width):
        self.position = self.x, self.y = (x, y)
        self.pt_size = int(width)
        self.step = self.pt_size // 10

    def draw_pattern(self, delay = False):
        self.screen.fill(self.bg)
        x, y = self.x, self.y
        while True:
            pg.draw.rect(self.screen, self.pttern, (0, y, self.width, self.pt_size), 0)     # draw pattern
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
    def move_up(self):
        x, y = self.x, self.y
        self.screen.fill(self.bg)
        # pg.draw.rect(screen, pttern, (x - pt_size, y, 2 * pt_size, 3 * pt_size), 0)
        pg.draw.rect(self.screen, self.pttern, (0, y, self.width, self.pt_size), 0)                # draw pattern
        pg.display.flip()

    def move_down(self):
        x, y = self.x, self.y
        self.screen.fill(self.bg)
        # pg.draw.rect(screen, pttern, (x - pt_size, y - 2 * pt_size, 2 * pt_size, 3 * pt_size), 0)
        pg.draw.rect(self.screen, self.pttern, (0, y + self.step, self.width, self.pt_size), 0)
        pg.display.flip()

    def size_up(self):
        self.pt_size += 1
        self.screen.fill(self.bg)
        pg.draw.rect(self.screen, self.pttern, (self.x, 0, self.pt_size, self.height), 0)

    def size_down(self):
        self.pt_size -= 1
        self.screen.fill(self.bg)
        pg.draw.rect(self.screen, self.pttern, (self.x, 0, self.pt_size, self.height), 0)

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


    def auto_move(self):
        while True:
            while self.y - 3 * self.pt_size > 0:
                pg.time.delay(self.delay)
                self.move_up()
                self.y -= self.step
                self.manual_set()

            while self.y + self.pt_size < self.height:
                pg.time.delay(self.delay)
                self.move_down()
                self.y += self.step
                self.manual_set()

            self.manual_set()


if __name__ == '__main__':
    pattern = Pattern(30)
    pattern.pattern_reset(300,300,30)
    pattern.draw_pattern()
    pattern.auto_move()


