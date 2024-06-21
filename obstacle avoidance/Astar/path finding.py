from random import randint
import pygame as pg
import sys
from pygame.locals import *
import easygui as eg
from tkinter import *
from tkinter import messagebox

best_path = []
block_x = []
block_y = []
class SearchEntry():
    def __init__(self, x, y, g_cost, f_cost=0, pre_entry=None):
        self.x = x
        self.y = y
        # cost move form start entry to this entry
        self.g_cost = g_cost
        self.f_cost = f_cost
        self.pre_entry = pre_entry

    def getPos(self):
        return (self.x, self.y)


class Map():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.map = [[0 for x in range(self.width)] for y in range(self.height)]

    def createBlock(self, block_num, radius):
        for i in range(block_num):
            x, y = (randint(10, self.width - 10), randint(20, self.height - 20))
            block_x.append(x)
            block_y.append(y)
            for m in range(x-3-radius,x+4+radius):
                for n in range(y-3-radius,y+4+radius):
                    self.map[n][m] = 1

    def generatePos(self, rangeX, rangeY):
        x, y = (randint(rangeX[0], rangeX[1]), randint(rangeY[0], rangeY[1]))
        while self.map[y][x] == 1:
            x, y = (randint(rangeX[0], rangeX[1]), randint(rangeY[0], rangeY[1]))
        return (x, y)

    def showMap(self):
        print("+" * (3 * self.width + 2))

        for row in self.map:
            s = '+'
            for entry in row:
                s += ' ' + str(entry) + ' '
            s += '+'
            print(s)

        print("+" * (3 * self.width + 2))


def AStarSearch(map, source, dest):
    def getNewPosition(map, locatioin, offset):
        x, y = (location.x + offset[0], location.y + offset[1])
        if x < 0 or x >= map.width or y < 0 or y >= map.height or map.map[y][x] == 1:
            return None
        return (x, y)

    def getPositions(map, location):
        # use four ways or eight ways to move
        offsets = [(-1, 0), (0, -1), (1, 0), (0, 1)]
        # offsets = [(-1,0), (0, -1), (1, 0), (0, 1), (-1,-1), (1, -1), (-1, 1), (1, 1)]
        poslist = []
        for offset in offsets:
            pos = getNewPosition(map, location, offset)
            if pos is not None:
                poslist.append(pos)
        return poslist

    # imporve the heuristic distance more precisely in future
    def calHeuristic(pos, dest):
        return abs(dest.x - pos[0]) + abs(dest.y - pos[1])

    def getMoveCost(location, pos):
        if location.x != pos[0] and location.y != pos[1]:
            return 1.4
        else:
            return 1

    # check if the position is in list
    def isInList(list, pos):
        if pos in list:
            return list[pos]
        return None

    # add available adjacent positions
    def addAdjacentPositions(map, location, dest, openlist, closedlist):
        poslist = getPositions(map, location)
        for pos in poslist:
            # if position is already in closedlist, do nothing
            if isInList(closedlist, pos) is None:
                findEntry = isInList(openlist, pos)
                h_cost = calHeuristic(pos, dest)
                g_cost = location.g_cost + getMoveCost(location, pos)
                if findEntry is None:
                    # if position is not in openlist, add it to openlist
                    openlist[pos] = SearchEntry(pos[0], pos[1], g_cost, g_cost + h_cost, location)
                elif findEntry.g_cost > g_cost:
                    # if position is in openlist and cost is larger than current one,
                    # then update cost and previous position
                    findEntry.g_cost = g_cost
                    findEntry.f_cost = g_cost + h_cost
                    findEntry.pre_entry = location

    # find a least cost position in openlist, return None if openlist is empty
    def getFastPosition(openlist):
        fast = None
        for entry in openlist.values():
            if fast is None:
                fast = entry
            elif fast.f_cost > entry.f_cost:
                fast = entry
        return fast

    openlist = {}
    closedlist = {}
    location = SearchEntry(source[0], source[1], 0.0)
    dest = SearchEntry(dest[0], dest[1], 0.0)
    openlist[source] = location
    while True:
        location = getFastPosition(openlist)
        if location is None:
            # not found valid path
            print("can't find valid path")
            break;

        if location.x == dest.x and location.y == dest.y:
            break

        closedlist[location.getPos()] = location
        openlist.pop(location.getPos())
        addAdjacentPositions(map, location, dest, openlist, closedlist)

    # mark the found path at the map
    while location is not None:
        map.map[location.y][location.x] = 2
        best_path.append((location.x, location.y))
        location = location.pre_entry

    print(best_path)

