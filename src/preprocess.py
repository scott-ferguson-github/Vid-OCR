# ------------------------------------------------------------------
# Copyright  Scott Ferguson, 2021
# Copyright  Ken Ferguson, 2021
#      License is GPLv2 only as part of the Vid-OCR project.
# ------------------------------------------------------------------
# Functions to do preprocessing of the video frames before
# submitting them for OCR.
# ------------------------------------------------------------------
import numpy as np
import sliceutil as  slu
import cv2

# Just a short list of some useful convolution
# kernels.  Expand as necessary.
kernels = { 'edgedetect': np.array([ [ 0, 1, 0],
                                     [ 1, -4, 1],
                                     [ 0, 1, 0]]),
            'edgedetect_unif': np.array([ [ 1, 1, 1],
                                          [ 1, -8, 1],
                                          [ 1, 1, 1]]),
            'sharpen': np.array([ [ 0, -1, 0],
                                  [ -1, 5, -1],
                                  [ 0, -1, 0]])
}


def edgedetect(image, kernel = None):
    """
    edgedetect
       Given a opencv grayscale image, apply a kernel
       transform to detect edges.
    image = opencv grayscale image
    kernel = (optional) kernel to be applied
    """
    if kernel is None:
        kernel = kernels['edgedetect_unif']
    return cv2.filter2D(image, -1, kernel)

def block_stdev(image, blockdim = (15,15)):
    """
    block_stdev
       Given an opencv image (or any 2-D numpy array),
       break it into blockdim sized blocks that tile
       the image.  Return a numpy array giving the
       stdev of each of those tiles.
    """
    # Get an array of array of 2-tuples of slices.  The
    # 2-tuple of slices is a rectangle the represents the tile
    tiles = slu.tile_grid( np.shape(image), blockdim )
    result = np.zeros( (len(tiles), len(tiles[0])) )
    for row in range( np.shape(result)[0] ):
        for col in range( np.shape(result)[1]):
            result[row,col] = image[tiles[row][col]].std()
    return result

def scale2image( nparray, minval = 0, maxval = 255, outtype = np.uint8 ):
    """
    scale2image
        Given a 2D numpy array of possible float values, rescale this to a
        grayscale image.
    nparray  =  incoming 2D numpy array.  This is not changed.
    optional arguments:  minval=0, maxval=255, outtype = np.uint8

    Returns a numpy array rescaled to be a grayscale image (np.uint8 values)
    """
    curminval, curmaxval = nparray.min(), nparray.max()
    return ((nparray-curminval)*maxval/(curmaxval-curminval)).astype(outtype)


def __get_image_from_std_edgedetect_blocks(image, blockdim = (15,15)):
    # Apply edgedetect filter
    edged = edgedetect(image)
    # Get stdev of the tiling with blockdim sized blocks
    return scale2image(block_stdev(edged, blockdim = blockdim))

def __get_black_runs(imageslice):
    """
    get_black_runs    Private Routine
        imageslice = column or row from a grayscale image
    Returns a list of slice objects (step=1).  Recall that for a
    slice object s you can do s.start, s.stop, ...
    """
    indicesblack = np.where(imageslice==0)[0] # where is a 1-tuple in this case
    return slu.indices2slices(indicesblack)

def __get_longest_blackish_runs(image, colnum=None, rownum=None, gappct=0.3):
    """
    __get_longest_blackish_runs  Private Routine
        image = grayscale image
        colnum or rownum = column number or row number to consider
        pct = allow non-black gaps as long as gap < 1-pct of sum of
            the side black parts
    """
    if colnum is not None:
        sl = image[:, colnum]
    elif rownum is not None:
        sl = image[rownum, :]
    else:
        raise Exception("Error.  Must specify colnum or rownum.")
    runs = __get_black_runs(sl)
    if len(runs) == 0: return None
    filledruns = slu.fillgaps_slicelist(runs, gappct=gappct, verify=True)
    runlen, run = max( (slu.slicelen(r), r) for r in filledruns)
    return run

def __maxrect(sl, slicelist):
    """
    __maxrect  Private Routine
       sl = slice of indices into slicelist
       slicelist  = list of slices

       Think of sl as a run of indices as the biggest base of a rectangle.
       Think of slicelist as a list of vertical slices that contain a column
       of the 'maximum rectangle'.

       Outputs the maximum rectangle as a 2-tuple of slices
    """
    # We will consider the slicelist as column slices and use
    # the terms top and bottom
    start, stop, maxlen = sl.start, sl.stop, sl.stop-sl.start
    maxarea = 0
    outslice = None
    # Loop over all possible width of rectangles ... and for
    # each width all possible bases (given by left side) in sl
    for width in range(1, maxlen+1):
        for left in range(start, stop-width+1):
