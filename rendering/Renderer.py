import time
import numpy as np
from ObjectsHandler import ObjectsHandler
import pyopencl as cl

class Renderer:
  cam = None
  ctx = None
  queue = None

  vertShader = None
  fragShader = None

  def setCam(cam):
    Renderer.cam = cam

  def init(ctx, queue):
    Renderer.ctx = ctx
    Renderer.queue = queue

    vert_kernels = ''.join(open('./cl/vertShader.cl', 'r', encoding='utf-8').readlines())
    Renderer.vertShader = cl.Program(ctx, vert_kernels).build()

  def renderScene(IMGbuf):
    # get transform matrices from local coords to projected points
    ObjectsHandler.getTransforms(Renderer.cam)

    # build combined VBOs only once per frame to avoid unnecessary movement of data
    VBO_mats = np.array([obj.VBO for obj in ObjectsHandler.objects], dtype=np.float32).flatten(order='C')
    IBO_mats = np.array([obj.IBO for obj in ObjectsHandler.objects], dtype=np.uint32).flatten(order='C')

    VBOs = cl.Buffer(Renderer.ctx, cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR, hostbuf=VBO_mats)
    IBOs = cl.Buffer(Renderer.ctx, cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR, hostbuf=IBO_mats)
    cam_transformed_VBOs = cl.Buffer(Renderer.ctx, cl.mem_flags.READ_WRITE, len(VBO_mats))

    offset = 0
    for obj in ObjectsHandler.objects:
      Renderer.vertShader.applyTransformMatrixToVBO(Renderer.queue, (obj.vert_count,), None, VBOs, obj.matrix, cam_transformed_VBOs, np.uint32(obj.vert_count), np.uint32(offset))

      # update offset in combined buffer
      offset += len(obj.VBO)-1