def showPath(width, height, radius, dest):

    pg.init()

    size = width, height
    unit = 15
    R = radius*5
    bg = (255, 255, 255)
    BLUE = (100, 149, 237)
    RED = (200, 30, 50)
    GRAY = (169, 169, 169)
    LIGHTRED = (255, 193, 193)

    # set the background and title
    screen = pg.display.set_mode(size)
    pg.display.set_caption('Droplet Transport')


    (dest_x,dest_y) = dest

    len_path = len(best_path) - 1

    for i in range(len_path):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
        pg.time.delay(100)
        screen.fill(bg)
        (center_x, center_y) = best_path[(len_path - i)]
        center = (center_x * 5, center_y * 5)

        for i in range(len(block_x)):
            pg.draw.rect(screen, GRAY, (block_x[i] * 5 - unit, block_y[i] * 5 - unit, unit * 2, unit * 2),
                         0)  # draw all the droplets trapped before and turn gray

        for j in range(len(best_path)):
            path_x, path_y = best_path[j]
            pg.draw.rect(screen, LIGHTRED, (path_x * 5 - 2, path_y * 5 - 2, 4, 4), 0)

        pg.draw.rect(screen, RED, (dest_x * 5 - unit, dest_y * 5 - unit, unit * 2, unit * 2), 0)

        pg.draw.circle(screen, BLUE, center, R)

        pg.display.update()

    while True:
        screen.fill(bg)
        for i in range(len(block_x)):
            pg.draw.rect(screen, GRAY, (block_x[i] * 5 - unit, block_y[i] * 5 - unit, unit * 2, unit * 2),
                     0)  # draw all the droplets trapped before and turn gray

        for j in range(len(best_path)):
            path_x, path_y = best_path[j]
            pg.draw.rect(screen, LIGHTRED, (path_x * 5 - R, path_y * 5 - R, R * 2, R * 2), 0)

        pg.draw.rect(screen, RED, (dest_x * 5 - unit, dest_y * 5 - unit, unit * 2, unit * 2), 0)

        pg.draw.circle(screen, BLUE, (dest_x * 5, dest_y * 5), R)

        pg.display.update()

        for event in pg.event.get():
            if event.type == QUIT:
                choice = messagebox.askquestion(title=None, message='Restart or not?')
                if choice == 'no':
                    sys.exit()
                if choice == 'yes':
                    showPath(width, height, radius, dest)


        # for event in pg.event.get():
        #     if event.type == QUIT:
        #         choice = eg.buttonbox(msg='Are you sure to exit?',title='Exit Option', choices=('Restart', 'Exit'))
        #         if choice == 'Exit':
        #             sys.exit()
        #         if choice == 'Restart':
        #             screen.fill(bg)
        #             pg.display.update()
        #             setting()


def setting():
    WIDTH = 60
    HEIGHT = 60

    root = Tk()
    Label(root, text="Block number(1~5): ").grid(row=0)
    Label(root, text="Droplet radius(1~5): ").grid(row=1)
    Label(root, text="Destination(5~55): ").grid(row=2)

    e1 = Entry(root)
    e2 = Entry(root)
    e3 = Entry(root)
    e4 = Entry(root)

    e1.grid(row=0, column=1, padx=10, pady=5)
    e2.grid(row=1, column=1, padx=10, pady=5)
    e3.grid(row=2, column=1, padx=10, pady=5)
    e4.grid(row=2, column=2, padx=10, pady=5)


    def get():
        BLOCK_NUM = int(e1.get())
        radius = int(e2.get())
        dest = (int(e3.get()), int(e4.get()))
        return BLOCK_NUM, radius, dest


    Button(root, text="OK", width=10, command=lambda: (get(), root.quit())) \
        .grid(row=3, column=1, padx=10, pady=5)

    mainloop()
    BLOCK_NUM, radius, dest = get()

    map = Map(WIDTH, HEIGHT)
    map.createBlock(BLOCK_NUM, 3*radius)
    map.showMap()

    source = (3, 30)
    print("source:", source)
    print("dest:", dest)
    AStarSearch(map, source, dest)
    map.showMap()
    showPath(WIDTH * 5, HEIGHT * 5, radius, dest)


setting()