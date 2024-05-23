import numpy as np

# custom quaternion class that's probably very slow but good for learning
class quaternion:
  def __init__(self, w, x=0, y=0, z=0):
    if (isinstance(w, np.ndarray)):
      self.q = w
    else:
      self.q = np.array([w,x,y,z])

  def getQ(self):
    return self.q
  
  def print(self):
    print(self.q)

  def inverse(self):
    divisor = self.q[0]**2 + self.q[1]**2 + self.q[2]**2 + self.q[3]**2
    return quaternion(np.array([self.q[0], -self.q[1], -self.q[2], -self.q[3]])/divisor)

  def __mul__(self, other):
    q = self.q
    p = other.q

    return quaternion(q[0]*p[0] - q[1]*p[1] - q[2]*p[2] - q[3]*p[3],
                      q[0]*p[1] + q[1]*p[0] + q[2]*p[3] - q[3]*p[2],
                      q[0]*p[2] - q[1]*p[3] + q[2]*p[0] + q[3]*p[1],
                      q[0]*p[3] + q[1]*p[2] - q[2]*p[1] + q[3]*p[0])