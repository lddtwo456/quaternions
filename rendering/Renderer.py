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

    for obj in ObjectsHandler.objects:
      Renderer.vertShader.transformVBO(Renderer.queue, (obj.VBO.size/32,), (None,), obj.VBO, obj.matrix, obj.outVBO, np.uint32(obj.vert_count)).wait()