import numpy
from aiv.math.vector3 import Vector3
from aiv.math.vector2 import Vector2

class ObjLoader(object):

    def __init__(self, filename):

        tmp_vertices = []
        tmp_normals = []
        tmp_uvs = []

        self._vertices = []
        self._normals = []
        self._uvs = []

        with open(filename) as f:
            while True:
               line = f.readline()
               if line == '':
                   break

               if line.startswith('v '):
                   items = line.split(' ')
                   v0 = float(items[1])
                   v1 = float(items[2])
                   v2 = float(items[3])
                   tmp_vertices.append(Vector3(v0, v1, v2))

               if line.startswith('vt '):
                   items = line.split(' ')
                   uv0 = float(items[1])
                   uv1 = float(items[2])
                   tmp_uvs.append(Vector2(uv0, uv1))

               if line.startswith('vn '):
                   items = line.split(' ')
                   n0 = float(items[1])
                   n1 = float(items[2])
                   n2 = float(items[3])
                   tmp_normals.append(Vector3(n0, n1, n2))

               if line.startswith('f '):
                   items = line.split(' ')
                   f0 = items[1]
                   f1 = items[2]
                   f2 = items[3]

                   f0_items = f0.split('/')
                   idx0 = int(f0_items[0])-1
                   idx1 = int(f0_items[1])-1
                   idx2 = int(f0_items[2])-1
                   self._vertices += tmp_vertices[idx0].tuple
                   self._uvs += tmp_uvs[idx1].tuple
                   self._normals += tmp_normals[idx2].tuple

                   f1_items = f1.split('/')
                   idx0 = int(f1_items[0])-1
                   idx1 = int(f1_items[1])-1
                   idx2 = int(f1_items[2])-1
                   self._vertices += tmp_vertices[idx0].tuple
                   self._uvs += tmp_uvs[idx1].tuple
                   self._normals += tmp_normals[idx2].tuple

                   f2_items = f2.split('/')
                   idx0 = int(f2_items[0])-1
                   idx1 = int(f2_items[1])-1
                   idx2 = int(f2_items[2])-1
                   self._vertices += tmp_vertices[idx0].tuple
                   self._uvs += tmp_uvs[idx1].tuple
                   self._normals += tmp_normals[idx2].tuple


        self.vertices = numpy.array(self._vertices, dtype=numpy.float32)
        self.normals = numpy.array(self._normals, dtype=numpy.float32)
        self.uvs = numpy.array(self._uvs, dtype=numpy.float32)
