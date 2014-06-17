
import cv2.cv as cv
# Parameters for haar detection
# From the API:
# The default parameters (scale_factor=2, min_neighbors=3, flags=0) are tuned
# for accurate yet slow object detection. For a faster operation on real video
# images the settings are:
# scale_factor=1.2, min_neighbors=2, flags=CV_HAAR_DO_CANNY_PRUNING,
# min_size=<minimum possible face size

min_size        = (5, 5)
image_scale     = 1
haar_scale      = 1.2
min_neighbors   = 4
haar_flags      = cv.CV_HAAR_DO_CANNY_PRUNING

TYPES_MAP = {
    'image': ['jpg']
}

COLOR_MAP = {
    'unknown': (128, 128, 255),
    'detected': (0, 255, 0),
    'false-positive': (0, 255, 255),
    'false-negative': (255, 0, 0)
}

DETECT_CODE = "___x___"
