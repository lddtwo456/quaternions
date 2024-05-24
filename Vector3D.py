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
      
  def __str__(self):
    return f"v3d x:{round(self.x*1000)/1000}, y:{round(self.y*1000)/1000}, z:{round(self.z*1000)/1000}"