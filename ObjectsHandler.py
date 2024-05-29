import time
import numpy as np
import pyopencl as cl

from Model_Utils.VBObuilder import VBObuilder
from Object import Object
from Vector3D import v3d
from Quaternion import Quaternion

class ObjectsHandler:
  objects = {}

  ctx = None
  queue = None
  prg = None

  def init(ctx, queue):
    ObjectsHandler.ctx = ctx
    ObjectsHandler.queue = queue
    VBObuilder.setContext(ctx)

    kernels = ''.join(open('./cl/getTransformMatrix.cl', 'r', encoding='utf-8').readlines())
    ObjectsHandler.prg = cl.Program(ctx, kernels).build()
  
  unnamedNum = 0
  def addObject(id=None, model=None, pos=v3d(0,0,0), qat=Quaternion.fromEuler(v3d(0,0,0)), scl=v3d(1,1,1)):
    if ObjectsHandler.ctx == None:
      raise Exception("no context defined for object handler")
    
    if id == None:
      id = f"Obj{ObjectsHandler.unnamedNum}"
      ObjectsHandler.unnamedNum += 1
    
    # allow for opbjects with no model later
    ObjectsHandler.objects.update({id : Object(ObjectsHandler.ctx, pos, qat, scl).withModel(model)})

  def getVBOs():
    print("getting VBOs...")
    for key in ObjectsHandler.objects:
      object = ObjectsHandler.objects[key]

      object.buildVBOs()
  
  def getTransforms():
    object_vals = ObjectsHandler.objects.values()
    pos_mat = np.array([[obj.pos.x, obj.pos.y, obj.pos.z, 1] for obj in object_vals], dtype=np.float32)
    qat_mat = np.array([[obj.qat.x, obj.qat.y, obj.qat.z, obj.qat.w] for obj in object_vals], dtype=np.float32)
    scl_mat = np.array([[obj.scl.x, obj.scl.y, obj.scl.z, 1] for obj in object_vals], dtype=np.float32)
    out_mat = np.empty((len(ObjectsHandler.objects), 4, 4), dtype=np.float32)

    pos_buffer = cl.Buffer(ObjectsHandler.ctx, cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR, hostbuf=pos_mat)
    qat_buffer = cl.Buffer(ObjectsHandler.ctx, cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR, hostbuf=qat_mat)
    scl_buffer = cl.Buffer(ObjectsHandler.ctx, cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR, hostbuf=scl_mat)
    out_buffer = cl.Buffer(ObjectsHandler.ctx, cl.mem_flags.WRITE_ONLY, out_mat.nbytes)

    ObjectsHandler.prg.getTransformMatrix(ObjectsHandler.queue, pos_mat.shape, None, 
                                          pos_buffer, qat_buffer, scl_buffer, out_buffer, np.int32(len(ObjectsHandler.objects)))
    
    cl.enqueue_copy(ObjectsHandler.queue, out_mat, out_buffer).wait()
    
    i=0
    for obj in object_vals:
      obj.setTransformMatrix(out_mat[i])
      i+=1