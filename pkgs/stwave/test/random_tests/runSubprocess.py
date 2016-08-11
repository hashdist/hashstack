import sys, os

TEST_DIR = os.environ['PWD']
binary_serial_c    = 'hello_serial_c.out'
binary_serial_f    = 'hello_serial_fortran.out'
binary_parallel_c  = 'hello_parallel_c.out'
binary_parallel_f  = 'hello_parallel_fortran.out'

MPIRUN = 'mpirun'
NP     = 2

try:
    os.system(TEST_DIR+'/'+binary_serial_c)
    print 'C version - Serial run ... OK' 
except:
    print 'Error in running serial C binary'

try:
    os.system(TEST_DIR+'/'+binary_serial_f)
    print 'Fortran90 version - Serial run ... OK'
except:
    print 'Error in running serial Fortran90 binary'

try:
    os.system(MPIRUN+' -np '+NP+binary_parallel_f)
    print 'Fortran90 version - Parallel run ... OK'
except:
    print 'Error in running parallel Fortran90 binary'

