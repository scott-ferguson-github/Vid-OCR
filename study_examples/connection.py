#!/usr/bin/env python3
import os
import cv2
import numpy as np
outdir = "canny"
if not os.path.isdir(outdir):
    os.mkdir(outdir)
vid = cv2.VideoCapture('pages.mp4')
framenum = 0

def find_next(edge,rownum,colnum):
    if edge[rownum+1][colnum-1] == 255:
        return rownum+1, colnum - 1
    if edge[rownum+1][colnum] == 255:
        return rownum+1, colnum
    if edge[rownum+1][colnum+1] == 255:
        return rownum+1, colnum + 1
    print("end: " , rownum,colnum," from: ",end = " ")

    return 0,0

while (vid.isOpened()):
    ret, frame = vid.read()
    if not ret: break
    grayframe = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    grayframe = cv2.rotate(grayframe, cv2.ROTATE_180)
    edge = cv2.Canny(grayframe, 100, 200)
    if framenum == 22:
        #f = open("edge.txt", "w")
        rownum = 0
        colnum = 0
        for row in edge:
            for col in row:
                if rownum == 50:
                    #print(col,end = " ")
                    #print(edge[rownum][colnum],end = " ")
                    if edge[rownum][colnum] == 255:
                        notbroken = True
                        length = 0
                        chRow = rownum
                        chCol = colnum
                        while (notbroken):
                            chRow,chCol = find_next(edge,chRow,chCol)
                            if chRow == 0:
                                notbroken = False
                            length += 1
                        print(rownum,colnum, "length :  ",length)

                colnum += 1
            rownum += 1
            colnum = 0
            #f.write(",".join(map(str,row)) + "\n")
    #cv2.imwrite(outdir+"/pages.%06d.edge.tiff" % framenum, edge)
    #if framenum == 0:
        #print(edge)
    framenum += 1
vid.release()
cv2.destroyAllWindows()

