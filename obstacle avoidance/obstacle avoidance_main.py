import sys

sys.path.append("D:\install\DLAM-AI\keras_yolo3_master_trained")
import time
from lightPattern.pattern_astar_auto import *  # pattern part
from keras_yolo3_master_trained.yolostart import *  # droplet detection part
from thorlabs_camera.pycamera3 import *
from Astar.astar import *
import pygame as pg
from PIL import Image
import re
import os
from thorlabs_tsi_sdk import tl_camera
from thorlabs_tsi_sdk import tl_mono_to_color_processor
# dir_project = os.path.abspath(os.path.join(os.getcwd(), "../.."))  
from numpy.core.defchararray import strip


class Droplet:

    def __init__(self, size, x, y):
        self.size = size
        self.center = self.x, self.y = (x, y)
        self.radius = self.size/2

    def size_reset(self, size):
        self.size = size
        self.radius = self.size/2

    def center_reset(self, x, y):
        self.center = self.x, self.y = (x, y)

    def move(self, ai_droplet, path, blocks):
        for k in range(len(path)):
            target = path[k]
            des_x = int(target[0])
            des_y = int(target[1])
            print('the destination' + ' ' + str(k) + ' ' +  'is:' + str(des_x) + ',' + str(des_y))
            #feedback_y(camera, detector, starter, terminal,  pattern)
            #image = camera.pic_collect()
            #drop_center, drop_size = detector.detection(image)
            #react_1, react_2, block = "red drop", "yellow drop", "green drop"
            #x, y = drop_center[react_1][0]

            while abs(des_x - self.x) > pattern.pt_size//2 or abs(des_y - self.y) > pattern.pt_size//2:
                detect_space = 0
                #if abs(des_x - starter.x) > pattern.pt_size or abs(des_y - starter.y) > pattern.pt_size:
                if (des_y - self.y) > radius:
                    while True:
                        pg.time.delay(ai_droplet.pattern.delay)
                        ai_droplet.pattern.move_down()
                        ai_droplet.pattern.y += ai_droplet.pattern.step
                        ai_droplet.pattern.manual_set()
                        detect_space += 1
                        if detect_space >=80 or (ai_droplet.pattern.y - des_y) > self.radius/8:
                            break

                    ai_droplet.pattern.draw_blank()
                    #Blank_pattern.draw_blank()
                    ai_droplet.feedback(self, blocks)
                    #pattern.draw_pattern_y(1000)
                    ai_droplet.pattern.manual_set()

                elif (self.y - des_y) > self.radius:
                    while True:
                        pg.time.delay(ai_droplet.pattern.delay)
                        ai_droplet.pattern.move_up()
                        ai_droplet.pattern.y -= ai_droplet.pattern.step
                        ai_droplet.pattern.manual_set()
                        detect_space += 1
                        if detect_space >= 80 or (des_y-ai_droplet.pattern.y) > self.radius/8:
                            break

                    ai_droplet.pattern.draw_blank()
                    #Blank_pattern.draw_blank()

                    ai_droplet.feedback(self, blocks)
                    #pattern.draw_pattern_y(1000)
                    ai_droplet.pattern.manual_set()

                elif (des_x - self.x) > self.radius:
                    while True:
                        pg.time.delay(ai_droplet.pattern.delay)
                        ai_droplet.pattern.draw_pattern_x(blocks.center, blocks.size + self.radius)
                        ai_droplet.pattern.x += ai_droplet.pattern.step
                        ai_droplet.pattern.manual_set()
                        detect_space += 1
                        if detect_space >= 80 or (ai_droplet.pattern.x - des_x) > self.radius/8:
                            break
                    ai_droplet.pattern.draw_blank()
                    #Blank_pattern.draw_blank()
                    ai_droplet.feedback(self, blocks)
                    #pattern.draw_pattern_x(Block[1], Block[0] + radius)
                    ai_droplet.pattern.manual_set()

                elif (self.x - des_x) > self.radius:
                    while True:
                        pg.time.delay(ai_droplet.pattern.delay)
                        ai_droplet.pattern.draw_pattern_x(blocks.center, blocks.size + self.radius*0.5)
                        ai_droplet.pattern.x -= ai_droplet.pattern.step
                        ai_droplet.pattern.manual_set()
                        detect_space += 1
                        if detect_space >= 80 or (des_x-ai_droplet.pattern.x) > self.radius/8:
                            break

                    ai_droplet.pattern.draw_blank()
                    #Blank_pattern.draw_blank()
                    ai_droplet.feedback(self, blocks)
                    #pattern.draw_pattern_x(Block[1], Block[0] + radius)
                    ai_droplet.pattern.manual_set()

                else:
                    break
            print('The droplet achieved the destination')
        #detector.close_camera()
        return path


