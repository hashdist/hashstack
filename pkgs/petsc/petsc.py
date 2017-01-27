from hashdist import build_stage

def preConfigureCrayXE6(ctx, conf_lines):
    conf_lines += ['LDFLAGS=-dynamic /usr/lib64/libcpuset.so.1 /usr/lib64/libbitmask.so.1',
               '--known-mpi-shared-libraries=1',
               '--with-batch',
               '--known-level1-dcache-size=16384',
               '--known-level1-dcache-linesize=64',
               '--known-level1-dcache-assoc=4',
               '--known-memcmp-ok=1',
               '--known-sizeof-char=1',
               '--known-sizeof-void-p=8',
               '--known-sizeof-short=2',
               '--known-sizeof-int=4',
               '--known-sizeof-long=8',
               '--known-sizeof-long-long=8',
               '--known-sizeof-float=4',
               '--known-sizeof-double=8',
               '--known-sizeof-size_t=8',
               '--known-bits-per-byte=8',
               '--known-sizeof-MPI_Comm=4',
               '--known-sizeof-MPI_Fint=4',
               '--known-mpi-long-double=1',
               '--known-mpi-c-double-complex=1',
               '--known-mpi-int64_t=1',
               '--with-pthread=1']

def preConfigureSGIICEX(ctx, conf_lines):
    conf_lines += ['LDFLAGS=' + ctx.parameters['DYNAMIC_EXE_LINKER_FLAGS'],
               '--known-mpi-shared-libraries=1',
               '--with-pic',
               '--with-batch',
               '--known-sdot-returns-double=0',
               '--known-snrm2-returns-double=0',
               '--known-level1-dcache-size=16384',
               '--known-level1-dcache-linesize=64',
               '--known-level1-dcache-assoc=4',
               '--known-memcmp-ok=1',
               '--known-sizeof-char=1',
               '--known-sizeof-void-p=8',
               '--known-sizeof-short=2',
               '--known-sizeof-int=4',
               '--known-sizeof-long=8',
               '--known-sizeof-long-long=8',
               '--known-sizeof-float=4',
               '--known-sizeof-double=8',
               '--known-sizeof-size_t=8',
               '--known-bits-per-byte=8',
               '--known-sizeof-MPI_Comm=4',
               '--known-sizeof-MPI_Fint=4',
               '--known-mpi-long-double=1',
               '--known-mpi-c-double-complex=1',
               '--known-mpi-int64_t=1',
               '--with-pthread=1',
               '--with-blas-lapack-lib="-L/app/unsupported/COST/lapack/3.5.0/gnu/lib -llapack -L/app/unsupported/COST/gotoblas2/1.13/gnu/lib -lgoto2  -llapacke  -lrefblas -ltmglib -lgfortran"']

