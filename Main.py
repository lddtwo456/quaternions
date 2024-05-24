import numpy as np
from Quaternion import quaternion
from Vector3D import v3d

p = np.array([0, 2, 0])
q = quaternion.fromEulerDeg(90, 0, 0)

q.print()

v = v3d(2, 3, 5)
print(f"{v.x} {v.y} {v.z}")

print(q.applyToPoint(p))