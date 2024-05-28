import numpy
import pyopencl as cl

TASKS = 64

if __name__ == '__main__':
    # load program from .cl source file
    f = open('./opencl_learn/1-1/hello_world.cl', 'r', encoding='utf-8')
    kernels = ''.join(f.readlines())
    f.close()

    # prepare input matrix
    matrix = numpy.random.randint(low=1, high=101, dtype=numpy.int32, size=TASKS)

    # create context
    ctx = cl.create_some_context()
    # create command queue
    queue = cl.CommandQueue(ctx, properties=cl.command_queue_properties.PROFILING_ENABLE)

    # prepare device memory for OpenCL
    dev_matrix = cl.Buffer(ctx, cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR, hostbuf=matrix)

    # compile kernel code
    prg = cl.Program(ctx, kernels).build()

    # execute compiled kernel code
    evt = prg.hello_world(queue, (TASKS, ), (1, ), dev_matrix)
    # wait for kernel to finish execution
    evt.wait()
    print('done')