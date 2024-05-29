import pyopencl as cl
import numpy as np

class ObjParser:
  def parse(filename):
    vertices = []
    normals = []
    texcoords = []
    indices = []

    with open(filename, 'r') as f:
      for line in f:
        if line.startswith('v '):
          vertices.append(list(map(float, line.strip().split()[1:])))
        elif line.startswith('vn'):
          normals.append(list(map(float, line.strip().split()[1:])))
        elif line.startswith('vt'):
          texcoords.append(list(map(float, line.strip().split()[1:])))
        elif line.startswith('f'):
          face = line.strip().split()[1:]
          for i in range(3):
            indices.append(list(map(int, face[i].split('/'))))
    print(f"{vertices}\n\n{normals}\n\n{texcoords}\n\n{indices}\n\n")
    return vertices, normals, texcoords, indices