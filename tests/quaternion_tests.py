import unittest
from aiv.math.quaternion import Quaternion
from aiv.math.vector3 import Vector3

class TestQuaternion(unittest.TestCase):

    def test_vector3_rotation(self):
        v = Vector3(17, 30, 22)
        self.assertEqual(Quaternion.euler(0, 0, 0) * v, Vector3(17, 30, 22))
        self.assertEqual(Quaternion.euler(0, 0, 180) * v, Vector3(17, -30, 22))

if __name__ == '__main__':
   unittest.main()
