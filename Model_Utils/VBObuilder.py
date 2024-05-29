import numpy as np
import pyopencl as cl

class VBObuilder:
  ctx = None

  def setContext(ctx):
    VBObuilder.ctx = ctx

  def buildBuffers(vertices, normals, texcoords, indices):
    for i in range(len(indices/3)):
      print(indices[i*3])