#!/usr/bin/env python3
import os
import cv2
import numpy as np
outdir = "canny"
if not os.path.isdir(outdir):
    os.mkdir(outdir)
vid = cv2.VideoCapture('pages.mp4')
framenum = 0
while (vid.isOpened()):
    ret, frame = vid.read()
    if not ret: break
    grayframe = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    grayframe = cv2.rotate(grayframe, cv2.ROTATE_180)
    edge = cv2.Canny(grayframe, 100, 200)
    if framenum == 22:
        f = open("edge.txt", "w")
        for row in edge:
            f.write(",".join(map(str,row)) + "\n")
    cv2.imwrite(outdir+"/pages.%06d.edge.tiff" % framenum, edge)
    if framenum == 0:
        print(edge)
    framenum += 1
vid.release()
cv2.destroyAllWindows()
