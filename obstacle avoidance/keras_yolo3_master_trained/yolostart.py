import sys
sys.path.append("D:\install\DLAM-AI\keras_yolo3_master_trained")
from yolo import YOLO
from PIL import Image
import time


class ImageDetector:

    def __init__(self):
        self.yolo = YOLO()

    def detection(self, image):
        #yolo = YOLO()
        #print(image)
        #image = Image.open(image)
        #print(image)
        rel_image, drops_center, drops_size = self.yolo.detect_image(image)
        rel_image.show()
        local = time.strftime('%Y%m%d%H%M%S')
        path = 'D:\install\DLAM-AI\\result/'
        figure_name = path + local
        rel_image.save(figure_name+'.jpg')
        return drops_center, drops_size

    def close_camera(self):
        self.yolo.close_session()

if __name__ == "__main__":
    img = r'D:\install\DLAM-feedback\keras_yolo3_master\test pic\image_38.png'
    detector = ImageDetector()
    drops_center, drops_size = detector.detection(img)
    print(drops_center)
    print(drops_size)
# from yolo3.model import yolo_body
# from keras.layers import Input
# import sys
# sys.path.append(r'C:\Users\86198\Desktop\python\pycharm\Astar')
# from yolo import YOLO
# from astar import *
# from PIL import Image
# from pattern_astar_auto import AutoPattern
#
# yolo = YOLO()
#
# factor = 0.2
# img = r'.\pic\000155.png'
#
# image = Image.open(img)
# width, height = image.size[0], image.size[1]
# image = image.resize((int(width * factor), int(height * factor)), Image.ANTIALIAS)
# width, height = int(width * factor), int(height * factor)
# rel_image, drops_center, drops_size = yolo.detect_image(image)
# target_size = 5
# rel_image.show()
#
# print(drops_center)
# print(drops_size)
# yolo.close_session()
#
# path_width = 4
# map = Map(width, height)   # map for path finding
# for i in range(len(drops_center)):
#     block_center, radius = drops_center[i], drops_size[i]
#     block_center = (block_center[1], block_center[0])
#     print(block_center)
#     map.createBlock(block_center, radius, path_width + 2*target_size)
#
# map_pattern = Map(width, height)     # map for pattern
# for i in range(len(drops_center)):
#     block_center, radius = drops_center[i], drops_size[i]
#     block_center = (block_center[1], block_center[0])
#     print(block_center)
#     map_pattern.createBlock(block_center, radius, path_width)
# source = (5, height // 2)
# dest = (width - 5, height // 2)
# print("source:", source)
# print("dest:", dest)
# best_path = AStarSearch(map, source, dest)
# print(best_path)
# # showPath(width, height, path_width, dest)
# pattern = AutoPattern(width, height, path_width, target_size)
# pattern.transport_pattern(map_pattern, best_path)
