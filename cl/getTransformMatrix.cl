typedef struct {
    float4 col[4];
} float4x4;

__kernel void getTransformMatrix(__global float4* position, __global float4* quaternion, __global float4* scale, __global float4x4* outputMatrix, const int numElements) {
  int index = get_global_id(0);

  // get position, quaternion, and scale
  float4 pos = position[index];
  float4 qat = quaternion[index];
  float4 scl = scale[index];
  
  // get simpler position and scale vectors
  float3 posv = (float3)(pos.x, pos.y, pos.z);
  float3 sclv = (float3)(scl.x, scl.y, scl.z);

  // get rotation matrix from quaternion
  float xx = qat.x * qat.x;
  float yy = qat.y * qat.y;
  float zz = qat.z * qat.z;
  float xy = qat.x * qat.y;
  float xz = qat.x * qat.z;
  float yz = qat.y * qat.z;
  float wx = qat.w * qat.x;
  float wy = qat.w * qat.y;
  float wz = qat.w * qat.z;

  float4x4 rotationMatrix = {
    (float4)(1.0f - 2.0f * (yy + zz), 2.0f * (xy - wz), 2.0f * (xz + wy), 0.0f),
    (float4)(2.0f * (xy + wz), 1.0f - 2.0f * (xx + zz), 2.0f * (yz - wx), 0.0f),
    (float4)(2.0f * (xz - wy), 2.0f * (yz + wx), 1.0f - 2.0f * (xx + yy), 0.0f),
    (float4)(0.0f, 0.0f, 0.0f, 1.0f)
  };

  float4x4 transformationMatrix = {
    (float4)(rotationMatrix.col[0].x * sclv.x, rotationMatrix.col[1].x * sclv.y, rotationMatrix.col[2].x * sclv.z, 0.0f),
    (float4)(rotationMatrix.col[0].y * sclv.x, rotationMatrix.col[1].y * sclv.y, rotationMatrix.col[2].y * sclv.z, 0.0f),
    (float4)(rotationMatrix.col[0].z * sclv.x, rotationMatrix.col[1].z * sclv.y, rotationMatrix.col[2].z * sclv.z, 0.0f),
    (float4)(posv.x, posv.y, posv.z, 1.0f)
  };

  outputMatrix[index] = transformationMatrix;
}