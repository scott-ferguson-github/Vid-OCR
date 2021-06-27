#!/usr/bin/env python3
import os
import cv2
import numpy as np
# ------------------------------------------------------------------
# outimg = cv2.GaussianBlur(image, kernelsize, stdev)
#      kernelsize = (x,y) = width and height of kerenl
#      stdev  (can be a tuple representing the stdev of the kernel)
#             if one number ... it uses the same for x and y
#             if 0 it "calculates it from the kernel size".
# outimg = cv2.addWeighted(img1, wgt1, img2, wgt2)
# outimg = cv2.filter2D(img, ddepth, kernel)
#      ddepth is destination depth; -1 means to use same depth as input
#      kernel = convulution matrix (https://en.wikipedia.org/wiki/Kernel_(image_processing))
#               (specified as a numpy array of arrays)
# Example:  https://theailearner.com/tag/cv2-addweighted/
#
# Interesting blur detection article: https://www.pyimagesearch.com/2015/09/07/blur-detection-with-opencv/
# ------------------------------------------------------------------
outdir = "BlueAndSharpen"
if not os.path.isdir(outdir):
    os.mkdir(outdir)
vid = cv2.VideoCapture('pages.mp4')
framenum = 0
while (vid.isOpened()):
    ret, frame = vid.read()
    if not ret: break
    grayframe = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    grayframe = cv2.rotate(grayframe, cv2.ROTATE_180)
    cv2.imwrite(outdir+"/pages.%06d.gray.tiff" % framenum, grayframe)
    blur3 = cv2.GaussianBlur(grayframe, (3,3), 0)
    blur5 = cv2.GaussianBlur(grayframe, (5,5), 0)
    blur9 = cv2.GaussianBlur(grayframe, (9,9), 0)
    blur15 = cv2.GaussianBlur(grayframe, (15,15), 0)
    for pct in range(30, 110, 10):
        sharpen3 = cv2.addWeighted(grayframe, 1.0+pct/100.0, blur3, -pct/100.0, 0)
        sharpen5 = cv2.addWeighted(grayframe, 1.0+pct/100.0, blur5, -pct/100.0, 0)
        sharpen9 = cv2.addWeighted(grayframe, 1.0+pct/100.0, blur9, -pct/100.0, 0)
        sharpen15 = cv2.addWeighted(grayframe, 1.0+pct/100.0, blur15, -pct/100.0, 0)
        cv2.imwrite(outdir+"/pages.%06d.blur03.%02d.tiff" % (framenum, pct), sharpen3)
        cv2.imwrite(outdir+"/pages.%06d.blur05.%02d.tiff" % (framenum, pct), sharpen5)
        cv2.imwrite(outdir+"/pages.%06d.blur09.%02d.tiff" % (framenum, pct), sharpen9)
        cv2.imwrite(outdir+"/pages.%06d.blur15.%02d.tiff" % (framenum, pct), sharpen15)
    skernel1 = np.array( [[0, -1, 0], [-1, 5, -1], [0, -1, 0]] )
    sharp = cv2.filter2D(grayframe, -1, skernel1)
    cv2.imwrite(outdir+"/pages.%06d.filter2D.tiff" % framenum, sharp)
    if framenum>=40: break
    framenum += 1
vid.release()
cv2.destroyAllWindows()
