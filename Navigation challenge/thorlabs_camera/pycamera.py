import sys
sys.path.append("D:\install\DLAM-feedback\\thorlabs_camera")
import os
from PIL import Image
import matplotlib
import numpy as np
import cv2 as cv
from thorlabs_tsi_sdk.tl_camera_enums import EEP_STATUS, DATA_RATE, SENSOR_TYPE, OPERATION_MODE, COMMUNICATION_INTERFACE, \
    USB_PORT_TYPE, TRIGGER_POLARITY, TAPS
from thorlabs_tsi_sdk import tl_camera
from thorlabs_tsi_sdk import tl_mono_to_color_processor
os.chdir(r"D:\install\anaconda\envs\tensorflow\DLLs")
import time

class Camera():
    def __init__(self):
        self.roi_size = 580
        self.roi = tl_camera.ROI(0, 0, self.roi_size, self.roi_size)
        self.path = r'D:/install/DLAM-feedback/temp_image/'

    def pic_collect(self):
        with tl_camera.TLCameraSDK() as TLCameraSDK:
            camera_list = TLCameraSDK.discover_available_cameras()  # find camera
            print(camera_list)

            with TLCameraSDK.open_camera(camera_list[1]) as TLCamera:   # open camera
                TLCamera.operation_mode = OPERATION_MODE.SOFTWARE_TRIGGERED
                # TLCamera.roi = self.roi
                TLCamera.frames_per_trigger_zero_for_unlimited = 1
                sensor_type = TLCamera.camera_sensor_type
                color_filter = TLCamera.color_filter_array_phase
                color_correction = TLCamera.get_color_correction_matrix()
                white_balance = TLCamera.get_default_white_balance_matrix()
                bit_depth = TLCamera.bit_depth
                TLCamera.arm(1)
                TLCamera.issue_software_trigger()

                frame = TLCamera.get_pending_frame_or_null()
                image_buffer = frame.image_buffer
                TLCamera.disarm()   # parameters of camera

                with tl_mono_to_color_processor.MonoToColorProcessorSDK() as MonoToColorProcessorSDK:
                    with MonoToColorProcessorSDK.create_mono_to_color_processor(sensor_type, color_filter, color_correction, white_balance, bit_depth) as MonoToColorProcessor:
                        image_array = MonoToColorProcessor.transform_to_24(image_buffer, self.roi_size, self.roi_size)
                        image_array = np.reshape(image_array,(self.roi_size, self.roi_size, 3))
                        img = Image.fromarray(image_array)
                        img_name = self.path + str(int(time.time())) +'.jpg'
                        # img.convert('RGB').save(img_name)
                        img.save(img_name)
                        # img.show()
                        print(img_name)
                        return img

if __name__ == '__main__':
    camera = Camera()
    image = camera.pic_collect()

