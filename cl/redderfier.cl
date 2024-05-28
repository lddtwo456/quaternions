__kernel void redify(__read_only image2d_t imgIN, __write_only image2d_t imgOUT) {
  const int2 pos = (int2)(get_global_id(0), get_global_id(1));
  const sampler_t sampler = CLK_NORMALIZED_COORDS_FALSE | CLK_ADDRESS_CLAMP_TO_EDGE | CLK_FILTER_NEAREST;

  uint4 px = read_imageui(imgIN, sampler, pos);
  px.x += 1;

  write_imageui(imgOUT, pos, px);
}