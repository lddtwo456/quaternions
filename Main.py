import numpy as np
from Quaternion import quaternion

p = np.array([0, 2, 0])
q = quaternion.fromEulerDeg(90, 0, 0)

q.print()

print(q.applyToPoint(p))