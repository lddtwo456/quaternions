__kernel void redify(__global uchar* data) {
  int global_id = get_global_id(0);

  if (global_id < get_global_size(0)) {
    uchar3 pixel = vload3(global_id, data);
    pixel.x += 1;
    vstore3(pixel, global_id, data);
  }
}