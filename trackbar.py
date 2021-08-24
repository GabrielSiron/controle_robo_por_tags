import cv2
import numpy as np

def nothing(x):
    pass

# Create a black image, a window
cv2.namedWindow('image')

# create trackbars for color change
cv2.createTrackbar('R-l','image',0,255,nothing)
cv2.createTrackbar('G-l','image',0,255,nothing)
cv2.createTrackbar('B-l','image',0,255,nothing)
cv2.createTrackbar('R-h','image',0,255,nothing)
cv2.createTrackbar('G-h','image',0,255,nothing)
cv2.createTrackbar('B-h','image',0,255,nothing)

camera = cv2.VideoCapture(0)

while True:
    conf, frame = camera.read()
    frameHsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

    # get current positions of four trackbars
    r_l = cv2.getTrackbarPos('R-l','image')
    g_l = cv2.getTrackbarPos('G-l','image')
    b_l = cv2.getTrackbarPos('B-l','image')
    r_h = cv2.getTrackbarPos('R-h','image')
    g_h = cv2.getTrackbarPos('G-h','image')
    b_h = cv2.getTrackbarPos('B-h','image')

    mask = cv2.inRange(frameHsv, np.array([b_l, g_l, r_l]), np.array([b_h, g_h, r_h]))

    cv2.imshow('frame', frame)
    cv2.imshow('mask', mask)

cv2.destroyAllWindows()