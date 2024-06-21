import sys
sys.path.append(r"D:\install\pythonProject\DLAM-color\thorlabs_camera")
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
#TLCameraSDK, MonoToColorProcessorSDK
class Camera():
    def __init__(self):
        self.roi_size = 580
        self.roi = tl_camera.ROI(0, 0, self.roi_size, self.roi_size)
        self.TLCameraSDK = tl_camera.TLCameraSDK()
        #self.MonoToColorProcessorSDK = tl_mono_to_color_processor.MonoToColorProcessorSDK()

        self.path = r'D:\install\pythonProject\DLAM-color\temp_image/'
        camera_list = self.TLCameraSDK.discover_available_cameras()
        print(camera_list)
        try:
            self.TLCamera = self.TLCameraSDK.open_camera(camera_list[0])
        except IndexError:
            raise('no camera available')
        self.TLCamera.operation_mode = OPERATION_MODE.SOFTWARE_TRIGGERED
        # TLCamera.roi = self.roi
        self.TLCamera.frames_per_trigger_zero_for_unlimited = 1
        self.sensor_type = self.TLCamera.camera_sensor_type
        self.color_filter = self.TLCamera.color_filter_array_phase
        self.color_correction = self.TLCamera.get_color_correction_matrix()
        self.white_balance = self.TLCamera.get_default_white_balance_matrix()
        self.bit_depth = self.TLCamera.bit_depth
        self.TLCamera.arm(1)
        self.TLCamera.issue_software_trigger()
        #self.MonoToColorProcessorSDK = tl_mono_to_color_processor.MonoToColorProcessorSDK
        self.MonoToColorProcessorSDK = tl_mono_to_color_processor.MonoToColorProcessorSDK()
        self.sensor_type = self.TLCamera.camera_sensor_type
        self.color_filter = self.TLCamera.color_filter_array_phase
        self.color_correction = self.TLCamera.get_color_correction_matrix()
        self.white_balance = self.TLCamera.get_default_white_balance_matrix()
        self.bit_depth = self.TLCamera.bit_depth
        self.MonoToColorPcessor = self.MonoToColorProcessorSDK.create_mono_to_color_processor(self.sensor_type, self.color_filter, self.color_correction, self.white_balance, self.bit_depth)
        
    def __enter__(self, TLCameraSDK):
        return self
    
    def __exit__(self):
        return False
        
    def pic_collect(self, save=False):
        frame = self.TLCamera.get_pending_frame_or_null()
        image_buffer = frame.image_buffer
        self.TLCamera.disarm()
        image_array = MonoToColorProcessor.transform_to_24(image_buffer, self.roi_size, self.roi_size)
        image_array = np.reshape(image_array, (self.roi_size, self.roi_size, 3))
        if save:
                img = Image.fromarray(image_array)
                img_name = self.path + str(int(time.time())) +'.jpg'
                # img.convert('RGB').save(img_name)
                img.save(img_name)
                # img.show()
                #print(img_name)
        return image_array


if __name__ == '__main__':

    with tl_camera.TLCameraSDK() as TLCameraSDK, tl_mono_to_color_processor.MonoToColorProcessorSDK() as MonoToColorProcessorSDK: #should be called only once
        with Camera(TLCameraSDK,MonoToColorProcessorSDK) as camera1, Camera(TLCameraSDK,MonoToColorProcessorSDK) as camera2:
            for i in range(3):
                image = camera1.pic_collect()
                img = Image.fromarray(image_array)
                img.show()