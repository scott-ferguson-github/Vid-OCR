

#This is supposed to take two images that are cut by margins
# - grayscale or thresholded
# and a block size, and return the placement of blocks onto each other

# the placement of blocks onto each other should be formatted as
# a tuple with : the original slice placement and the new slice placement

#Find the best placement for blocks by using the square difference or absolute difference

#PLACING BLOCKS FROM IMG1 ONTO IMG2

#For getting the top left block of img1 to match on top left of img2
#----
# probably a similar method as below with the exceptions that -
# - expected area is just the same coordinates, or same coordinates relative to the margin
# - increase the area used for checking
# - 


# For getting the rest after top left (should be easier)
# arguments needed / used (other than block size / imgs) ---
# ---slice for location determined of last block on img2
# ---slice for either last block of img1 or this block of img1
# - get the slice for the next block of img1
# - check the abs/sq difference of 'default next location' 
#           - for ( i = expected - checking_width; I < start + checking_width; i++  )  ---- i is start of slice, separate for x and y?
#           - making checking slice as : slice = i:i+blocksize for x and y
#           - keep track of best match so far
#           - use the sum of the abs differences with the methods dad used earlier. 
# - check it for locations 'around' default next - area of 1/2 - 2 blocks around? determine
# - return the 'determined location slice'


def block_placement(img1, img2, block_size, ):
    slice_list = #list of img1 slices to be used 

    for slc in slice_list:
        place_block()


#block_size is either tuple or number
#slc is the slice (tuple of 2 slices?) from img1 that will be placed on img2
#looking_location is the area where we are expecting this block to be placed.
def place_block(img1,img2,block_size,slc,looking_location):
    startx, starty = lookinglocation #the starting location for looking
    checking_width = block_size #how far from looking location to check around
    current_slice = slice(0:4)#the current minimum slice
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
                current_slice = checking_slice
    
    return current_slice #might also return min_abs


def get_abs_difference(img1,img2,slc1,slc2):
    pass

