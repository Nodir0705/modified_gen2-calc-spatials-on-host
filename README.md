# Dynamic Box Fill Level Detection

A depth sensing application for measuring box fill levels using OAK-D camera. This project was inspired by the spatial calculation concepts from Luxonis' DepthAI examples.

## 🔄 Key Modifications & Features

### 1. Improved Depth Calculation
- **Original Method**: Only showed the closest pixel's depth within ROI
- **New Method**: 
  - Calculates average depth across entire ROI area which is needed for getting accurate depth/fullness of box
  - Provides accurate representation of fill level
  - Display real-time percentage of fullness


### Operation Steps
1. Position your box in the camera's view
2. Adjust ROI size to match box dimensions
3. Perform empty box calibration
4. Perform full box calibration
5. Begin monitoring fill levels

## Installation
```bash
python3 -m pip install -r requirements.txt
```

### Controls
- **WASD**: Move ROI position
- **R/F**: Increase/Decrease ROI height
- **T/G**: Increase/Decrease ROI width
- **Q**: Quit application


## Requirements
- OAK-D camera
- Python 3.x
- OpenCV
- DepthAI
- NumPy

## Notes
- Ensure consistent lighting conditions during operation
- Keep box position stable after calibration

```
### Main script to start the process
```bash
python3 main.py
```


![depth](https://github.com/user-attachments/assets/78f29472-f6b8-4cfb-8ac7-6a7615a350a8)



