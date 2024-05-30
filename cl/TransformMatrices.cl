typedef struct {
    float4 row[4];
} float4x4;

__kernel void getTransformMatrices(__global float4* position, __global float4* quaternion, __global float4* scale, __global float4x4* outputMatrix, const int numElements) {
  int index = get_global_id(0);
  
  // check this is valid work element
  if (index < numElements) {
    // get position, quaternion, and scale
    float4 pos = position[index];
    float4 qat = quaternion[index];
    float4 scl = scale[index];

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

    float4x4 rmt = {
      (float4)(1.0f - 2.0f * (yy + zz), 2.0f * (xy - wz), 2.0f * (xz + wy), 0.0f),
      (float4)(2.0f * (xy + wz), 1.0f - 2.0f * (xx + zz), 2.0f * (yz - wx), 0.0f),
      (float4)(2.0f * (xz - wy), 2.0f * (yz + wx), 1.0f - 2.0f * (xx + yy), 0.0f),
      (float4)(0.0f, 0.0f, 0.0f, 1.0f)
    };

    float4x4 transformationMatrix = {
      (float4)(rmt.row[0].x * scl.x, rmt.row[1].x * scl.x, rmt.row[2].x * scl.x, pos.x),
      (float4)(rmt.row[0].y * scl.y, rmt.row[1].y * scl.y, rmt.row[2].y * scl.y, pos.y),
      (float4)(rmt.row[0].z * scl.z, rmt.row[1].z * scl.z, rmt.row[2].z * scl.z, pos.z),
      (float4)(0.0f, 0.0f, 0.0f, 1.0f)
    };

    outputMatrix[index] = transformationMatrix;
  }
}

__kernel void applyMatrixToMatrices(__global float4x4* matrix_in, const float4x4 apply_matrix_in, __global float4x4* outputMatrix, const int numElements) {
  int index = get_global_id(0);

  if (index < numElements) {
    float4x4 A = matrix_in[index];
    float4x4 B = apply_matrix_in;

    float c11 = A.row[0].x * B.row[0].x + A.row[0].y * B.row[1].x + A.row[0].z * B.row[2].x;
    float c12 = A.row[0].x * B.row[0].y + A.row[0].y * B.row[1].y + A.row[0].z * B.row[2].y;
    float c13 = A.row[0].x * B.row[0].z + A.row[0].y * B.row[1].z + A.row[0].z * B.row[2].z;
    float c21 = A.row[1].x * B.row[0].x + A.row[1].y * B.row[1].x + A.row[1].z * B.row[2].x;
    float c22 = A.row[1].x * B.row[0].y + A.row[1].y * B.row[1].y + A.row[1].z * B.row[2].y;
    float c23 = A.row[1].x * B.row[0].z + A.row[1].y * B.row[1].z + A.row[1].z * B.row[2].z;
    float c31 = A.row[2].x * B.row[0].x + A.row[2].y * B.row[2].x + A.row[2].z * B.row[2].x;
    float c32 = A.row[2].x * B.row[0].y + A.row[2].y * B.row[2].y + A.row[2].z * B.row[2].y;
    float c33 = A.row[2].x * B.row[0].z + A.row[2].y * B.row[2].z + A.row[2].z * B.row[2].z;

    float4x4 finalMatrix = {
      (float4)(B.row[0].x,  B.row[0].y,  B.row[0].z,  0.0f),
      (float4)(B.row[1].x,  B.row[1].y,  B.row[1].z,  0.0f),
      (float4)(B.row[2].x,  B.row[2].y,  B.row[2].z,  0.0f),
      (float4)(0.0f, 0.0f, 0.0f, 1.0f)
    };

    outputMatrix[index] = finalMatrix;
  }
}