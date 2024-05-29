import numpy as np
import pyopencl as cl

class VBObuilder:
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