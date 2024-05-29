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
  def addObject(id=None, model=None, pos=v3d(0,0,0), q=Quaternion.fromEuler(v3d(0,0,0)), s=1):
    if ObjectsHandler.ctx == None:
      raise Exception("no context defined for object handler")
    
    if id == None:
      id = f"Obj{ObjectsHandler.unnamedNum}"
      ObjectsHandler.unnamedNum += 1
    
    # allow for opbjects with no model later
    ObjectsHandler.objects.update({id : Object(ObjectsHandler.ctx, pos, q, s).withModel(model)})

  def getVBOs():
    for key in ObjectsHandler.objects:
      object = ObjectsHandler.objects[key]

      object.buildVBOs()