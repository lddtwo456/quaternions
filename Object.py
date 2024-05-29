from parsers.ObjParser import ObjParser

class Object:
  def __init__(self, x, y, z):
    self.x = x
    self.y = y
    self.z = z

    self.ctx = None

    self.model = None
    self.VBO = None

  def setContext(self, ctx):
    self.ctx = ctx

  def addModel(self, filename):
    if filename.endswith("obj", "."):
      vertices, normals, texcoords, indices = ObjParser.parse(filename)