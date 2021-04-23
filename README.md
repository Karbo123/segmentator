# A simple lib for 3d segmentation

It implements both pointcloud segmentation (using graph) and mesh segmentation.

Codes are adapted from: https://github.com/ScanNet/ScanNet/tree/master/Segmentator

Build example:
```bash
cd csrc && mkdir build && cd build

cmake .. \
-DCMAKE_PREFIX_PATH=`python -c 'import torch;print(torch.utils.cmake_prefix_path)'` \
-DPYTHON_INCLUDE_DIR=$(python -c "from distutils.sysconfig import get_python_inc; print(get_python_inc())")  \
-DPYTHON_LIBRARY=$(python -c "import distutils.sysconfig as sysconfig; print(sysconfig.get_config_var('LIBDIR'))")

make 
```
