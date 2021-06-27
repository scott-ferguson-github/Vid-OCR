#!/usr/bin/env python3
import os
import cv2

outdir = "bwpages"
if not os.path.isdir(outdir):
    os.mkdir(outdir)
vid = cv2.VideoCapture('pages.mp4')
framenum = 0
while (vid.isOpened()):
    ret, frame = vid.read()
    if not ret: break
    grayframe = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    grayframe = cv2.rotate(grayframe, cv2.ROTATE_180)
    # threshold takes: frame, threshold, max, type
    ret, filterframe = cv2.threshold(grayframe, int(255*0.55), 255, cv2.THRESH_BINARY)
    framenum +=1 
#    cv2.imshow("frame %d" % framenum, filterframe)
#    cv2.waitKey(0) # Without this imshow does nothing
    cv2.imwrite(outdir + '/pages.%06d.tiff' % framenum , filterframe)
vid.release()
cv2.destroyAllWindows()

# Aside:  opencv has an adaptiveThreshold() routine too.
# https://docs.opencv.org/4.5.2/d7/d4d/tutorial_py_thresholding.html

# cv2.waitKey(0) and cv2.waitKey(1) allow
# you to press keys and compare against ord('c')
# 0 waits for you ... while 1 waits 1 ms.
#
# 1.  Need to handle rotation!!!  Detect and perform!!!
#
# 2.  Need to find the edges of the page.
#     a.  For a grayscale image, one can use cv2.Canny( ...)
# https://www.pyimagesearch.com/2021/05/12/opencv-edge-detection-cv2-canny/