class AI_droplet():
    def __init__(self, camera):
        self.camera = camera
        self.detector = ImageDetector()
        self.map = Map(580, 580)
        self.react_1, self.react_2, self.block = "orange_droplet", "yellow_droplet", "green_droplet"

    def detect(self):
        img = self.camera.pic_collect()
        #self.detector = ImageDetector()
        drop_center, drop_size = self.detector.detection(img)
        return drop_center, drop_size

    def best_path(self, drop_center, drop_size):
        radius = drop_size[self.react_1][0]
        start = start_x, start_y = drop_center[self.react_1][0]
        terminal = drop_center[self.react_2][0]
        block_center, block_size = drop_center[self.block][0], drop_size[self.block][0]
        Block = block_size, block_center
        self.pattern = AutoPattern(580, 580, radius)
        self.map.createBlock(Block[1], 4*Block[0], radius)
        self.pattern.pattern_reset(start[0], start[1], 1.5*radius)
        self.pattern.set_terminal(terminal)
        self.pattern.draw_pattern(Block[1], Block[0] + 1.5*radius)
        best_path = AStarSearch(self.map, terminal, start)
        return radius, start, terminal, Block, self.pattern, self.map, best_path


    def feedback(self, droplet2move, blocks):
        self.pattern.draw_blank()
        time.sleep(0.05)
        drop_center, drop_size = self.detect()
        if drop_center:
            x1, y1 = drop_center[self.react_1][0]
            droplet2move.center_reset(x1, y1)
            x2, y2 = drop_center[self.block][0]
            droplet2move.size_reset(drop_size[self.react_1][0])
            blocks.center_reset(x2, y2)
            blocks.size_reset(drop_size[self.block][0])
            # if abs(starter.x - pattern.x) > 20:
            self.pattern.pattern_reset(x1, y1, drop_size[self.react_1][0])


    def data_saving(self, radius, start, terminal, Block, best_path, path):
        rusults = 'D:\install\DLAM-AI\\result' 
        # objects_data = 'E:\liuenqing\ML\keras-yolo3-master\keras-yolo3-master\single_droplets\mAP-master\input\detection-results'  # detectnion-results目录

        txt_path = rusults + '/best_path.txt'
        txt_objects = rusults + '/objects.txt'  # hdf5
        path_file = open(txt_path, 'w')
        for j in range(len(best_path)):
            path_file.write(str(best_path[j]) + '\n')
        for i in range(len(path)):
            path_file.write('the temporal destination' + str(i) + 'are:' + str(path[i]) + '\n')
        objects_file = open(txt_objects, 'w')
        objects_file.write('the start is : ' + str(start) + '\n' + 'the start size is' + str(radius) + '\n' + 'the block is :' + '\n' + str(
            Block[1]) + '\n' + 'the block size is' + str(Block[0]) + '\n' + 'the block is :' + str(Block[1]) + '\n' + 'the destination is : ' + str(terminal) )



    # return self.detector, self.pattern, self.map



with tl_camera.TLCameraSDK() as TLCameraSDK, tl_mono_to_color_processor.MonoToColorProcessorSDK() as MonoToColorProcessorSDK: #should be called only once
    with Camera(TLCameraSDK, MonoToColorProcessorSDK) as camera:

        ai_droplet = AI_droplet(camera)
        drop_center, drop_size = ai_droplet.detect()
        radius, start, terminal, Block, pattern, map, best_path = ai_droplet.best_path(drop_center, drop_size)

        droplet2move = Droplet(radius, start[0], start[1])
        blocks = Droplet(Block[0], Block[1][0], Block[1][1])
        path = best_path[250::250]
        path.append((terminal[0] - radius * 2, best_path[250][1]))
        path.append(terminal)
        #Blank_pattern = AutoPattern(580, 580, 1.5 * radius)

        data = ai_droplet.data_saving(radius, start, terminal, Block, best_path, path)
        data
        print('the start is : ' + str(start))
        print('the block is : ' + str(Block[1]))
        print('the destination is : ' + str(terminal))
        print('the best_path is at: ' + str(best_path))
        print(str(path))

        droplet2move.move(ai_droplet, path, blocks)




