import numpy as np
import pyopencl as cl

class VBObuilder:
  ctx = None

  def setContext(ctx):
    VBObuilder.ctx = ctx

  def constructVBO(vertices):
    matrix = np.array(vertices, dtype=np.float32)
    return cl.Buffer(VBObuilder.ctx, cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR, hostbuf=matrix)
  
  def constructNBO(normals):
    matrix = np.array(normals, dtype=np.float32)
    return cl.Buffer(VBObuilder.ctx, cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR, hostbuf=matrix)
  
  def constructTBO(texcoords):
    matrix = np.array(texcoords, dtype=np.float32)
    return cl.Buffer(VBObuilder.ctx, cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR, hostbuf=matrix)
  
  def constructIBO(indices):
    matrix = np.array(indices, dtype=np.uint32)
    return cl.Buffer(VBObuilder.ctx, cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR, hostbuf=matrix)