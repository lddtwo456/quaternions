import pyopencl as cl
import numpy as np

class ObjParser:
  def parse(filename):
    vertices = []
    normals = []
    texcoords = []
    indices = []
    
    # fix parser
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
          triangle_count = len(face) - 2
          face_indecies = []
          for i in range(len(face)):
            vertex_data = face[i].split('/')
            int_vertex_data = []
            for index in vertex_data:
              if index != '':
                int_vertex_data.append(int(index))
              else:
                int_vertex_data.append(0)
            face_indecies.append(int_vertex_data)

          for i in range(triangle_count):
            indices.append(face_indecies[0])
            indices.append(face_indecies[1+i])
            indices.append(face_indecies[2+i])

    #print(f"{vertices}\n\n{normals}\n\n{texcoords}\n\n{indices}\n\n")
    return vertices, normals, texcoords, indices