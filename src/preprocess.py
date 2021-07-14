# ------------------------------------------------------------------
# Copyright  Scott Ferguson, 2021
# Copyright  Ken Ferguson, 2021
#      License is GPLv2 only as part of the Vid-OCR project.
# ------------------------------------------------------------------
# Functions to do preprocessing of the video frames before
# submitting them for OCR.
# ------------------------------------------------------------------
import numpy as np

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


