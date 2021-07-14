# ------------------------------------------------------------------
# sliceutil.py
#    Library of routines for slices.  As you know, slices
#    are instantiated by, for example: slice(a,b,c)
#    where a,b,c are int or None.  slice(a,b,c) can be
#    used for list or numpy array indexing by using slice(a,b,c) instead
#    of a:b:c.
#
# ------------------------------------------------------------------

def slicelen(s, asize=None):
    """
    slicelen returns the number of values in the slice.
       s = the slice for which we are calculating the length
       asize = the assumed array size we are indexing (optional,
               but it is required if the "stop" for the slice is None
               i.e. It will not give the length of unbounded slices.
    """
    if s.stop is None and asize is None:
        # Not sure if I should raise a ValueError or TypeError
        raise ValueError("slicelen requires an asize if the stop is None")
    if asize is None:
        asize = s.stop
    start, stop, step = s.indices(asize)
    return max(((stop - start -1) // step) + 1, 0)


def slice2indices(s, asize=None):
    """
    slice2indices return a list of indices for the slice
        s = slice
       asize = the assumed array size we are indexing (optional,
               but it is required if the "stop" for the slice is None)
    """
    if asize is None: asize = s.stop
    return list(range(*s.indices(asize)))

def indices2slices(indices):
    """
    indices2slices  returns a list of slices (of step 1) that condenses
                    the runs in the indicess.
         indices = list of indices
    """
    if len(indices) == 0: return []
    slices, start = [], indices[0]
    if len(indices) == 1: return [slice(start, start+1)]
    for ind, nextind in zip(indices, indices[1:]):
        if ind + 1 != nextind: # gap
            slices.append(slice(start, ind+1))
            start = nextind
    slices.append(slice(start,nextind+1))
    return slices

def slice_set_default(sl, asize=None):
    start, stop, step = sl.start, sl.stop, sl.step
    if start is None: start = 0
    if step is None: step = 1
    if stop is None: stop = asize
    return slice(start, stop, step)

def fillgaps_slicelist(lslices, gappct=0.0, gapsize=0, verify=True):
    """
    fillgaps_slicelist  returns a list of slices where small gaps
                        are filled in.  The gap size is given as
                        either a percentage of the surrounding
                        slices or as an absolute number.
        lslices = list of slices of step 1 in sequence (verified if verify=True)
        gappct = float.  If gappct = 0.1, then a gap is filled if
                        length(gap)/(length(leftslice)+length(rightslice)) <= 0.1
        gapsize = int    Gap is filled if length(gap)<=gapsize
        verify = boolean (default True).  First verify that slices are step
                         1 and in order relative to start

    """
    if len(lslices) == 0: return []
    if len(lslices) == 1: return [lslices[0]]
    sllist = [slice_set_default(sl) for sl in lslices]
    if verify:
        if not all([ s.step is None or s.step == 1 for s in sllist]):
            raise ValueError("fillgaps_slices verify failed (step)")
        if any([ s.stop is None for s in sllist]):
            raise ValueError("fillgaps_slices verify failed (stop)")
        if not all([sllist[i].start < sllist[i+1].start for i in range(len(sllist)-1)]):
            raise ValueError("fillgaps_slices verify failed (ordered)")
    slices, startsl = [], sllist[0]
    for leftsl, rightsl in zip(sllist, sllist[1:]):
        gaplen = max(0, rightsl.start - leftsl.stop)
        pctgap = float(gaplen) / (slicelen(leftsl) + slicelen(rightsl))
        if gaplen > gapsize and pctgap > gappct: # gap too big; leave it
            slices.append(slice(startsl.start, leftsl.stop, 1))
            startsl = rightsl
    slices.append(slice(startsl.start, rightsl.stop, 1))
    return slices

def tile_grid( shape, blocksize ):
    """
    tile_grid  Produce an 2D array of 2-tuples of slices.
               The 2-tuple of slices represent rectangles
               in the grid of the given shape ... and can 
               be used to access those tiles.
       shape = 2 tuple representing np.shape() of the grid
       blocksize = 2 tuple = (row blocksize, col blocksize)
    """
    result = []
    for row in range(0, shape[0], blocksize[0]):
        column = [ (slice(row, min(row+blocksize[0], shape[0]), 1), \
                    slice(col, min(col+blocksize[1], shape[1]), 1)) \
                    for col in range(0, shape[1], blocksize[1]) ]
        result.append(column)
    return result
