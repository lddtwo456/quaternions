import numpy as np

class v3d:
  def __init__(self, x, y, z):
    self.v = np.array([x, y, z])
  
  def fromArray(v):
    return v3d(v[0], v[1], v[2])
  
  def __getattribute__(self, attr):
    match (attr):
      case 'x':
        return self.v[0]
      case 'y':
        return self.v[1]
      case 'z':
        return self.v[2]
      case _:
        return super().__getattribute__(attr)