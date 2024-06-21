import sys

sys.path.append("D:\install\DLAM-feedback\keras_yolo3_master_trained")
from lightPattern.pattern_auto2d import *  # pattern part
from keras_yolo3_master_trained.yolostart_mutidrop import *  # droplet detection part
from thorlabs_camera.pycamera import *
import pygame as pg
import re
import os


class Droplet:
    def __init__(self, size, x, y, process):
        self.size = size
        self.center = self.x, self.y = (x, y)
        self.process = process

    def size_reset(self, size):
        self.size = size

    def center_reset(self, x, y):
        self.center = self.x, self.y = (x, y)

    def process_reset(self, process):
        self.process = process


'''sample_list = []
DNApol_list = []

def position_storage(drop_center1, drop_center2):
    sample_list.extend(drop_center1)
    DNApol_list.extend(drop_center2)
    
    print('the sample_list is:' + str(sample_list) + 'the DNApol_list is:' + str(DNA_list))
    return sample_list, DNApol_list'''


def position_storage(sample_list, DNApol_list):
    sample_list1 = sorted(sample_list, key=lambda x: (x[0], x[1]), reverse=False)
    DNApol_list1 = sorted(DNApol_list, key=lambda y: (y[1], y[0]), reverse=False)
    DNApol_xlist = sorted(DNApol_list, key=lambda x: (x[0], x[1]), reverse=False)

    print('the sorted_sample_list is:' + str(sample_list1) + 'the sorted_DNApol_list is:' + str(DNApol_list1))
    return sample_list1, DNApol_list1, DNApol_xlist


def AI_init():
    camera = Camera()  # class camera from pycamera
    img = camera.pic_collect()  # img-name from camera
    detector = ImageDetector()
    DNA_pol, sample = "DNA_pol", "sample"
    # img = r'D:\install\pythonProject\DLAM-color\keras_yolo3_master\VOC2007\test\000073.jpg'
    drop_center, drop_size = detector.detection(img)
    sample_list = drop_center[sample]
    DNApol_list = drop_center[DNA_pol]
    sample_list1, DNApol_list1, DNApol_xlist = position_storage(sample_list, DNApol_list)
    radius = drop_size[sample][0]
    (x, y) = sample_list1[0]
    process = 0
    # start = start_x, start_y = drop_center[self.react_1][0]
    terminal = (terminal_x, terminal_y) = DNApol_xlist[-1]
    # block_center, block_size = drop_center[block][0], drop_size[block][0]
    # drop_center, drop_size = detector.detection(img)
    print(drop_center)
    # radius = drop_size[0]
    start = Droplet(radius, x, y, process)
    pattern = Pattern(0.8 * radius)
    pattern.pattern_reset(x, y, radius)
    pattern.draw_pattern_x()
    return camera, detector, start, terminal, pattern, radius,process, sample_list1, DNApol_list1


def feedback_x(camera, detector, start, terminal, pattern):
    pattern.draw_blank()
    image = camera.pic_collect()
    drop_center, drop_size = detector.detection(image)
    DNA_pol, sample = "DNA_pol", "sample"
    sample_list2 = []
    DNApol_list2 = []
    if (sample in drop_center) & (DNA_pol in drop_center):

        process = 0
        sample_list = drop_center[sample]
        DNApol_list = drop_center[DNA_pol]
        sample_list2, DNApol_list2, DNApol_xlist = position_storage(sample_list, DNApol_list)
        print('the sample_list2 is:' + str(sample_list2) + '\n' + 'the DNApol_list2 is:' + str(DNApol_list2))
        if drop_center:
            (x, y) = sample_list2[0]
            start.center_reset(x, y)
            start.size_reset(drop_size[sample][0])
            start.process_reset(process)
            #if (abs(start.x - pattern.x)) > 20 or (abs(start.y - pattern.y) > 20):
            pattern.pattern_reset(x, y, drop_size[sample][0])
    elif (sample not in drop_center) & (DNA_pol in drop_center):
        process = 1
        start.process_reset(process)
        print("the sample and DNA_pol are mixed")

    return sample_list2, DNApol_list2


