# A simple cpp lib for 3d unsupervised segmentation

It provides **point cloud segmentation** (using graph) and **mesh segmentation** by offering a simple pytorch binding.

> Our code is written based on this great work: [Segmentator](https://github.com/ScanNet/ScanNet/tree/master/Segmentator)

Build Example:
```bash
cd csrc && mkdir build && cd build

cmake .. \
-DCMAKE_PREFIX_PATH=`python -c 'import torch;print(torch.utils.cmake_prefix_path)'` \
-DPYTHON_INCLUDE_DIR=$(python -c "from distutils.sysconfig import get_python_inc; print(get_python_inc())")  \
-DPYTHON_LIBRARY=$(python -c "import distutils.sysconfig as sysconfig; print(sysconfig.get_config_var('LIBDIR'))") \
-DCMAKE_INSTALL_PREFIX=`python -c 'from distutils.sysconfig import get_python_lib; print(get_python_lib())'` 

make && make install # after install, please do not delete this folder (as we only create a symbolic link)
```

Some Helpful Notes:
- If you cannot compile and have some issues with cuDNN, try additionally passing `-DCAFFE2_USE_CUDNN=0` to cmake
- Our code is expected to be run with `g++` and has not been tested on `MSVC`
- If you cannot compile the code, please ensure your compilation setup is correct

# Examples

```python
import trimesh
import numpy as np
from segmentator import segment_mesh, segment_point, compute_vn

MESH_PATH = ??? # here is the path to your triangle mesh
mesh = trimesh.load_mesh(MESH_PATH)

# segment on mesh
vertices = torch.from_numpy(mesh.vertices.astype(np.float32))
faces = torch.from_numpy(mesh.faces.astype(np.int64))
ind = segment_mesh(vertices, faces) 
color_table = torch.randint(0, 256, size=(1 + ind.max(), 3))
np.savetxt("result_pc_mesh.txt", torch.cat([vertices, color_table[ind]], dim=1).numpy())

# segment on pointcloud
normals = torch.from_numpy(compute_vn(mesh).astype(np.float32))
edges = torch.from_numpy(mesh.edges.astype(np.int64)) # NOTE the edges can actually be obtained from knn graph or radius graph
ind = segment_point(vertices, normals, edges) 
np.savetxt("result_pc_point.txt", torch.cat([vertices, color_table[ind]], dim=1).numpy())
```
