#!/usr/bin/env python3
import cv2

vid = cv2.VideoCapture('pages.mp4')
framenum = 0
while (vid.isOpened()):
    ret, frame = vid.read()
    if not ret: break
    framenum += 1
    cv2.imshow("frame %d" % framenum, frame)
    cv2.imwrite('pages/pages.%06d.tiff' % framenum ,frame)
vid.release()
cv2.destroyAllWindows()
# cv2.waitKey(0) and cv2.waitKey(1) allow
# you to press keys and compare against ord('c')
# 0 waits for you ... while 1 waits 1 ms.
#
# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#
# and for BW ... it's just 0/255 grayscale
# (thresh, blackAndWhiteImage) = cv2.threshold(grayImage, 127, 255, cv2.THRESH_BINARY)
#
# 1.  Need to handle rotation!!!  Detect and perform!!!
# frame = cv2.rotate(frame, cv2.ROTATE_180)
#
# 2.  Need to find the edges of the page.
#     a.  For a grayscale image, one can use cv2.Canny( ...)
# https://www.pyimagesearch.com/2021/05/12/opencv-edge-detection-cv2-canny/

