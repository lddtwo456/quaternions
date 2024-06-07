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

    VBOs_list = []
    Mats_list = []
    Offs_list = []
    offset = 0
    for obj in ObjectsHandler.objects:
      Offs_list.append(offset)
      VBOs_list.append(obj.VBO)
      Mats_list.append(obj.matrix)
      offset += obj.vert_count

    VBOs_mat = np.array(VBOs_list, dtype=np.float32).flatten('C')
    Mats_mat = np.array(Mats_list, dtype=np.float32).flatten('C')
    Offs_mat = np.array(Offs_list, dtype=np.uint32)

    VBOs = cl.Buffer(Renderer.ctx, cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR, hostbuf=VBOs_mat)
    cam_transformed_VBOs = cl.Buffer(Renderer.ctx, cl.mem_flags.READ_WRITE, len(VBOs_mat))
    Mats = cl.Buffer(Renderer.ctx, cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR, hostbuf=Mats_mat)
    Offs = cl.Buffer(Renderer.ctx, cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR, hostbuf=Offs_mat)

    Renderer.vertShader.applyTransformMatrixToVBO(Renderer.queue, (np.uint32(VBOs_mat.size/32),), None, VBOs, Mats, cam_transformed_VBOs, Offs)