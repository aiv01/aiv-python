import unittest
from aiv.math.vector3 import Vector3

class TestVector3(unittest.TestCase):

    def test_sum_with_vector3(self):
        v0 = Vector3(17, 30, 22)
        v1 = Vector3(22, 17, 30)
        v_sum = v0 + v1
        self.assertEqual(v_sum, Vector3(39, 47, 52))

    def test_sub_with_vector3(self):
        v0 = Vector3(17, 30, 22)
        v1 = Vector3(5, 5, 5)
        v_sub = v0 - v1
        self.assertEqual(v_sub, Vector3(12, 25, 17))

    def test_sum_with_num(self):
        v0 = Vector3(17, 30, 22)
        v_sum = v0 + 5
        self.assertEqual(v_sum, Vector3(22, 35, 27))

    def test_mul_with_vector3(self):
        v0 = Vector3(17, 30, 22)
        v1 = Vector3(1, 1, 1)
        v_mul = v0 * v1
        self.assertEqual(v_mul, Vector3(17, 30, 22))
        self.assertEqual(v_mul * Vector3(2, 2, 2), Vector3(34, 60, 44))

    def test_mul_with_num(self):
        v0 = Vector3(17, 30, 22)
        v_mul = v0 * 1
        self.assertEqual(v_mul, Vector3(17, 30, 22))
        self.assertEqual(v_mul * Vector3(2, 2, 2), Vector3(34, 60, 44))

    def test_indexing(self):
        v = Vector3(17, 30, 22)
        self.assertEqual(v[0], 17)
        self.assertEqual(v[1], 30)
        self.assertEqual(v[2], 22)

    def test_cross(self):
        v0 = Vector3(1, 0, 0)
        v1 = Vector3(0, 1, 0)
        v_cross = v0.cross(v1)
        self.assertEqual(v_cross, Vector3(0, 0, 1))

    def test_normalized(self):
        v0 = Vector3(1, 0, 0)
        self.assertEqual(v0.normalized, Vector3(1, 0, 0))
        v1 = Vector3(2, 0, 0)
        self.assertEqual(v1.normalized, Vector3(1, 0, 0))

if __name__ == '__main__':
   unittest.main()
