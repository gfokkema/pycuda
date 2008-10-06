import pycuda.gpuarray as gpuarray
import pycuda.driver as cuda
import pycuda.tools

cuda.init()
assert cuda.Device.count() >= 1

device = pycuda.tools.get_default_device()
context = device.make_context()
