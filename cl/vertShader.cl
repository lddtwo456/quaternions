__kernel void transformVBOs(__global float* VBOs, __global float* mats, __global float* VBOs_out, __global uint* offsets, const uint offsets_len) {
  uint id = get_global_id(0);

  uint offset = 0;
  uint offset_num = 0;
  while (offset < offsets[offset_num]) {
    offset = offsets[offset_num];
    offset_num++;
  }

  // prepare offset index
  uint vboi = id*8;

  // construct vert as float4 for easy dot with matrix
  float4 vert = (float4)(vload3(vboi, VBOs), 1.0f);

  // create transformed vert
  float4 transformed_vert;
  transformed_vert.x = dot(vload4(offset_num*16, mats), vert);
  transformed_vert.y = dot(vload4(offset_num*16+4, mats), vert);
  transformed_vert.z = dot(vload4(offset_num*16+8, mats), vert);
  transformed_vert.w = dot(vload4(offset_num*16+12, mats), vert);

  // output transformed vertex into VBO
  VBOs_out[vboi+0] = transformed_vert.x;
  VBOs_out[vboi+1] = transformed_vert.y;
  VBOs_out[vboi+2] = transformed_vert.z;

  // copy texcoord and normal data
  VBOs_out[vboi+3] = VBOs[vboi+3];
  VBOs_out[vboi+4] = VBOs[vboi+4];
  VBOs_out[vboi+5] = VBOs[vboi+5];
  VBOs_out[vboi+6] = VBOs[vboi+6];
  VBOs_out[vboi+7] = VBOs[vboi+7];
}