#! /usr/bin/env python
import pycuda.autoinit
import pycuda.driver as drv
import numpy
import numpy.linalg as la
import unittest
import pycuda.gpuarray as gpuarray
import sys
import test_abstract_array

class TestGPUArray(test_abstract_array.TestAbstractArray):                                      
    """tests the gpu array class"""

    def make_test_array(self,array):
        """creates a gpu array"""
        return gpuarray.to_gpu(array)

    def test_random(self):
        from pycuda.curandom import rand as curand
        a = curand((5, 5)).get()

        self.assert_((0 <= a).all())
        self.assert_((a < 1).all())

    def test_nan_arithmetic(self):
        def make_nan_contaminated_vector(size):
            shape = (size,)
            a = numpy.random.randn(*shape).astype(numpy.float32)
            #for i in range(0, shape[0], 3):
                #a[i] = float('nan')
            from random import randrange
            for i in range(size//10):
                a[randrange(0, size)] = float('nan')
            return a

        size = 1 << 20

        a = make_nan_contaminated_vector(size)
        a_gpu = gpuarray.to_gpu(a)
        b = make_nan_contaminated_vector(size)
        b_gpu = gpuarray.to_gpu(b)

        ab = a*b
        ab_gpu = (a_gpu*b_gpu).get()

        for i in range(size):
            assert numpy.isnan(ab[i]) == numpy.isnan(ab_gpu[i])
        
if __name__ == '__main__':
    unittest.main()