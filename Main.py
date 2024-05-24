import numpy as np
from Quaternion import quaternion

p = np.array([2, 0, 0])
q = quaternion.fromAxisAngleDeg(90, 0, 0, 1)

q.print()

print(q.applyToPoint(p))