#            print("width, left, start, stop len(slicelist):", width, left, start, stop, len(slicelist))
            toprect = min( [slicelist[i].stop for i in range(left, left+width)])
            botrect = max( [slicelist[i].start for i in range(left, left+width)])
            if toprect > botrect:
                area = width * (toprect-botrect)
                if area>maxarea:
                    maxarea = area
                    outrect = ( slice(botrect, toprect), slice(left, left+width))
    return outrect

# Private routine for find_margins
def __find_black_rectangles(margindetect, gappct=0.3):
    """
    __find_black_rectangles   Private routine
    """
    runs = [ __get_longest_blackish_runs(margindetect, colnum=col, gappct=gappct) \
             for col in range(np.shape(margindetect)[1]) ]
    #    if runs is None or len(runs) == 0: return None # maybe delete
    marginlen = 0.5 * np.shape(margindetect)[0]
    # Find indices of runs with lengths more than marginlen
    runindex = [ i for (i,run) in enumerate(runs) if run is not None and slu.slicelen(run) >= marginlen ]
    # Convert these indices into slices
    slices_of_runs = slu.indices2slices(runindex)
    # Find the maximum rectangle contained in these slices of black-runs
    rectangles = [ __maxrect(r, runs) for r in slices_of_runs]
    return rectangles

def __vertical_rect(rect):
    return slu.slicelen(rect[0]) >= slu.slicelen(rect[1])

def __find_leftright_edges_old(margindetect, leftpct=0.6, gappct=0.3, debug=False):
    """
    __find_leftright_edges   Private routine
    """
    fnname = "__find_leftright_edges"
    # Find the biggest black rectangles in the margindetect image
    # Each rectangle is a 2-tuple of slices (rowslice, colslice)
    rectangles = __find_black_rectangles(margindetect, gappct=gappct)
    if debug: print(fnname + " Rectangles: ", rectangles)
    # Left Margin is the largest rectangle on the left side of the page margindetect image
    # Do same for right margin.
    lside, rside = leftpct * np.shape(margindetect)[1], (1-leftpct) * np.shape(margindetect)[1]
    lrects = [rect for rect in rectangles if rect[1].start < lside and __vertical_rect(rect)]
    rrects = [rect for rect in rectangles if rect[1].stop > rside and __vertical_rect(rect)]
    if debug:
        print(fnname + " lrects:", len(lrects), lrects)
        print(fnname + " rrects:", len(rrects), rrects)
    # max throws a ValueError if the list is empty
    try:
        larea, lrect = max([(slu.slicelen(rect[0])*slu.slicelen(rect[1]), rect) for rect in lrects])
        left = lrect[1].stop-1
    except ValueError:
        left = 0
    try:
        rarea, rrect = max([(slu.slicelen(rect[0])*slu.slicelen(rect[1]), rect) for rect in rrects])
        right = rrect[1].start
    except ValueError:
        right = np.shape(margindetect)[1]
    if debug:
        print(fnname + " left:", left, larea)
        print(fnname + " right:", right, rarea)
    return left, right

#  I don't really like the shape of this code yet.  It's a bit too
#  ad-hoc at getting rid of the background vs. the margins.
def __find_leftright_edges(margindetect, leftpct=0.6, gappct=0.3, debug=False):
    """
    __find_leftright_edges   Private routine
    """
    fnname = "__find_leftright_edges"
    # Find the biggest black rectangles in the margindetect image
    # Each rectangle is a 2-tuple of slices (rowslice, colslice)
    rectangles = __find_black_rectangles(margindetect, gappct=gappct)
    if debug: print(fnname + " Rectangles: ", rectangles)
    # Left Margin is the largest rectangle on the left side of the page margindetect image
    # Do same for right margin.
    # Update:  Sometimes the "largest" as background instead of margin.  We now will
    # give the inner rectangle ... as long as it doesn't skip text (e.g. the gap between
    # rectangles is less than the inner rectang
    lside, rside = leftpct * np.shape(margindetect)[1], (1-leftpct) * np.shape(margindetect)[1]
    lrects = [rect for rect in rectangles if rect[1].start < lside and __vertical_rect(rect)]
    rrects = [rect for rect in rectangles if rect[1].stop > rside and __vertical_rect(rect)]
    if debug:
        print(fnname + " lrects:", len(lrects), lrects)
        print(fnname + " rrects:", len(rrects), rrects)
    # Sort the area, baseslice rectangles. Keep iterating through the possible
    # margins (by area) as long as the next one has a small enough gap.  While
    # the thought is that we are going out-->in ... we are really iterating by area
    # so if the biggest area is inside _the_next_biggest_area we are still done
    area_basesl = sorted([(slu.slicelen(rect[0])*slu.slicelen(rect[1]), rect[1]) for rect in lrects], reverse=True)
    larea, leftmargin = 0, slice(0,0)
    while len(area_basesl) > 0:
        larea, leftmargin = area_basesl.pop(0)
        if debug: print("left now: ", leftmargin)
        if len(area_basesl) > 0:
            nextbase = area_basesl[0][1]
            if debug: print("Test: ", nextbase, nextbase.start-leftmargin.stop, slu.slicelen(nextbase))
            if (nextbase.start < leftmargin.stop): break
            if (nextbase.start - leftmargin.stop) > slu.slicelen(nextbase): break
    # Now do the right hand margin
    area_basesl = sorted([(slu.slicelen(rect[0])*slu.slicelen(rect[1]), rect[1]) for rect in rrects], reverse=True)
    rarea, rightmargin = 0, slice(0,0)
    while len(area_basesl) > 0:
        rarea, rightmargin = area_basesl.pop(0)
        if debug: print("right now: ", rightmargin)        
        if len(area_basesl) > 0:
            nextbase = area_basesl[0][1]
            if debug: print("Test: ", nextbase, rightmargin.start - nextbase.stop, slu.slicelen(nextbase))
            if (rightmargin.start < nextbase.stop): break
            if (rightmargin.start - nextbase.stop) > slu.slicelen(nextbase): break
    if debug:
        print(fnname + " left:", leftmargin, larea)
        print(fnname + " right:", rightmargin, rarea)
    return leftmargin.stop-1, rightmargin.start

