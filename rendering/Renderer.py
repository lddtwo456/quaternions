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
      VBO = obj.VBO
      IBO = obj.IBO

      # create empty camera transformed VBO buffer
      camera_transformed_VBO = cl.Buffer(Renderer.ctx, cl.mem_flags.READ_WRITE, obj.vert_count*8)

      Renderer.vertShader.applyTransformMatrixToVBO(Renderer.queue, (obj.vert_count,), None, VBO, obj.matrix, camera_transformed_VBO, np.uint32(obj.vert_count))
