import numpy as np

# custom quaternion class that's probably very slow but good for learning
class quaternion:
  def __init__(self, w, x=0, y=0, z=0):
    if (isinstance(w, np.ndarray)):
      self.q = w
    else:
      self.q = np.array([w,x,y,z])

  def fromAxisAngle(theta, x, y, z):
    # constructor for making quaternions from axis angle representation
    return quaternion(np.cos(theta/2), 
                      x*np.sin(theta/2), 
                      y*np.sin(theta/2), 
                      z*np.sin(theta/2))
  
  def fromEuler(p, y, r):
    # constructor for making quaternions from euler rotations

    # build rotation matrix
    rx = np.array([
      [1, 0, 0],
      [0, np.cos(p), -np.sin(p)],
      [0, np.sin(p), np.cos(p)]
    ])

    ry = np.array({
      [np.cos(y), 0, np.sin(y)],
      [0, 1, 0],
      [-np.sin(y), 0, np.cos(y)]
    })

    rz = np.array([
      [np.cos(r), -np.sin(r), 0],
      [np.sin(r), np.cos(r), 0],
      [0, 0, 1]
    ])

    r = (np.matmul(rx, ry)).matmul(rz)
    w = np.sqrt(1 + r[0][0] + r[1][1] + r[2][2])

    # turn matrix into quaternion
    return quaternion(w,
                      (r[2][1] - r[1][2]) / (4*w),
                      (r[0][2] - r[2][0]) / (4*w),
                      (r[1][0] - r[0][1]) / (4*w)
                     ).normalized()

  def getQ(self):
    return self.q
  
  def print(self):
    print(self.q)

  def inverse(self):
    divisor = self.q[0]**2 + self.q[1]**2 + self.q[2]**2 + self.q[3]**2
    return quaternion(np.array([self.q[0], -self.q[1], -self.q[2], -self.q[3]])/divisor)
  
  def normalized(self):
    q = self.q
    m = np.sqrt(q[0]**2 + q[1]**2 + q[2]**2 + q[3]**2)
    return quaternion(self.q / m)

  def __mul__(self, other):
    q = self.q
    p = other.q

    return quaternion(q[0]*p[0] - q[1]*p[1] - q[2]*p[2] - q[3]*p[3],
                      q[0]*p[1] + q[1]*p[0] + q[2]*p[3] - q[3]*p[2],
                      q[0]*p[2] - q[1]*p[3] + q[2]*p[0] + q[3]*p[1],
                      q[0]*p[3] + q[1]*p[2] - q[2]*p[1] + q[3]*p[0])