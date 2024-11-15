#!/usr/bin/env python3
import cv2
import depthai as dai
from calc import HostSpatialsCalc
from utility import *
import numpy as np
import math

class ROISelector:
    def __init__(self):
        self.roi = None
        self.drawing = False
        self.start_point = None
        self.end_point = None

    def mouse_callback(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.drawing = True
            self.start_point = (x, y)
            self.end_point = (x, y)
            
        elif event == cv2.EVENT_MOUSEMOVE:
            if self.drawing:
                self.end_point = (x, y)
                
        elif event == cv2.EVENT_LBUTTONUP:
            self.drawing = False
            self.end_point = (x, y)
            # Create ROI with proper ordering of coordinates
            x1 = min(self.start_point[0], self.end_point[0])
            y1 = min(self.start_point[1], self.end_point[1])
            x2 = max(self.start_point[0], self.end_point[0])
            y2 = max(self.start_point[1], self.end_point[1])
            self.roi = (x1, y1, x2, y2)

class BoxAnalyzer:
    def __init__(self, box_height_mm):
        self.box_height_mm = box_height_mm
        self.ground_distance = None
        self.full_box_depth = None

    def calibrate_ground(self, depth):
        self.ground_distance = depth
        print(f"Empty Box distance calibrated: {self.ground_distance:.0f}mm")

    def calibrate_full_box(self, depth):
        self.full_box_depth = depth
        print(f"Full box depth calibrated: {self.full_box_depth:.0f}mm")

    def calculate_fullness(self, current_depth):
        if self.ground_distance is None or self.full_box_depth is None:
            return None
            
        total_range = self.ground_distance - self.full_box_depth
        current_range = self.ground_distance - current_depth
        fill_percentage = (current_range / total_range) * 100
        return max(0, min(100, fill_percentage))

# Create pipeline
pipeline = dai.Pipeline()

# Define sources and outputs
monoLeft = pipeline.create(dai.node.MonoCamera)
monoRight = pipeline.create(dai.node.MonoCamera)
stereo = pipeline.create(dai.node.StereoDepth)

# Properties
monoLeft.setResolution(dai.MonoCameraProperties.SensorResolution.THE_800_P)
monoLeft.setBoardSocket(dai.CameraBoardSocket.CAM_B)
monoRight.setResolution(dai.MonoCameraProperties.SensorResolution.THE_800_P)
monoRight.setBoardSocket(dai.CameraBoardSocket.CAM_C)

stereo.initialConfig.setConfidenceThreshold(255)
stereo.setLeftRightCheck(True)
stereo.setSubpixel(False)

# Linking
monoLeft.out.link(stereo.left)
monoRight.out.link(stereo.right)

xoutDepth = pipeline.create(dai.node.XLinkOut)
xoutDepth.setStreamName("depth")
stereo.depth.link(xoutDepth.input)

xoutDepth = pipeline.create(dai.node.XLinkOut)
xoutDepth.setStreamName("disp")
stereo.disparity.link(xoutDepth.input)

# Connect to device and start pipeline
with dai.Device(pipeline) as device:
    # Initialize
    depthQueue = device.getOutputQueue(name="depth")
    dispQ = device.getOutputQueue(name="disp")
    text = TextHelper()
    hostSpatials = HostSpatialsCalc(device)
    roi_selector = ROISelector()
    box_analyzer = BoxAnalyzer(730)  # 730mm box height

    # Create window and set mouse callback
    cv2.namedWindow("depth")
    cv2.setMouseCallback("depth", roi_selector.mouse_callback)

    print("Instructions:")
    print("1. Click and drag to draw ROI")
    print("2. Press 'g' to calibrate empty box distance")
    print("3. Press 'f' to calibrate full box")
    print("4. Press 'c' to clear ROI")
    print("5. Press 'q' to quit")

    while True:
        depthData = depthQueue.get()
        disp = dispQ.get().getFrame()
        disp = (disp * (255 / stereo.initialConfig.getMaxDisparity())).astype(np.uint8)
        disp = cv2.applyColorMap(disp, cv2.COLORMAP_JET)

        if roi_selector.roi is not None:
            x1, y1, x2, y2 = roi_selector.roi
            
            # Get depth information for full ROI
            spatials, _ = hostSpatials.calc_spatials(depthData, roi_selector.roi)

            if not math.isnan(spatials['z']):
                current_depth = spatials['z']
                
                # Draw ROI
                text.rectangle(disp, (x1, y1), (x2, y2))

                # Display depth information
                y_offset = y1 - 60
                text.putText(disp, f"Current Depth: {current_depth:.0f}mm", (x1, y_offset))
                y_offset += 20

                text.putText(disp, "Avg Z: " + ("{:.1f}m".format(spatials['z']/1000) if not math.isnan(spatials['z']) else "--"), 
                            (x1, y_offset))
                y_offset += 20
                text.putText(disp, "Min Z: " + ("{:.1f}m".format(spatials['min_z']/1000) if not math.isnan(spatials['min_z']) else "--"), 
                            (x1, y_offset))
                y_offset += 20
                text.putText(disp, "Max Z: " + ("{:.1f}m".format(spatials['max_z']/1000) if not math.isnan(spatials['max_z']) else "--"), 
                            (x1, y_offset))
                y_offset += 20
                text.putText(disp, f"Valid: {spatials['valid_points']}/{spatials['total_points']}", 
                            (x1, y_offset))
                y_offset += 20

                if box_analyzer.ground_distance is not None:
                    text.putText(disp, f"Empty Box: {box_analyzer.ground_distance:.0f}mm", 
                               (x1, y_offset))
                    y_offset += 20

                if box_analyzer.full_box_depth is not None:
                    text.putText(disp, f"Full Box: {box_analyzer.full_box_depth:.0f}mm", 
                               (x1, y_offset))
                    y_offset += 20

                    fullness = box_analyzer.calculate_fullness(current_depth)
                    if fullness is not None:
                        text.putText(disp, f"Fullness: {fullness:.1f}%", (x1, y_offset))
                        
                        # Draw fullness bar
                        bar_height = 100
                        bar_width = 20
                        bar_x = x2 + 30
                        bar_y = y1
                        
                        cv2.rectangle(disp, (bar_x, bar_y), 
                                    (bar_x + bar_width, bar_y + bar_height), 
                                    (255, 255, 255), 2)
                        
                        fill_height = int(bar_height * (fullness / 100))
                        cv2.rectangle(disp, 
                                    (bar_x, bar_y + bar_height - fill_height),
                                    (bar_x + bar_width, bar_y + bar_height),
                                    (0, 255, 0), -1)

        elif roi_selector.drawing:
            cv2.rectangle(disp, roi_selector.start_point, 
                        roi_selector.end_point, (0, 255, 0), 2)

        cv2.imshow("depth", disp)

        key = cv2.waitKey(1)
        if key == ord('q'):
            break
        elif key == ord('c'):
            roi_selector.roi = None
            roi_selector.drawing = False
            roi_selector.start_point = None
            roi_selector.end_point = None
        elif key == ord('g'):
            if roi_selector.roi is not None:
                spatials, _ = hostSpatials.calc_spatials(depthData, roi_selector.roi)
                if not math.isnan(spatials['z']):
                    box_analyzer.calibrate_ground(spatials['z'])
        elif key == ord('f'):
            if roi_selector.roi is not None:
                spatials, _ = hostSpatials.calc_spatials(depthData, roi_selector.roi)
                if not math.isnan(spatials['z']):
                    box_analyzer.calibrate_full_box(spatials['z'])

    cv2.destroyAllWindows()