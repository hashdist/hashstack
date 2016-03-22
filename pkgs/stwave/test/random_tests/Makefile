# Builds C/Fortran90 binaries in serial and parallel

# Compilers
CC 	= clang
CXX	= clang++
FC 	= gfortran
F90	= gfortran
F77	= gfortran
PFC	= mpif90

# User-Defined Vars
RM	= rm -f
all: hello_serial_c hello_serial_fortran hello_parallel_fortran

hello_serial_c:
	$(CC) -c hello_serial_c.c
	$(CC) -o hello_serial_c.out hello_serial_c.o

hello_serial_fortran:
	$(F90) -c hello_serial_fortran.f90
	$(F90) -o hello_serial_fortran.out hello_serial_fortran.o

hello_parallel_fortran:
	$(PFC) hello_parallel_fortran.f90 -o hello_parallel_fortran.out

clean:
	$(RM) *.o *.out