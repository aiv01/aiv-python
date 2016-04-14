import unittest
from aiv.math.matrix4 import Matrix4
from aiv.math.quaternion import Quaternion
from aiv.math.vector3 import Vector3

class TestMatrix4(unittest.TestCase):

    def test_double_translation(self):
        m0 = Matrix4.translate(1, 2, 3)
        m1 = Matrix4.translate(4, 5, 6)
        mm = m0 * m1
        self.assertEqual(mm.m[12], 5)
        self.assertEqual(mm.m[13], 7)
        self.assertEqual(mm.m[14], 9)
        self.assertEqual(mm.m[15], 1)

if __name__ == '__main__':
   unittest.main()
