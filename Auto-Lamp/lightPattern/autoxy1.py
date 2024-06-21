import pygame as pg
from pygame.locals import *
import sys


class Pattern():
    def __init__(self):
        pg.init()
        self.bg = (255, 255, 255)      # set the backgroud color
        self.pttern = (0, 0, 0)     # set the pattern color
        self.delay = 300         # initial time delay
        self.size = self.width, self.height = 720, 720       # the size of background
        self.pt_size = self.width // 50     # the size of pattern
        self.step = 2      # the step length of pattern's moving
        self.position = self.x, self.y = (self.width // 2, self.height // 2)  # initial position of pattern

        # screen initialization
        self.screen = pg.display.set_mode(self.size, flags = RESIZABLE)
        self.screen.fill(self.bg)
        pg.display.update()

    def position_reset(self, x, y):
        self.position = self.x, self.y = (x, y)

    def draw_pattern(self):
        x, y = self.x, self.y
        while True:
            pg.draw.rect(self.screen, self.pttern, (0,self.y-4*self.pt_size,x-self.pt_size ,self.pt_size), 0)
            pg.draw.rect(self.screen, self.pttern, (self.y-self.pt_size,self.y-4 * self.pt_size,self.pt_size,9*self.pt_size), 0)
            pg.draw.rect(self.screen, self.pttern, (self.y,self.y+4 * self.pt_size,self.width//2, self.pt_size ), 0)
            pg.display.flip()
            keys = pg.key.get_pressed()  # get pressed key
            # press the 'w' to widen the pattern
            if keys[pg.K_q]:
                break
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    sys.exit()

    # define functions of pattern's moving control
    def move_up(self):
        x, y = self.x, self.y
        self.screen.fill(self.bg)
        pg.draw.rect(self.screen, self.pttern, (0,self.y, self.width,self.y), 0)
        pg.display.flip()
    def move_down(self):
        x, y = self.x, self.y
        self.screen.fill(self.bg)
        pg.draw.rect(self.screen, self.pttern, (0,self.y, self.width,self.y), 0)
        pg.display.flip()
    def move_left(self):
        x,y=self.x,self.y
        self.screen.fill(self.bg)
        pg.draw.rect(self.screen, self.pttern, (0, self.y - 4 * self.pt_size, x - self.pt_size, self.pt_size),0)
        pg.draw.rect(self.screen, self.pttern,(x - self.pt_size, self.y - 4 * self.pt_size, self.pt_size, 9 * self.pt_size), 0)
        pg.draw.rect(self.screen, self.pttern,(x, self.y + 4 * self.pt_size, self.width-x, self.pt_size), 0)
        pg.display.flip()

    def move_right(self):
        x, y = self.x, self.y
        self.screen.fill(self.bg)
        pg.draw.rect(self.screen, self.pttern,(0, self.y - 4 * self.pt_size, x - self.pt_size, self.pt_size), 0)
        pg.draw.rect(self.screen, self.pttern,(x - self.pt_size, self.y - 4 * self.pt_size, self.pt_size, 9 * self.pt_size), 0)
        pg.draw.rect(self.screen, self.pttern,(x, self.y + 4 * self.pt_size, self.width - x, self.pt_size), 0)
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

        elif keys[pg.K_UP]:
            self.y -= 2*self.step
        elif keys[pg.K_DOWN]:
            self.y += 2*self.step

        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()


    def auto_move(self):
        while True:
            while self.x - 3 * self.pt_size > 0:
                pg.time.delay(self.delay)
                self.move_left()
                self.x-= self.step
                self.manual_set()


            while self.x + self.pt_size < self.width:
                pg.time.delay(self.delay)
                self.move_right()
                self.x+= self.step
                self.manual_set()

            self.manual_set()


if __name__ == '__main__':
    pattern = Pattern()
    # pattern.position_reset(300,300)
    pattern.draw_pattern()
    pattern.auto_move()