'''def feedback_y(camera, detector, start, terminal, pattern):
    pattern.draw_blank()
    image = camera.pic_collect()
    drop_center, drop_size = detector.detection(image)
    DNA_pol, sample = "DNA_pol", "sample"
    if drop_center:
        x, y = drop_center[sample][0]
        start.center_reset(x, y)
        start.size_reset(drop_size[sample][0])
        if abs(start.y - pattern.y) > 20:
            pattern.pattern_reset(x, y, drop_size[sample][0])'''


camera, detector, start, terminal, pattern, radius, process, sample_list1, DNApol_list1 = AI_init()
detect_space = 0


# target = get_target()
def get_target(terminal):
    target = terminal
    print(target)
    return target


target = get_target(terminal)


def data_saving():
    rusults = 'D:\install\DLAM-feedback\\result'  # yolo批量处理结果的目录
    # objects_data = 'E:\liuenqing\ML\keras-yolo3-master\keras-yolo3-master\single_droplets\mAP-master\input\detection-results'  # detectnion-results目录

    # 创建记录检测结果的文件
    txt_path = rusults + '/result.txt'
    path_file = open(txt_path, 'w')
    path_file.write('the droplet size  is ' + str(radius) + '\n' + 'the droplet is at' + str(
        start) + '\n' + 'the terminal is at' + str(target))
    '''for i in range(len(path)):
        path_file.write('the temporal destination' + str(i) + 'are:' + str(path[i]) + '\n')
    objects_file = open(txt_objects, 'w')
    objects_file.write('the start is : ' + str(start) + '\n' + 'the block is : ' + str(
        Block[1]) + '\n' + 'the destination is : ' + str(terminal))'''


data_saving()


def move_RNA():
    des_x = int(target[0])
    des_y = int(target[1])
    print('the destination is:' + str(des_x) + ',' + str(des_y))

    while True:
        if start.process == 0:
            detect_space = 0
            '''if (des_y - start.y) > pattern.pt_size/2:
                while pattern.y - 2 * pattern.pt_size > 0:
                    pg.time.delay(pattern.delay)
                    pattern.move_down()
                    pattern.y += pattern.step
                    pattern.manual_set()
                    detect_space += 1

                    if detect_space >= 80 or (pattern.y - des_y) > pattern.pt_size/4:
                        break

                feedback_y(camera, detector, start, terminal, pattern)
                #pattern.draw_pattern_y(1000)
                pattern.manual_set()

            elif (start.y - des_y) > pattern.pt_size/2:
                while pattern.y - 2 * pattern.pt_size > 0:
                    pg.time.delay(pattern.delay)
                    pattern.move_up()
                    pattern.y -= pattern.step
                    pattern.manual_set()
                    detect_space += 1
                    if detect_space >= 80 or (des_y - pattern.y) > pattern.pt_size/4:
                        break
                feedback_y(camera, detector, start, terminal, pattern)
                #pattern.draw_pattern_y(1000)
                pattern.manual_set()'''
            if (des_x - start.x) > pattern.pt_size:
                while pattern.x - 2 * pattern.pt_size > 0:
                    pg.time.delay(pattern.delay)
                    pattern.move_right()
                    pattern.x += pattern.step
                    pattern.manual_set()
                    detect_space += 1
                    if detect_space >= 150 or (pattern.x - des_x) > pattern.pt_size / 4:
                        break
                feedback_x(camera, detector, start, terminal, pattern)
                # pattern.draw_pattern_x(1000)
                pattern.manual_set()

            elif (start.x - des_x) > pattern.pt_size:
                while pattern.x - 2 * pattern.pt_size > 0:
                    pg.time.delay(pattern.delay)
                    pattern.move_left()
                    pattern.x -= pattern.step
                    pattern.manual_set()
                    detect_space += 1
                    if detect_space >= 150 or (des_x - pattern.x) > pattern.pt_size / 4:
                        break
                feedback_x(camera, detector, start, terminal, pattern)
                # pattern.draw_pattern_x(1000)
                pattern.manual_set()


            elif abs(des_x - start.x) <= pattern.pt_size:
                print("The droplet achieved the destination")
                feedback_x(camera, detector, start, terminal, pattern)


        elif start.process == 1:
            print("the RNA and the DNApol are mixed, please add samples")
            position1 = 80, 100
            pattern.draw_text('Sample!', position1, 0)
            break


