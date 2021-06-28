#!/usr/bin/env python3
import os
import cv2
import numpy as np
# ------------------------------------------------------------------
# We aim to see if it is easy to detect the sharpness of the image
# as a way to study which frames we should throw away.
#
# https://www.pyimagesearch.com/2015/09/07/blur-detection-with-opencv/
# suggests using cv2.Laplacian(image, cv2.CV_64F).var() ... the
# variance of the laplacian.
#
# He also claims that the Laplacian is simply the convolution with
# the kernel.  I don't think so ... so let's look at that.
# [ [ 0, 1, 0],
#   [ 1, -4, 1],
#   [ 0, 1, 0] ]
#
# We will calculate the the above two numbers and simply print
# them to the console.  We will label the framenumbers starting
# at 1 ... to agree with the "pages/" subdirectory numbering.
# ------------------------------------------------------------------
outdir = "bwpages_adaptive"
if not os.path.isdir(outdir):
    os.mkdir(outdir)
vid = cv2.VideoCapture('pages.mp4')
framenum = 0
kernel = np.array([ [ 0, 1, 0],
                    [ 1, -4, 1],
                    [ 0, 1, 0]])
print(kernel)
while (vid.isOpened()):
    ret, frame = vid.read()
    if not ret: break
    grayframe = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    grayframe = cv2.rotate(grayframe, cv2.ROTATE_180)
    val1 = cv2.Laplacian(grayframe, cv2.CV_64F).var()
    val2 = cv2.filter2D(grayframe, -1, kernel).var()
    print("Framenum, laplacian, alt = %d, %f, %f" % (framenum+1, val1, val2))
    framenum += 1    
    if framenum>=40: break
vid.release()
