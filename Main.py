import numpy as np
from Quaternion import quaternion

p = np.array([2, 0, 0])
q = quaternion.fromEulerDeg(0, 90, 0)

q.print()

print(q.applyToPoint(p))