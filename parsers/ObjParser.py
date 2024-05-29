import pyopencl as cl
import numpy as np

class ObjParser:
  def parse(filename):
    vertices = []
    normals = []
    texcoords = []
    indices = []

    with open(filename, 'r') as f:
      for line in f:
        if line.startswith('v '):
          vertices.append(list(map(float, line.strip().split()[1:])))
        elif line.startswith('vn'):
          normals.append(list(map(float, line.strip().split()[1:])))
        elif line.startswith('vt'):
          texcoords.append(list(map(float, line.strip().split()[1:])))
        elif line.startswith('f'):
          face = line.strip().split()[1:]
          for i in range(3):
            indices.append(list(map(int, face[i].split('/'))))

    return vertices, normals, texcoords, indices
  
  def constructVBO(vertices, ctx):
    matrix = np.array(vertices, dtype=np.float32)
    return cl.Buffer(ctx, cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR, hostbuf=matrix)
  
  def constructIBO(indices, ctx):
    matrix = np.array(indices, dtype=np.int32)
    return cl.Buffer(ctx, cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR, hostbuf=matrix)
  
  def constructNBO(normals, ctx):
    matrix = np.array(normals, dtype=np.float32)
    return cl.Buffer(ctx, cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR, hostbuf=matrix)
  
  def constructTBO(texcoords, ctx):
    matrix = np.array(texcoords, dtype=np.float32)
    return cl.Buffer(ctx, cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR, hostbuf=matrix)