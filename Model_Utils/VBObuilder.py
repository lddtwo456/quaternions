import numpy as np
import pyopencl as cl

class VBObuilder:
  ctx = None

  def setContext(ctx):
    VBObuilder.ctx = ctx

  def buildBuffers(vertices, normals, texcoords, indices):
    vert_map = {}
    new_indices = []
    new_vertices = []
    
    for i in range(int(len(indices)/3)):
      # prepare vertex, normal, and texcoord data at indices
      v_i = indices[i*3]-1
      v_data = (vertices[v_i][0], vertices[v_i][1], vertices[v_i][2])
      t_i = indices[i*3+1]-1
      if t_i >= 0: t_data = (texcoords[t_i][0], texcoords[t_i][1])
      else: t_data = (0.0, 0.0)
      n_i = indices[i*3+2]-1
      if n_i >= 0: n_data = (normals[n_i][0], normals[n_i][1], normals[n_i][2])
      else: n_data = (0.0, 0.0, 0.0)

      vertex_buffer_data = (v_data, t_data, n_data)

      if vertex_buffer_data not in  vert_map:
        # add unique vertex as key to vert_map that points to index
        vert_map[vertex_buffer_data] = len(new_vertices)
        # add unique vertex to new vertex data
        new_vertices.append(vertex_buffer_data)

      # add index of vertex to indices
      new_indices.append(vert_map[vertex_buffer_data])

    # make flattened np matrices (vert is structured [v.x, v.y, v.z, t.x, t.y, n.x, n.y, n.z])
    vert_matrix = np.array([item for tupletuple in new_vertices for tuple in tupletuple for item in tuple], dtype=np.float32)
    indx_matrix = np.array(new_indices, dtype=np.uint32)

    return cl.Buffer(VBObuilder.ctx, cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR, hostbuf=vert_matrix), cl.Buffer(VBObuilder.ctx, cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR, hostbuf=indx_matrix), cl.Buffer(VBObuilder.ctx, cl.mem_flags.READ_WRITE | cl.mem_flags.COPY_HOST_PTR, hostbuf=vert_matrix), np.uint32(len(vert_matrix)/8)