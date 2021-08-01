

#This is supposed to take two images that are cut by margins
# - grayscale or thresholded
# and a block size, and return the placement of blocks onto each other as a tuple

# the placement of blocks onto each other should be formatted as
# a tuple with : the original slice placement and the new slice placement
#note : each 'slice' will actually be a tuple of slices

#Find the best placement for blocks by using the square difference or absolute difference

#PLACING BLOCKS FROM IMG1 ONTO IMG2

#For getting the top left block of img1 to match on top left of img2
#----
# probably a similar method as below with the exceptions that -
# - expected area is just the same coordinates, or same coordinates relative to the margin
# - increase the area used for checking
# - 
# - Consider having a different starting point in the case of bad top left matches


# For getting the rest after top left (should be easier)
# arguments needed / used (other than block size / imgs) ---
# ---slice for location determined of last block on img2 - Or where expected location is
# ---slice for either last block of img1 or this block of img1
# - get the slice for the next block of img1
# - check the abs/sq difference of 'default next location' 
#           - for ( i = expected - checking_width; I < expected + checking_width; i++  )  ---- i is start of slice, separate for x and y?
#           - making checking slice as : slice = i:i+blocksize for x and y
#           - keep track of best match so far
#           - use the sum of the abs differences with the methods dad used earlier. 
# - check it for locations 'around' default next - area of 1/2 - 2 blocks around? determine
# - return the 'determined location slice'


#try to format the return from block_placement in the same way as tile_grid
# this being : list full of list , where each entry is a 2tuple of slices

import sliceutil as slu

def block_placement(img1, img2, block_size, ):
    slice_list = slu.tile_grid(np.shape(img1,block_size))#list of img1 slices to be used // same format as tile_grid in sliceutil
    #maybe want to get a sort of list of which tiles are in the margins

    for slc in slice_list:
        place_block()


#block_size is either tuple or number
#slc is the slice (tuple of 2 slices?) from img1 that will be placed on img2
#looking_location is the area where we are expecting this block to be placed.
def place_block(img1,img2,block_size,slc,looking_location):
    startx, starty = lookinglocation #the starting location for looking
    checking_width = block_size #how far from looking location to check around
    min_slice = slice(0:4)#the current minimum slice
    min_abs = 999999

    for (i = startx - checking_width ;  i < startx + checking_width; i+=1):
        for (j = starty - checking_width ;  j < starty + checking_width; j+=1):
            checking_slice = slice(i:i+block_size)#the slice that would result from the top_left being i,j
            
            abs = get_abs_difference(img1,img2,slc,checking_slice)
            #get the absolute difference from the looking location
            #something like for each: img1(slc) compare to img2(checking_slice)
            #probably just make another function for this

            if (abs < min_abs):
                min_abs = abs
                min_slice = checking_slice
    
    return current_slice #might also return min_abs, 


#find the absolute difference of grayscaled pixels
#comparing img1, slc1 to img2, slc2
#where slc1 and slc2 are rectangles/squares of pixels
def get_abs_difference(img1,img2,slc1,slc2):
    img1block = img1[scl1[0],slc1[1]].astype(int)
    img2block = img2[slc2[0],slc2[1]].astype(int)
    return np.sum(np.abs(img1block - img2block))


