import torch
from .csrc.build.libsegmentator import segment_mesh as segment_mesh_fn, segment_point as segment_point_fn


def segment_mesh(vertices, faces, kThresh=0.01, segMinVerts=20):
    """ segment a mesh (CPU)

    Args:
        vertices (torch.Tensor): vertices of shape==(nv, 3)
        faces (torch.Tensor): faces of shape==(nf, 3)
        kThresh (float): segmentation cluster threshold parameter (larger values lead to larger segments)
        segMinVerts (int): the minimum number of vertices per-segment, enforced by merging small clusters into larger segments
    Returns:
        index (torch.Tensor): the cluster index (starts from 0)
    """
    index = segment_mesh_fn(vertices, faces, kThresh, segMinVerts)
    index = torch.unique(index, return_inverse=True)[1]
    return index


def segment_point(vertices, normals, edges, kThresh=0.01, segMinVerts=20):
    """ segment a point cloud (CPU)

    Args:
        vertices (torch.Tensor): vertices of shape==(nv, 3)
        normals (torch.Tensor): normals of shape==(nf, 3)
        edges (torch.Tensor): edges of shape==(ne, 2)
        kThresh (float): segmentation cluster threshold parameter (larger values lead to larger segments)
        segMinVerts (int): the minimum number of vertices per-segment, enforced by merging small clusters into larger segments
    Returns:
        index (torch.Tensor): the cluster index (starts from 0)
    """
    index = segment_point_fn(vertices, normals, edges, kThresh, segMinVerts)
    index = torch.unique(index, return_inverse=True)[1]
    return index



if __name__ == "__main__":
    import trimesh
    import numpy as np
    from .utils import compute_vn

    mesh = trimesh.load_mesh("/data/lab-lei.jiabao/ScanNet_Source/scene0001_00/scene0001_00_vh_clean_2.ply")

    vertices = torch.from_numpy(mesh.vertices.astype(np.float32))
    faces = torch.from_numpy(mesh.faces.astype(np.int64))
    ind = segment_mesh(vertices, faces) 
    color_table = torch.randint(0, 256, size=(1 + ind.max(), 3))
    np.savetxt("result_pc_mesh.txt", torch.cat([vertices, color_table[ind]], dim=1).numpy())

    normals = torch.from_numpy(compute_vn(mesh).astype(np.float32))
    edges = torch.from_numpy(mesh.edges.astype(np.int64))
    ind = segment_point(vertices, normals, edges) 
    np.savetxt("result_pc_point.txt", torch.cat([vertices, color_table[ind]], dim=1).numpy())

