#!/usr/bin/env python3
import os
import cv2
from matplotlib import pyplot as plt
# ------------------------------------------------------------------
# cv2.adaptiveThreshold()
#     cv.adaptiveThreshold(image, maxval, method, threshtype, blocksize, C)
#            cv.THRESH_BINARY,11,2)
#      method = ADAPTIVE_THRESH_MEAN_C, ADAPTIVE_THRESH_GAUSSIAN_C,
#      threshtype = THRESH_BINARY, THRESH_BINARY_INV, THRESH_TRUNC,
#                   THRESH_TO_ZERO,...
#      blocksize = int number of pixels in neighborhood to determine
#                  threshold value
#      C = int to be subtracted from the mean (or weighted mean).
#
#  We will use Gaussian and experiment with the blocksize.  The larger
#  the blocksize the slower it will be (likely).  I will look at
#  just C=2 ... but it seems to me that it's irrelevant???
# ------------------------------------------------------------------
outdir = "bwpages_adaptive"
if not os.path.isdir(outdir):
    os.mkdir(outdir)
vid = cv2.VideoCapture('pages.mp4')
framenum = 0
thresh = [1]*5
threshmethod = cv2.ADAPTIVE_THRESH_GAUSSIAN_C
threshtype = cv2.THRESH_BINARY
c = 5
while (vid.isOpened()):
    ret, frame = vid.read()
    if not ret: break
    grayframe = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    grayframe = cv2.rotate(grayframe, cv2.ROTATE_180)
    for i in range(5):
        thresh[i] = cv2.adaptiveThreshold(grayframe, 255, threshmethod, \
                                               threshtype, 5+6*i, c)
        cv2.imwrite(outdir + '/pages.%06d.%03d.%02d.tiff' % (framenum, 5+6*i, c), thresh[i])

    if framenum>=40: break
#    plt.subplot(3,2,1)
#    plt.imshow(grayframe,'gray')
#    plt.title("Original Grayscale")
#    plt.xticks([]), plt.yticks([])
#    for i in range(5):
#        plt.subplot(3,2,i+2)
#        plt.imshow(thresh[i], 'gray')
#        plt.title("Frame %d; Blocksize %d" % (framenum, 5+4*i))
#        plt.xticks([]), plt.yticks([])
#    plt.savefig(outdir + '/pages.%06d.tiff' % framenum)
#    plt.show()
#    print("Waiting for a keypress")
#    cv2.waitKey(0) # Without this imshow does nothing
#    plt.close()
    framenum += 1
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