def find_margins(image, bthresh=30, gappct = 0.3):
    """
    find_margins  Find the left, right, top and bottom margins.

                  Returns dictionary with keys 'left', 'right', 'top', 'bottom'
                  The left and right elements are column numbers, while the
                  top and bottom elements are row numbers.

    Arguments:
       image       The grayscale image of the page.  Not changed.
       bthresh=30  Black threshold on margindetected image (technical parameter)
                   The higher this is set, the larger/more possible margins found.
       gappct=0.3  Fills gaps on runs (vertical runs if leftright=True) if the gap is
                   less than 30% of the top/bottom pure-black.
    """
    # Margins will be found using low-stdev blocks in the edge-detect-filtered image
    blocksize = (15, 15)
    margindetect = __get_image_from_std_edgedetect_blocks(image, blockdim = blocksize)
    margindetect[ margindetect <= bthresh ] = np.uint8(0)

    left, right = __find_leftright_edges(margindetect, leftpct=0.6, gappct=gappct, debug=True)
    # Truncate left and right sides of margindetect before finding top and bottom margins
    # We find top/bottom rectangles by getting left/right rectangles on the transpose
    trunc_transpose = margindetect[:, left:right].transpose()
    top, bottom = __find_leftright_edges( trunc_transpose, leftpct=0.6, gappct=gappct, debug=True)
    # The above were edges in the margindetect blocks.  Convert to image
    result = {}
    result['top'], result['left'] = top * blocksize[0], left * blocksize[1]
    result['bottom'], result['right'] = bottom * blocksize[0], right * blocksize[1]
    result['bottom'] = min( np.shape(image)[0], result['bottom'])
    result['right'] = min( np.shape(image)[1], result['right'])
    return result


def remove_outer(image, blocksize = 9, cutoff = 128):
    """remove_outer
    image = grayscale image from opencv
    blocksize = odd number size sequence of blocks to analyze
    cutoff = uint8 from 0 to 255; will result in True for a block
             if the average over the block is <= cutoff (blacker).
    
    From the outer edges (left, right, top, bottom)  moving inward,
    convert all blocks whose average is <= cutoff to white (255).
    """
    pass

def remove_speckles(image):
    """remove_speckes
    image = grayscale image from opencv
    blocksize = default 5, dimension of blocks to analyze.  Must be odd.
    percentage = percentage of pixels in block >= cutoff necessary to
                 change center pixels to white (255).

    """
    pass

def threshold_to_white(image):
    pass

def threshold_to_bw(image):
    pass

def find_best_shift_matrix(image1, image2, blocksize, hint = None):
    """find_shift_matrix
    image1, image2 = two grayscale images
    blocksize = default to 30 pixels
    hint = optional starting point for a shift matrix
    
    Goal is, for each blocksize x blocksize block, to find the x and y shift
    to align the block in image1 with the best match in image2.  The algorithm
    presumes shifts in adjacent blocks are similar and don't create more than
    1 pixel overlaps.
    """
    pass

# We should study whether we should pre-process first (e.g. apply some
# sort of gaussian filter.
def prob_text_block(image, ):
    """probability_in_text

    For each pixel in the image, estimate the probability that the
    pixel is in a text block.  We will do this by calculating the
    the standard deviation of a edge-detection-convolution
    """
    pass


