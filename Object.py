from Model_Utils.Parsers.ObjParser import ObjParser
from Model_Utils.VBObuilder import VBObuilder
from Quaternion import Quaternion
import numpy as np

from Vector3D import v3d

class Object:
  def __init__(self, ctx, pos=v3d(0,0,0), q=Quaternion.fromEuler(v3d(0,0,0)), s=1):
    # position, rotation, scale
    

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

    # VBOs will all be permanently stored in vram if they are in the scene for now, might change later
    self.buildVBOs()

    # untranslated AABB for MANY MANY MANY different types of optimizations, maybe later can use to cull non-visible VBOs from vram if needed
    self.min_corner = np.min(self.vertices, axis=0)
    self.max_corner = np.max(self.vertices, axis=0)

    return self
    
  def buildVBOs(self):
    if self.model == None:
      raise Exception("object has no model")
    if self.model.endswith("obj"):
      self.vertices, self.normals, self.texcoords, self.indices = ObjParser.parse(self.model)
    else:
      raise Exception("unsupported model filetype")
    
    if self.vertices != []:
      self.VBO = VBObuilder.constructVBO(self.vertices)
    if self.normals != []:
      self.NBO = VBObuilder.constructVBO(self.normals)
    if self.texcoords != []:
      self.TBO = VBObuilder.constructVBO(self.texcoords)
    if self.indices != []:
      self.IBO = VBObuilder.constructVBO(self.indices)

    self.VBOsBuilt = True

  def delVBOs(self):
    self.VBO.release()
    self.NBO.release()
    self.TBO.release()
    self.IBO.release()

    self.VBO, self.NBO, self.TBO, self.IBO = None
    self.VBOsBuilt = False