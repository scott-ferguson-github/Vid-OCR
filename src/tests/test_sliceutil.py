import unittest
# from ..src import sliceutil
import sliceutil as su

def slowslicelen(s, asize=None):
    if asize is None: asize = s.stop
    return len(range(*s.indices(asize)))

class slicelenTest(unittest.TestCase):
    # Simple :5 case
    def test_slicelen_case1(self):
        sl = slice(None, 5)
        self.assertEqual(su.slicelen(sl), slowslicelen(sl))
    #  :5 Case but testing constraining and unconstraining array length
    def test_slicelen_case2(self):
        sl = slice(None, 5)
        self.assertEqual(su.slicelen(sl, asize=4), slowslicelen(sl, asize=4))
        self.assertEqual(su.slicelen(sl, 4), slowslicelen(sl, 4))
    # a:10:4 cases with all different a's to test stop boundary with step
    def test_slicelen_case3(self):
        step = 4
        for start in range(step+1):
            sl = slice(start,10,step)
            self.assertEqual(su.slicelen(sl), slowslicelen(sl))
    # Simple 1:5 case            
    def test_slicelen_case4(self):
        sl = slice(1, None)
        self.assertEqual(su.slicelen(sl, asize=10), slowslicelen(sl, asize=10))
    # Boundary condition
    def test_slicelen_case5(self):
        sl = slice(10, None)
        self.assertEqual(su.slicelen(sl, asize=7), slowslicelen(sl, asize=7))
    # Boundary condition
    def test_slicelen_case5(self):
        sl = slice(10, 3)
        self.assertEqual(su.slicelen(sl, asize=7), slowslicelen(sl, asize=7))
    # Check that ValueError is raised appropriately
    def test_slicelen_raises_error(self):
        with self.assertRaises(ValueError):
            su.slicelen(slice(0, None))

class slice2indicesTest(unittest.TestCase):
    def test_slice2indices_case1(self):
        sl, fn = slice(3,10,2), su.slice2indices
        self.assertEqual(fn(sl), [3,5,7,9])
    def test_slice2indices_case2(self):
        sl, fn = slice(3,10,2), su.slice2indices
        self.assertEqual(fn(sl, asize=7), [3,5])


class indices2slicesTest(unittest.TestCase):
    def test_indices2slices_case1(self):
        fn = su.indices2slices
        self.assertEqual(fn([3,4,6,8,9,10]), [slice(3,5), slice(6,7), slice(8,11)])
    def test_indices2slices_case2(self):
        fn = su.indices2slices
        self.assertEqual(fn([3,4,6,8,9,10,12]), [slice(3,5), slice(6,7), slice(8,11), slice(12,13)])
    def test_indices2slices_case3(self):
        fn = su.indices2slices
        self.assertEqual(fn([]), [])
    def test_indices2slices_case4(self):
        fn = su.indices2slices
        self.assertEqual(fn([3]), [slice(3,4)])


class fillgaps_slicelistTest(unittest.TestCase):
    # empty and short
    def test_fillgaps_case1(self):
        fn = su.fillgaps_slicelist
        self.assertEqual(fn([]), [])
        self.assertEqual(fn([slice(3,10)]), [slice(3,10)])
    # gap too big
    def test_fillgaps_case2(self):
        fn = su.fillgaps_slicelist
        inlist = [slice(5), slice(6,10)]
        self.assertEqual(fn(inlist), [slice(0,5,1), slice(6,10,1)])
    # gap exactly one and filled
    def test_fillgaps_case3(self):
        fn = su.fillgaps_slicelist
        inlist = [slice(5), slice(6,10)]
        self.assertEqual(fn(inlist, gapsize=1), [slice(0,10,1)])
    # Three gaps.  Two filled due to gapsize.  One filled due to gappct.
    # One gap not filled.
    def test_fillgaps_case4(self):
        fn = su.fillgaps_slicelist
        #  len2 gap3 len1 gap1 len10 gap4 len6 gap8 len2
        #     gapsize    gapsize    gappct     None
        inlist = [slice(3,5), slice(8,9), slice(10,20), slice(24,30), slice(38,40)]
        self.assertEqual(fn(inlist, gapsize=3, gappct=0.25), [slice(3,30,1), slice(38,40,1)])


class tile_gridTest(unittest.TestCase):
    # test shape1
    def test_tile_grid_case1(self):
        out = su.tile_grid( (100,100), (10,10) )
        self.assertEqual(len(out), 10)
        for row in out:
            self.assertEqual(len(row), 10)
    # test shape2
    def test_tile_grid_case2(self):
        out = su.tile_grid( (102,113), (10,5) )
        self.assertEqual(len(out), 11)
        for row in out:
            self.assertEqual(len(row), 23)
    # test elements (just the corners)
    def test_tile_grid_case3(self):
        out = su.tile_grid( (102,113), (10,5) )
        self.assertEqual(out[0][0], (slice(0,10,1), slice(0,5,1)))
        self.assertEqual(out[0][22], (slice(0,10,1), slice(110,113,1)))
        self.assertEqual(out[10][0], (slice(100,102,1), slice(0,5,1)))
        self.assertEqual(out[10][22], (slice(100,102,1), slice(110,113,1)))