def move_DNA(DNApol_list2):
    feedback_x(camera, detector, start, terminal, pattern)
    sample_number = 0
    while sample_number <= 2:
        des_list = DNApol_list2
        des_x = des_list[sample_number][0]
        des_y = des_list[sample_number][1]
        detect_space = 0
        if start.process == 0:
            if (des_y - start.y) > pattern.pt_size:
                while pattern.y - 2 * pattern.pt_size > 0:
                    pg.time.delay(pattern.delay)
                    pattern.move_down()
                    pattern.y += pattern.step
                    pattern.manual_set()
                    detect_space += 1

                    if detect_space >= 100 or (pattern.y - des_y) > pattern.pt_size / 4:
                        break

                feedback_x(camera, detector, start, terminal, pattern)
                # pattern.draw_pattern_y(1000)
                pattern.manual_set()

            elif (start.y - des_y) > pattern.pt_size / 2:
                while pattern.y - 2 * pattern.pt_size > 0:
                    pg.time.delay(pattern.delay)
                    pattern.move_up()
                    pattern.y -= pattern.step
                    pattern.manual_set()
                    detect_space += 1
                    if detect_space >= 100 or (des_y - pattern.y) > pattern.pt_size / 4:
                        break
                feedback_x(camera, detector, start, terminal, pattern)
                # pattern.draw_pattern_y(1000)
                pattern.manual_set()
            elif (des_x - start.x) > pattern.pt_size:
                while pattern.x - 2 * pattern.pt_size > 0:
                    pg.time.delay(pattern.delay)
                    pattern.move_right()
                    pattern.x += pattern.step
                    pattern.manual_set()
                    detect_space += 1
                    if detect_space >= 100 or (pattern.x - des_x) > pattern.pt_size / 4:
                        break
                feedback_x(camera, detector, start, terminal, pattern)
                # pattern.draw_pattern_x(1000)
                pattern.manual_set()

            elif (start.x - des_x) > pattern.pt_size:
                while pattern.x - 2 * pattern.pt_size > 0:
                    pg.time.delay(pattern.delay)
                    pattern.move_left()
                    pattern.x -= pattern.step
                    pattern.manual_set()
                    detect_space += 1
                    if detect_space >= 100 or (des_x - pattern.x) > pattern.pt_size / 4:
                        break
                feedback_x(camera, detector, start, terminal, pattern)
                # pattern.draw_pattern_x(1000)
                pattern.manual_set()

            elif (abs(des_x - start.x) < pattern.pt_size / 2) & (abs(des_y - start.y) < pattern.pt_size / 2):
                print("The droplet achieved the destination")
                feedback_x(camera, detector, start, terminal, pattern)

        elif start.process == 1:
            print('the sample' + str(sample_number) + ' has mixed with the DNApol, please add the next sample')
            if sample_number < 2:
                pattern.draw_text('Sample!', (des_x-200, des_y + 150), 0)
                sample_number += 1
            elif sample_number == 2:
                pattern.draw_text('Bingo!', (80, 200), 0)
            time.sleep(5)
            feedback_x(camera, detector, start, terminal, pattern)
            # elif droplet.x > 600 or droplet.y > 600:
            # break'''
    print('all the samples are mixed, please start amplifying')
    pattern.draw_text('amplifying', (80, 200), 0)
    detector.close_camera()

    # while pattern.y + pattern.pt_size < pattern.height:
    #     pg.time.delay(pattern.delay)
    #     pattern.move_down()
    #     pattern.y += pattern.step
    #     pattern.manual_set()
    #     detect_space += 1
    #     if detect_space >= 20:
    #         break


get_target(terminal)
move_RNA()
time.sleep(2)
sample_list2, DNApol_list2 = feedback_x(camera, detector, start, terminal, pattern)
move_DNA(DNApol_list2)
