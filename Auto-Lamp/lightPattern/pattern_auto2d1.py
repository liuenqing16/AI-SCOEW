import pygame as pg
from pygame.locals import *
import sys


class Pattern:
    def __init__(self, pt_size1, pt_size2, pt_size3, ):

        pg.init()
        self.bg = (255, 255, 255)      # set the backgroud color
        self.pattern = (0, 0, 0)     # set the pattern color
        self.delay = 125      # initial time delay
        self.size = self.width, self.height = 580, 650     # the size of background
        self.pt_size1 = pt_size1
        self.pt_size2 = pt_size2
        self.pt_size3 = pt_size3# the size of pattern
        self.step = max(1, self.pt_size1 // 20)     # the step length of pattern's moving
        self.position1 = self.x1, self.y1 = (self.width // 2, self.height)
        self.position2 = self.x2, self.y2 = (self.width // 2, self.height)
        self.position3 = self.x3, self.y3 = (self.width // 2, self.height)
        # initial position of pattern

        # screen initialization
        self.screen = pg.display.set_mode(self.size, flags = RESIZABLE)
        self.screen.fill(self.bg)
        pg.display.update()

    def pattern_reset(self, x1, y1, width1, x2, y2, width2, x3, y3, width3):
        self.position1 = self.x1, self.y1 = (x1, y1)
        self.position2 = self.x2, self.y2 = (x2, y2)
        self.position3 = self.x3, self.y3 = (x3, y3)
        self.pt_size1 = int(1.3*width1)
        self.pt_size2 = int(1.3*width2)
        self.pt_size3 = int(1.3*width3)
        self.step = max(1, self.pt_size1 // 20)
        print('step =' + str(self.step))


    def draw_blank(self):
        self.screen.fill(self.bg)
        # pg.draw.rect(screen, pttern, (x - pt_size, y - 2 * pt_size, 2 * pt_size, 3 * pt_size), 0)
        #pg.draw.rect(self.screen, self.pattern, (0, 0, 1, 1), 0)
        pg.display.flip()


    def draw_pattern_x(self, delay = False):
        self.screen.fill(self.bg)
        x1, y1 = self.x1, self.y1
        x2, y2 = self.x2, self.y2
        x3, y3 = self.x3, self.y3
        while True:
            pg.draw.rect(self.screen, self.pattern, (x1-self.pt_size1, 0, self.pt_size1, self.height), 0)
            pg.draw.rect(self.screen, self.pattern, (x2 - self.pt_size2, 0, self.pt_size2, self.height), 0)
            pg.draw.rect(self.screen, self.pattern, (x3-self.pt_size3, 0, self.pt_size3, self.height), 0)
            # draw pattern
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

    '''def draw_pattern_y(self, delay = False):
        self.screen.fill(self.bg)
        x, y = self.x, self.y
        while True:
            pg.draw.rect(self.screen, self.pattern, (0, 0, x - self.pt_size * 3, y), 0)
            pg.draw.rect(self.screen, self.pattern, (x + self.pt_size * 3, y-self.pt_size, self.width - x - self.pt_size * 3, self.height - y+self.pt_size), 0)
            pg.draw.rect(self.screen, self.pattern, (x - self.pt_size * 3, y - self.pt_size, self.pt_size * 6, self.pt_size), 0)
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
                    sys.exit()'''

    # define functions of pattern's moving control
    def move_left(self):
        x1, y1 = self.x1, self.y1
        x2, y2 = self.x2, self.y2
        x3, y3 = self.x3, self.y3

        self.screen.fill(self.bg)
        # pg.draw.rect(screen, pttern, (x - pt_size, y, 2 * pt_size, 3 * pt_size), 0)
        pg.draw.rect(self.screen, self.pattern, (x1, 0, self.pt_size1, self.height), 0)
        pg.draw.rect(self.screen, self.pattern, (x2, 0, self.pt_size2, self.height), 0)
        pg.draw.rect(self.screen, self.pattern, (x3, 0, self.pt_size3, self.height), 0)

        # draw pattern
        pg.display.flip()

    def move_right(self):
        x1, y1 = self.x1, self.y1
        x2, y2 = self.x2, self.y2
        x3, y3 = self.x3, self.y3
        self.screen.fill(self.bg)
        # pg.draw.rect(screen, pttern, (x - pt_size, y - 2 * pt_size, 2 * pt_size, 3 * pt_size), 0)
        pg.draw.rect(self.screen, self.pattern, (x1 - self.pt_size1, 0, self.pt_size1, self.height), 0)
        pg.draw.rect(self.screen, self.pattern, (x2 - self.pt_size2, 0, self.pt_size2, self.height), 0)
        pg.draw.rect(self.screen, self.pattern, (x3 - self.pt_size3, 0, self.pt_size3, self.height), 0)
        pg.display.flip()

    def move_up(self):
        x, y = self.x, self.y
        self.screen.fill(self.bg)
        # pg.draw.rect(screen, pttern, (x - pt_size, y - 2 * pt_size, 2 * pt_size, 3 * pt_size), 0)
        pg.draw.rect(self.screen, self.pattern, (0, 0, x - self.pt_size * 2, y + self.pt_size ), 0)
        pg.draw.rect(self.screen, self.pattern,
                     (x + self.pt_size * 2, y, self.width - x - self.pt_size * 2, self.height - y ), 0)
        pg.draw.rect(self.screen, self.pattern,
                     (x - self.pt_size * 2, y, self.pt_size * 4, self.pt_size), 0)
        pg.display.flip()

    def move_down(self):
        x, y = self.x, self.y
        self.screen.fill(self.bg)
        # pg.draw.rect(screen, pttern, (x - pt_size, y - 2 * pt_size, 2 * pt_size, 3 * pt_size), 0)
        pg.draw.rect(self.screen, self.pattern, (0, 0, x - self.pt_size * 2, y ), 0)
        pg.draw.rect(self.screen, self.pattern,
                     (x + self.pt_size * 2, y - self.pt_size, self.width - x - self.pt_size * 4, self.height - y+self.pt_size ), 0)
        pg.draw.rect(self.screen, self.pattern,
                     (x - self.pt_size * 2, y - self.pt_size, self.pt_size * 4, self.pt_size), 0)
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


    def auto_move(self):
        while True:
            '''while self.x - 3 * self.pt_size > 0:
                pg.time.delay(self.delay)
                self.move_left()
                self.x -= self.step
                self.manual_set()

            while self.x + self.pt_size < self.width:
                pg.time.delay(self.delay)
                self.move_right()
                self.x += self.step
                self.manual_set()'''

            while self.y - self.pt_size*3 > 0:
                pg.time.delay(self.delay)
                self.move_up()
                self.y -= self.step
                self.manual_set()

            while self.y + self.pt_size < self.height:
                pg.time.delay(self.delay)
                self.move_down()
                self.y += self.step
                self.manual_set()
        #self.manual_set()


if __name__ == '__main__':
    pattern = Pattern(30)
    pattern.pattern_reset(360,360,30)
    pattern.draw_pattern_y()

    #pattern.draw_pattern_y()
    pattern.auto_move()
    pattern.manual_set()


