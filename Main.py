from Quaternion import quaternion

q = quaternion(2, 3, 4, 5)
p = quaternion(4, 2, 1, 3)

q.print()
q.inverse().print()
(q*(q.inverse())).print()
((q.inverse())*q).print()

(q*p).print()
(p*q).print()