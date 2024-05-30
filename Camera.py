import numpy as np
from Quaternion import Quaternion
from Vector3D import v3d
import pyopencl as cl

class Camera:
  def __init__(self, pos=v3d(0, 0, 0), qat=Quaternion.fromEuler(0,0,0)):
    self.pos = pos
    self.qat = qat

  def getTransformMatrix(self):
    p = self.pos
    q = self.qat

    return np.array([
      [1-2*(q.y**2)-2*(q.z**2), 2*q.x*q.y+2*q.w*q.z, 2*q.x*q.z-2*q.w*q.y, p.x],
      [2*q.x*q.y-2*q.w*q.z, 1-2*(q.x**2)-2*(q.z**2), 2*q.y*q.z+2*q.w*q.x, p.y],
      [2*q.x*q.z+2*q.w*q.y, 2*q.y*q.z-2*q.w*q.x, 1-2*(q.x**2)-2*(q.y**2), p.z],
      [0, 0, 0, 1]
    ], dtype=np.float32)

  def move(self, v):
    self.pos += v