import numpy as np

# custom quaternion class that's probably very slow but good for learning
class quaternion:
  def __init__(self, w, x, y, z):
    self.q = np.array([w, x, y, z])

  def fromArray(array):
    return quaternion(array[0], array[1], array[2], array[3])

  def fromAxisAngle(theta, x, y, z):
    # constructor for making quaternions from axis angle representation
    mag = np.sqrt(x**2 + y**2 + z**2)
    x /= mag
    y /= mag
    z /= mag
    
    return quaternion(np.cos(theta/2), 
                      x*np.sin(theta/2), 
                      y*np.sin(theta/2), 
                      z*np.sin(theta/2))
  
  def fromAxisAngleDeg(theta, x, y, z):
    return quaternion.fromAxisAngle(np.deg2rad(theta), x, y, z)
  
  def fromEuler(x, y, z):
    # constructor for making quaternions from euler rotations

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
    print(r)
    w = np.sqrt(1 + r[0][0] + r[1][1] + r[2][2])/2
    print(w)

    # turn matrix into quaternion
    return quaternion(w,
                      (r[2][1] - r[1][2]) / (4*w),
                      (r[0][2] - r[2][0]) / (4*w),
                      (r[1][0] - r[0][1]) / (4*w)
                     ).normalized()
  
  def fromEulerDeg(x, y, z):
    return quaternion.fromEuler(np.deg2rad(x), np.deg2rad(y), np.deg2rad(z))
  
  def fromPoint(point):
    # creates "pure" quaternion (0, x, y, z)
    return quaternion(0, point[0], point[1], point[2])
  
  def asPoint(self):
    # returns (x, y, z) if given (w, x, y, z)
    q = self.q
    return np.array([q[1], q[2], q[3]])

  def applyToPoint(self, point):
    # applies rotation quaternion to vector3D point
    q = quaternion.fromPoint(point)
    qp = self*q*(self.inverse())

    return qp.asPoint()

  def getQ(self):
    return self.q
  
  def print(self):
    print(self.q)

  def inverse(self):
    divisor = self.q[0]**2 + self.q[1]**2 + self.q[2]**2 + self.q[3]**2
    return quaternion.fromArray(np.array([self.q[0], -self.q[1], -self.q[2], -self.q[3]])/divisor)
  
  def normalized(self):
    q = self.q
    m = np.sqrt(q[0]**2 + q[1]**2 + q[2]**2 + q[3]**2)
    return quaternion.fromArray(self.q / m)

  def __mul__(self, other):
    q = self.q
    p = other.q

    return quaternion(q[0]*p[0] - q[1]*p[1] - q[2]*p[2] - q[3]*p[3],
                      q[0]*p[1] + q[1]*p[0] + q[2]*p[3] - q[3]*p[2],
                      q[0]*p[2] - q[1]*p[3] + q[2]*p[0] + q[3]*p[1],
                      q[0]*p[3] + q[1]*p[2] - q[2]*p[1] + q[3]*p[0])