@build_stage()
def configure(ctx, stage_args):
    """
    Generates PETSc ./configure line.

    Example::

        - name: configure
          coptflags: -O2
          link: shared
          debug: false

    Note: this is a fairly sophisticated build stage that inspects
    the build artifacts available to decide what to enable in PETSc.
    By default, this package builds PETSc with all required artifacts,
    debugging support enabled, and shared libraries enabled.  The
    following extra keys are relevant:

    * coptflags: Fine-grained control over PETSc's C optimization
    flags.  Left unspecified by default.
    * link: Build shared or static libraries.  Shared by default.
    * debug: Enable/disable debugging.  true by default.
    * download: A list of packages to instruct PETSc to download and
    build.  These will not be readily available outside PETSc.
    """

    # PETSc queries TMPDIR, which is not always a useful place to put
    # temporaries.  Here, we force PETSc to use our ./_tmp directory
    # as its temporary directory.  This configuration change may be of
    # general use for the other build systems.
    conf_lines = ['mkdir ${PWD}/_tmp && TMPDIR=${PWD}/_tmp',
                  './configure --prefix="${ARTIFACT}"']

    if ctx.parameters.get('machine','') == 'CrayXE6':
        preConfigureCrayXE6(ctx, conf_lines)
    elif ctx.parameters.get('machine','') == 'SGIICEX':
        preConfigureSGIICEX(ctx, conf_lines)

    if stage_args['coptflags']:
        conf_lines.append('COPTFLAGS=%s' % stage_args['coptflags'])
    if stage_args['link']:
        conf_lines.append('--with-shared-libraries=%d' %
                          bool(stage_args['link'] == 'shared'))
    # must explicitly set --with-debugging=0 to disable debugging
    conf_lines.append('--with-debugging=%d' % stage_args['debug'])

    # Special case, openssl provides ssl
    if 'OPENSSL' in ctx.dependency_dir_vars:
        conf_lines.append('--with-ssl=1')
        conf_lines.append('--with-ssl-dir=${OPENSSL_DIR}')
    else:
        # Disable ssl when not a dependency
        conf_lines.append('--with-ssl=0')

    # Special case, --with-blas-dir does not work with OpenBLAS
    if 'OPENBLAS' in ctx.dependency_dir_vars or ('BLAS' in ctx.dependency_dir_vars and ctx.parameters.get('openblas') == True):
        if ctx.parameters['platform'] == 'Darwin':
            libopenblas = '${OPENBLAS_DIR}/lib/libopenblas.dylib'
        else:
            libopenblas = '${OPENBLAS_DIR}/lib/libopenblas.so'
        conf_lines.append('--with-blas-lapack-lib=%s' % libopenblas)
    else:
        # Special case, no meaningful BLAS/LAPACK directories when using Accelerate

        if ctx.parameters['platform'] != 'Darwin':
            conf_lines.append('--with-blas-dir=$BLAS_DIR')
            conf_lines.append('--with-lapack-dir=$LAPACK_DIR')

    # Special case, ParMETIS also provides METIS
    if 'PARMETIS' in ctx.dependency_dir_vars:
        conf_lines.append('--with-metis-dir=$PARMETIS_DIR')
        conf_lines.append('--with-parmetis-dir=$PARMETIS_DIR')

    # Special case, SCOTCH also provides PTSCOTCH
    if 'SCOTCH' in ctx.dependency_dir_vars:
        conf_lines.append('--with-scotch-dir=${SCOTCH_DIR}')
        conf_lines.append('--with-ptscotch-dir=${SCOTCH_DIR}')

    # Special case, Trilinos provides ML
    if 'TRILINOS' in ctx.dependency_dir_vars:
        if ctx.parameters['platform'] == 'Darwin':
            libml = '${TRILINOS_DIR}/lib/libml.dylib'
        else:
            libml = '${TRILINOS_DIR}/lib/libml.so'
        conf_lines.append('--with-ml=1')
        conf_lines.append('--with-ml-lib=%s' % libml)
        conf_lines.append('--with-ml-include=${TRILINOS_DIR}/include/trilinos')

    if 'SUITESPARSE' in ctx.dependency_dir_vars:
        conf_lines.append('--with-suitesparse=1')
        conf_lines.append('--with-suitesparse-include=${SUITESPARSE_DIR}/include/suitesparse')
        conf_lines.append('--with-suitesparse-lib=[${SUITESPARSE_DIR}/lib/libumfpack.a,libklu.a,libcholmod.a,libbtf.a,libccolamd.a,libcolamd.a,libcamd.a,libamd.a,libsuitesparseconfig.a]')

    if 'HYPRE' in ctx.dependency_dir_vars:
        if ctx.parameters['platform'] == 'Darwin':
            libHYPRE = '${HYPRE_DIR}/lib/libHYPRE.a'
        else:
            libHYPRE = '${HYPRE_DIR}/lib/libHYPRE.so'
        conf_lines.append('--with-hypre=1')
        conf_lines.append('--with-hypre-include=${HYPRE_DIR}/include')
        conf_lines.append('--with-hypre-lib=%s' % libHYPRE)

    for dep_var in ctx.dependency_dir_vars:
        if dep_var in ['BLAS', 'HYPRE', 'LAPACK', 'OPENBLAS', 'PARMETIS',
                       'SCOTCH', 'TRILINOS', 'SUITESPARSE']:
            continue
        if dep_var == 'MPI':
            conf_lines.append('--with-mpi-compilers')
            conf_lines.append('CC=mpicc')
            conf_lines.append('CXX=mpicxx')
            if ctx.parameters['fortran']:
                conf_lines.append('F77=mpif90')
                conf_lines.append('F90=mpif90')
                conf_lines.append('FC=mpif90')
            else:
                conf_lines.append('--with-fc=0')
            continue
        conf_lines.append('--with-%s-dir=$%s_DIR' %
                          (dep_var.lower(),
                           dep_var))
    for package in stage_args['download']:
        package_name = package.strip()
        conf_lines.append('--download-%s=1' % package_name)

    # Multilinify
    for i in range(len(conf_lines) - 1):
        conf_lines[i] = conf_lines[i] + ' \\'
        conf_lines[i + 1] = '  ' + conf_lines[i + 1]

    return conf_lines
