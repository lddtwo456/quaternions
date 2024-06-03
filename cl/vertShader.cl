__kernel void transformVBO(__global float* VBO, __constant float4* mat, __global float* VBO_out, const uint num_verts) {
  int id = get_global_id(0);

  if (id < num_verts) {
    // prepare offset index
    int vboi = id * 8;

    // construct vert as float4 for easy dot with matrix
    float4 vert = (float4)(VBO[vboi], VBO[vboi+1], VBO[vboi+2], 1.0f);

    // create transformed vert
    float4 transformed_vert;
    transformed_vert.x = dot(mat[0], vert);
    transformed_vert.y = dot(mat[1], vert);
    transformed_vert.z = dot(mat[2], vert);
    transformed_vert.w = dot(mat[3], vert);

    // output transformed vertex into VBO
    VBO_out[vboi+0] = transformed_vert.x;
    VBO_out[vboi+1] = transformed_vert.y;
    VBO_out[vboi+2] = transformed_vert.z;

    // copy texcoord and normal data
    VBO_out[vboi+3] = VBO[vboi+3];
    VBO_out[vboi+4] = VBO[vboi+4];
    VBO_out[vboi+5] = VBO[vboi+5];
    VBO_out[vboi+6] = VBO[vboi+6];
    VBO_out[vboi+7] = VBO[vboi+7];
  }
}