import sys
sys.path.append("D:\install\DLAM-feedback\keras_yolo3_master_trained")
from lightPattern.pattern_auto2d import *  # pattern part
from keras_yolo3_master_trained.yolostart_singledrop import *  # droplet detection part
from thorlabs_camera.pycamera import *
import pygame as pg
import re
import os


class Droplet:
    def __init__(self, size, x, y):
        self.size = size
        self.center = self.x, self.y = (x, y)

    def size_reset(self, size):
        self.size = size

    def center_reset(self, x, y):
        self.center = self.x, self.y = (x, y)

class Target:
    def __init__(self, x, y):
        self.target = self.x, self.y = (x, y)

def AI_init():
    camera = Camera()   #class camera from pycamera
    img = camera.pic_collect() #img-name from camera
    detector = ImageDetector()
    drop_center, drop_size = detector.detection(img)
    print(drop_center)
    start = x, y = drop_center[0]
    radius = drop_size[0]
    droplet = Droplet(drop_size[0], x, y)
    pattern = Pattern(radius)

    pattern.pattern_reset(x, y, radius)
    pattern.draw_pattern_x()
    return camera, detector, droplet, pattern, start, radius


def feedback_x(camera, detector, droplet, pattern):
    pattern.draw_blank()
    image = camera.pic_collect()
    drop_center, drop_size = detector.detection(image)
    if drop_center:
        x, y = drop_center[0]
        droplet.center_reset(x, y)
        droplet.size_reset(drop_size[0])
        if abs(droplet.x - pattern.x) > 20:
            pattern.pattern_reset(x, y, drop_size[0])


def feedback_y(camera, detector, droplet, pattern):
    pattern.draw_blank()
    image = camera.pic_collect()
    drop_center, drop_size = detector.detection(image)
    if drop_center:
        x, y = drop_center[0]
        droplet.center_reset(x, y)
        droplet.size_reset(drop_size[0])
        if abs(droplet.y - pattern.y) > 20:
            pattern.pattern_reset(x, y, drop_size[0])


def get_target():
    des = input('please input the destination coordinate with ,:')
    target = tuple(des.split(","))
    print(target)
    return target

'''def get_target():
    target = start[0], start[1] + 100
    print(target)
    return target'''


camera, detector, droplet, pattern, start, radius = AI_init()
detect_space = 0
target = get_target()


def data_saving():
    rusults = 'D:\install\DLAM-feedback\\result' 
    # objects_data = 'E:\liuenqing\ML\keras-yolo3-master\keras-yolo3-master\single_droplets\mAP-master\input\detection-results'  # detectnion-results目录

    txt_path = rusults + '/result.txt'
    path_file = open(txt_path, 'w', encoding='utf-8')
    path_file.write( 'the droplet is at：' + str(start) + '\n' + 'the droplet size  is：' + str(radius) + '\n' + 'the terminal is at：' + str(target))
    '''for i in range(len(path)):
        path_file.write('the temporal destination' + str(i) + 'are:' + str(path[i]) + '\n')
    objects_file = open(txt_objects, 'w')
    objects_file.write('the start is : ' + str(start) + '\n' + 'the block is : ' + str(
        Block[1]) + '\n' + 'the destination is : ' + str(terminal))'''

data_saving()

def move():
    des_x = int(target[0])
    des_y = int(target[1])
    print('the destination is:' + str(des_x) + ',' + str(des_y))
    while True:
            detect_space = 0
            if (des_x - droplet.x) > pattern.pt_size:
                while pattern.x - 2 * pattern.pt_size > 0:
                    pg.time.delay(pattern.delay)
                    pattern.move_right()
                    pattern.x += pattern.step
                    pattern.manual_set()
                    detect_space += 1
                    if detect_space >= 80 or pattern.x - des_x > pattern.pt_size/4:
                    #if pattern.x - des_x > pattern.pt_size / 4:
                        break
                feedback_x(camera, detector, droplet, pattern)
                #pattern.draw_pattern_x(1000)
                pattern.manual_set()

            elif (droplet.x - des_x) > pattern.pt_size:
                while pattern.x - 2 * pattern.pt_size > 0:
                    pg.time.delay(pattern.delay)
                    pattern.move_left()
                    pattern.x -= pattern.step
                    pattern.manual_set()
                    detect_space += 1
                    if detect_space >= 80 or  des_x - pattern.x > pattern.pt_size/4:
                    #if des_x - pattern.x > pattern.pt_size / 4:
                        break
                feedback_x(camera, detector, droplet, pattern)
                #pattern.draw_pattern_x(1000)
                pattern.manual_set()

            elif (des_y - droplet.y) > pattern.pt_size:
                while pattern.y - 2 * pattern.pt_size > 0:
                    pg.time.delay(pattern.delay)
                    pattern.move_down()
                    pattern.y += pattern.step
                    pattern.manual_set()
                    detect_space += 1

                    if detect_space >= 80 or pattern.y - des_y > pattern.pt_size/4:
                    #if pattern.y - des_y > pattern.pt_size / 4:
                        break

                feedback_y(camera, detector, droplet, pattern)
                pattern.draw_pattern_y(1000)
                pattern.manual_set()

            elif (droplet.y - des_y) > pattern.pt_size:
                while pattern.y - 2 * pattern.pt_size > 0:
                    pg.time.delay(pattern.delay)
                    pattern.move_up()
                    pattern.y -= pattern.step
                    pattern.manual_set()
                    detect_space += 1
                    if detect_space >= 80 or des_y - pattern.y > pattern.pt_size/4:
                    #if des_y - pattern.y > pattern.pt_size / 4:
                        break
                feedback_y(camera, detector, droplet, pattern)
                pattern.draw_pattern_y(1000)
                pattern.manual_set()
            else:
                print("The droplet achieved the destination")
                break

            #elif droplet.x > 600 or droplet.y > 600:
                #break'''



    # while pattern.y + pattern.pt_size < pattern.height:
    #     pg.time.delay(pattern.delay)
    #     pattern.move_down()
    #     pattern.y += pattern.step
    #     pattern.manual_set()
    #     detect_space += 1
    #     if detect_space >= 20:
    #         break
    detector.close_camera()


move()

