# Dynamic Box Fill Level Detection

A depth sensing application for measuring box fill levels using OAK-D camera. This project was inspired by the spatial calculation concepts from Luxonis' DepthAI examples.

## 🔄 Key Modifications & Features

### 1. Enhanced ROI System
- **Flexible ROI Sizing**: Users can now adjust ROI to any size needed for their specific box dimensions
- **Dynamic Adjustment**: Real-time ROI size modification using keyboard controls
- **Visual Feedback**: Clear visualization of the selected area

### 2. Improved Depth Calculation
- **Original Method**: Only showed the closest pixel's depth within ROI
- **New Method**: 
  - Calculates average depth across entire ROI area
  - Provides more accurate representation of fill level
  - Better handles variations in content distribution

### 3. Calibration System
- **Empty Box Calibration**: Records baseline measurement
- **Full Box Calibration**: Sets reference for 100% fill level
- **Interactive Process**: Simple keyboard-controlled calibration procedure

## Installation
```bash
python3 -m pip install -r requirements.txt
```

## Usage

### Controls
- **WASD**: Move ROI position
- **R/F**: Increase/Decrease ROI height
- **T/G**: Increase/Decrease ROI width
- **[Add calibration controls here]**: For box calibration
- **Q**: Quit application

### Operation Steps
1. Position your box in the camera's view
2. Adjust ROI size to match box dimensions
3. Perform empty box calibration
4. Perform full box calibration
5. Begin monitoring fill levels

## Technical Features
- Real-time depth monitoring
- Configurable ROI dimensions
- Average depth calculation within ROI
- Percentage-based fill level display

## Requirements
- OAK-D camera
- Python 3.x
- OpenCV
- DepthAI
- NumPy

## Notes
- Ensure consistent lighting conditions during operation
- Keep box position stable after calibration
- Larger ROI size provides more stable measurements
```

### Regular Operation
```bash
python3 main.py
```

### Controls
- **WASD**: Move the ROI to position over the box
- **R/F**: Adjust ROI height to match box height (recommend 30 pixels minimum)
- **T/G**: Adjust ROI width to match box width (recommend 30 pixels minimum)
- **Q**: Quit application

## Technical Details

### Depth Analysis Improvement
```python
# Original method (simplified):
depth_center = depthROI[center_y, center_x]
depth_avg = np.mean(depthROI)

# New method (simplified):
depth_matrix = depthROI[ymin:ymax, xmin:xmax]  # Full ROI analysis
valid_depths = depth_matrix[depth_matrix > threshold]
```

### Important Notes
- Minimum recommended ROI size is 30x30 pixels for accurate measurements
- Calibration should be performed in consistent lighting conditions
- Keep the box position stable after calibration for best results

## Requirements
- OAK-D camera or similar DepthAI-compatible device
- Python 3.x
- OpenCV
- DepthAI (`depthai`)
- NumPy










# Calculate spatial coordinates on the host

This example shows how to calcualte spatial coordinates of a ROI on the host and gets depth frames from the device. Other option is to use [SpatialLocationCalculator](https://docs.luxonis.com/projects/api/en/latest/components/nodes/spatial_location_calculator/) to calcualte spatial coordinates on the device.

If you already have depth frames and ROI (Region-Of-Interest, eg. bounding box of an object) / POI (Point-Of-Interest, eg. feature/key-point) on
the host, it might be easier to just calculate the spatial coordiantes of that region/point on the host, instead of sending depth/ROI back
to the device.

**Note** using single points / tiny ROIs (eg. 3x3) should be avoided, as depth frame can be noisy, so you should use **at least 10x10 depth pixels
ROI**. Also note that to maximize spatial coordinates accuracy, you should define min and max threshold accurately.

## Demo

![Demo](https://user-images.githubusercontent.com/18037362/146296930-9e7071f5-33b9-45f9-af21-cace7ffffc0f.gif)

## Installation

```
python3 -m pip install -r requirements.txt
```
