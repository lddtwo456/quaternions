import numpy as np

from Vector3D import v3d

# custom Quaternion class that's probably very slow but good for learning
class Quaternion:
  def __init__(self, w, x, y, z):
    self.q = np.array([w, x, y, z])

  def fromArray(array):
    return Quaternion(array[0], array[1], array[2], array[3])

  def fromAxisAngle(theta, v):
    # constructor for making Quaternions from axis angle representation
    mag = np.sqrt(v.x**2 + v.y**2 + v.z**2)
    v.x /= mag
    v.y /= mag
    v.z /= mag
    
    return Quaternion(np.cos(theta/2), 
                      v.x*np.sin(theta/2), 
                      v.y*np.sin(theta/2), 
                      v.z*np.sin(theta/2))
  
  def fromAxisAngleDeg(theta, v):
    return Quaternion.fromAxisAngle(np.deg2rad(theta), v3d(np.deg2rad(v.x), np.deg2rad(v.y), np.deg2rad(v.z)))
  
  def fromEuler(x,y,z):
    # constructor for making Quaternions from euler rotations

    # build rotation matrix
    rx = np.array([
      [1, 0, 0],
      [0, np.cos(x), -np.sin(x)],
      [0, np.sin(x), np.cos(x)]
    ])

    ry = np.array([
      [np.cos(y), 0, np.sin(y)],
      [0, 1, 0],
      [-np.sin(y), 0, np.cos(y)]
    ])

    rz = np.array([
      [np.cos(z), -np.sin(z), 0],
      [np.sin(z), np.cos(z), 0],
      [0, 0, 1]
    ])

    r = np.matmul(rz, rx)
    r = np.matmul(r, ry)

    w = np.sqrt(1 + r[0][0] + r[1][1] + r[2][2])/2

    # turn matrix into Quaternion
    return Quaternion(w,
                      (r[2][1] - r[1][2]) / (4*w),
                      (r[0][2] - r[2][0]) / (4*w),
                      (r[1][0] - r[0][1]) / (4*w)
                     ).normalized()
  
  def fromEulerDeg(x,y,z):
    return Quaternion.fromEuler(v3d(np.deg2rad(x), np.deg2rad(y), np.deg2rad(z)))
  
  def fromPoint(p):
    # creates "pure" Quaternion (0, x, y, z)
    return Quaternion(0, p.x, p.y, p.z)
  
  def asPoint(self):
    # returns (x, y, z) if given (w, x, y, z)
    q = self
    return v3d(q.x, q.y, q.z)

  def applyToPoint(self, p):
    # applies rotation Quaternion to vector3D point
    q = Quaternion.fromPoint(p)
    qp = self*q*(self.inverse())

    return qp.asPoint()

  def getQ(self):
    return self.q

  def inverse(self):
    q = self
    divisor = q.w**2 + q.x**2 + q.y**2 + q.z**2
    return Quaternion.fromArray(np.array([q.w, -q.x, -q.y, -q.z])/divisor)
  
  def normalized(self):
    q = self
    m = np.sqrt(q.w**2 + q.x**2 + q.y**2 + q.z**2)
    return Quaternion.fromArray(q.q / m)

  def __mul__(self, p):
    q = self
    return Quaternion(q.w*p.w - q.x*p.x - q.y*p.y - q.z*p.z,
                      q.w*p.x + q.x*p.w + q.y*p.z - q.z*p.y,
                      q.w*p.y - q.x*p.z + q.y*p.w + q.z*p.x,
                      q.w*p.z + q.x*p.y - q.y*p.x + q.z*p.w)
  
  def __getattribute__(self, attr):
    match (attr):
      case 'w':
        return self.q[0]
      case 'x':
        return self.q[1]
      case 'y':
        return self.q[2]
      case 'z':
        return self.q[3]
      case _:
        return super().__getattribute__(attr)
      
  def __str__(self):
    return f"qat w:{round(self.w*1000)/1000}, x:{round(self.x*1000)/1000}, y:{round(self.y*1000)/1000}, z:{round(self.z*1000)/1000}"