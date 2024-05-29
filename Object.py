from Model_Utils.Parsers.ObjParser import ObjParser
from Model_Utils.VBObuilder import VBObuilder
from Quaternion import Quaternion
import numpy as np

from Vector3D import v3d

class Object:
  def __init__(self, ctx, pos=v3d(0,0,0), q=Quaternion.fromEuler(v3d(0,0,0)), s=v3d(1,1,1)):
    # position, rotation, scale
    self.pos = pos
    self.qat = q
    self.scl = s

    self.matrix = None

    # OpenCL context
    self.ctx = ctx

    # model and rendering things
    self.model = None
    self.VBOsBuilt = False
    self.vertices = []
    self.VBO = None
    self.normals = []
    self.NBO = None
    self.texcoords = []
    self.TBO = None
    self.indices = []
    self.IBO = None

  def withModel(self, filename):
    self.model = filename

    return self
  
  def setTransformMatrix(self, matrix):
    # calculated in parallel across all objects by ObjectsHandler.py
    self.matrix = matrix
    
  def buildBuffers(self):
    if self.model == None:
      raise Exception("object has no model")
    if self.model.endswith("obj"):
      self.vertices, self.normals, self.texcoords, self.indices = ObjParser.parse(self.model)
    else:
      raise Exception("unsupported model filetype")
    
    self.VBO = VBObuilder.constructVBO(self.vertices)
    self.NBO = VBObuilder.constructNBO(self.normals)
    self.TBO = VBObuilder.constructTBO(self.texcoords)
    self.IBO = VBObuilder.constructIBO(self.indices)

    # untranslated AABB for MANY MANY MANY different types of optimizations, maybe later can use to cull non-visible VBOs from vram if needed
    self.min_corner = np.min(self.vertices, axis=0)
    self.max_corner = np.max(self.vertices, axis=0)

    self.VBOsBuilt = True

  def delVBOs(self):
    self.VBO.release()
    self.NBO.release()
    self.TBO.release()
    self.IBO.release()

    self.VBO, self.NBO, self.TBO, self.IBO = None
    self.VBOsBuilt = False