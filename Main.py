import numpy as np
from Quaternion import quaternion
from Vector3D import v3d

p = v3d(2, 2, 2)
q = quaternion.fromEulerDeg(v3d(90, 0, 0))

print(q)

v = v3d(2, 3, 5)

print(q.applyToPoint(p))