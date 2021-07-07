#!/usr/bin/env python3
import os
import cv2
import numpy as np
outdir = "canny"
if not os.path.isdir(outdir):
    os.mkdir(outdir)
vid = cv2.VideoCapture('pages.mp4')
framenum = 0


#Checks the pixels : Directly below, below to the left, and below to the right
#to see if they are also white
#returns the row,col of the first white pixel found or 0,0 if not found
#TODO - check more pixels?  - return false condition better? - make horizontal option?
def find_next(edge,rownum,colnum):
    if edge[rownum+1][colnum-1] == 255:
        return rownum+1, colnum - 1
    if edge[rownum+1][colnum] == 255:
        return rownum+1, colnum
    if edge[rownum+1][colnum+1] == 255:
        return rownum+1, colnum + 1
    #print("end: " , rownum,colnum," from: ",end = " ")

    return rownum,colnum #have it return a boolean with it maybe?, then not 0,0 so outputting is better

def find_next_up(edge,rownum,colnum):
    if edge[rownum-1][colnum-1] == 255:
        return rownum-1, colnum - 1
    if edge[rownum-1][colnum] == 255:
        return rownum-1, colnum
    if edge[rownum-1][colnum+1] == 255:
        return rownum-1, colnum + 1
    #print("end: " , rownum,colnum," from: ",end = " ")

    return rownum,colnum #have it return a boolean with it maybe?, then not 0,0 so outputting is better

#CHECK IF ANY LINES IN THE LIST MATCH ANOTHER LINE - by being too near or by slope
def check_same_lines(line_list):
    slope_list = []
    pair_list = []
    for line in line_list:
        print(line)
        slope = ( (line[3] - line[0]) / (line[4] - line[1])  )

        #might want to check here to see if there is a slope that already matches --
        i = 0
        for s in slope_list:

            if ( (slope - s) / slope > -0.2 and (slope - s) / slope < 0.2):
                pair_list.append( (i, len(slope_list)) )
            
            i += 1

        slope_list.append(slope)

    print(pair_list, "PAIR LIST")
    print(slope_list, " SLOPES")
    
    
    
    

while (vid.isOpened()):
    ret, frame = vid.read()
    if not ret: break
    grayframe = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    grayframe = cv2.rotate(grayframe, cv2.ROTATE_180)
    edge = cv2.Canny(grayframe, 100, 200)
    if framenum == 22:
        #f = open("edge.txt", "w")
        colnum = 0
        rows = [50,150,250,350,450,550,650,750,850,950]
        lineBottoms = []
        for row in rows: #remove these loops as they are, only loop through certain rows, not every row
            for col in edge[row]: #probably make row list [100,200,etc..] , then for col in edge[row] 


            #above comments partial done
            
                    #print(col,end = " ")
                    #print(edge[rownum][colnum],end = " ")
                if edge[row][colnum] == 255:
                    
                    notbroken = True
                    length = 0
                    chRow = row
                    chCol = colnum
                    tmpR = 0

                    chRowUp = row
                    chColUp = colnum
                    tmpRUp = 0
                    #DO NOT NEED LENGTH UP, DIFFERENT LOOPS THAT ARE NOT DEPENDENT ON IT TO STOP
                    notBrokenUp = True

                    while (notbroken):
                        tmpR,chCol = find_next(edge,chRow,chCol)
                        if tmpR == chRow:
                            notbroken = False
                        else: 
                            chRow = tmpR
                        length += 1
                    
                    while (notBrokenUp):
                        tmpRUp,chColUp = find_next_up(edge,chRowUp,chColUp)
                        if tmpRUp == chRowUp:
                            notBrokenUp = False
                        else: 
                            chRowUp = tmpRUp
                        length += 1

                    if (length > 50):
                        #print(row,colnum, "length :  ",length)
                        #add the line to the list lineBottoms
                        notIn = True
                        for i in lineBottoms:
                            y = i[1]
                            if (chCol == y): #probably change to within 5 columns
                                notIn = False

                        if notIn:
                            lineBottoms.append( (chRow,chCol,length,chRowUp,chColUp) )
                        
                    


                colnum += 1
            
            colnum = 0


        for i in lineBottoms:
            x,y,z = i[0] , i[1], i[2] 
            print(x,y," length:",z)
        print(lineBottoms)
        check_same_lines(lineBottoms)
            
            #f.write(",".join(map(str,row)) + "\n")
    #cv2.imwrite(outdir+"/pages.%06d.edge.tiff" % framenum, edge)
    #if framenum == 0:
        #print(edge)
    framenum += 1
vid.release()
cv2.destroyAllWindows()

