from hashdist import build_stage

@build_stage()
def configure(ctx, stage_args):
    """
    Generates DOLFIN cmake line.

    Example::

        - name: configure
          build_type: RelWithDebInfo

    Note: this is a fairly sophisticated build stage that inspects
    the build artifacts available to decide what to enable in DOLFIN.
    By default, this package builds DOLFIN with all required artifacts,
    debugging support enabled, and shared libraries enabled. The
    following extra keys are relevant:

    * build_type: Release, Debug, RelWithDebInfo or Developer.
    RelWithDebInfo by default.
    """

    conf_lines = ['${CMAKE} -D CMAKE_INSTALL_PREFIX:PATH="${ARTIFACT}"',
                  '-D CMAKE_INSTALL_RPATH:STRING="${ARTIFACT}/lib"',
                  '-D CMAKE_INSTALL_RPATH_USE_LINK_PATH:BOOL=ON',
                  '-D DOLFIN_ENABLE_DOCS:BOOL=OFF',
                  '-D PKG_CONFIG_EXECUTABLE:FILEPATH="${PKG_CONFIG_EXECUTABLE}"',
                  '-D UFC_DIR:PATH="${UFC_DIR}"',
                  '-D EIGEN3_INCLUDE_DIR:PATH="${EIGEN_DIR}/include/eigen3"',
                  '-D BOOST_ROOT:PATH="${BOOST_DIR}"',
                  '-D Boost_USE_MULTITHREADED:BOOL=${BOOST_USE_MULTITHREADED}']

    build_type = stage_args.get('build_type', 'RelWithDebInfo')
    conf_lines.append('-D CMAKE_BUILD_TYPE:STRING="%s"' % build_type)

    if 'CGAL' in ctx.dependency_dir_vars:
        conf_lines.append('-D CGAL_DISABLE_ROUNDING_MATH_CHECK:BOOL=ON')

    if 'SWIG' in ctx.dependency_dir_vars:
        conf_lines.append('-D SWIG_EXECUTABLE:FILEPATH="${SWIG_EXECUTABLE}"')

    if 'PYTHON' in ctx.dependency_dir_vars:
        conf_lines.append('-D PYTHON_EXECUTABLE:FILEPATH="${PYTHON}"')

    # Some special variables are needed to find correct HDF5
    if 'HDF5' in ctx.dependency_dir_vars:
        conf_lines.append('-D HDF5_INCLUDE_DIRS="${HDF5_DIR}/include"')
        conf_lines.append('-D HDF5_ROOT:PATH="${HDF5_DIR}"')
        conf_lines.append('-D HDF5_C_COMPILER_EXECUTABLE="${HDF5_DIR}/bin/h5pcc"')

    # SuiteSparse provides UMFPACK and CHOLMOD
    if 'SUITESPARSE' in ctx.dependency_dir_vars:
        conf_lines.append('-D DOLFIN_ENABLE_UMFPACK:BOOL=ON')
        conf_lines.append('-D DOLFIN_ENABLE_CHOLMOD:BOOL=ON')
        conf_lines.append('-D UMFPACK_DIR:PATH="${SUITESPARSE_DIR}"')
        conf_lines.append('-D CHOLMOD_DIR:PATH="${SUITESPARSE_DIR}"')
    else:
        conf_lines.append('-D DOLFIN_ENABLE_UMFPACK:BOOL=OFF')
        conf_lines.append('-D DOLFIN_ENABLE_CHOLMOD:BOOL=OFF')

    if 'OPENBLAS' in ctx.dependency_dir_vars:
        if ctx.parameters['platform'] == 'Darwin':
            libopenblas = '${OPENBLAS_DIR}/lib/libopenblas.dylib'
        else:
            libopenblas = '${OPENBLAS_DIR}/lib/libopenblas.so'
        conf_lines.append('-D LAPACK_LIBRARIES:FILEPATH="%s"' % libopenblas)
        conf_lines.append('-D BLAS_LIBRARIES:FILEPATH="%s"' % libopenblas)

    if 'ZLIB' in ctx.dependency_dir_vars:
        conf_lines.append('-D ZLIB_ROOT="${ZLIB_DIR}"')

    optional_deps = ['CGAL', 'HDF5', 'PETSC', 'PETSC4PY', 'SLEPC',
                     'TAO', 'TRILINOS', 'PASTIX', 'SCOTCH', 'PARMETIS',
                     'CGAL', 'ZLIB', 'PYTHON','SPHINX', 'VTK', 'QT']

    for dep in optional_deps:
        if dep in ctx.dependency_dir_vars:
            conf_lines.append('-D DOLFIN_ENABLE_%s:BOOL=ON' % dep)
            conf_lines.append('-D %s_DIR:PATH="${%s_DIR}"' % (dep, dep))
        else:
            conf_lines.append('-D DOLFIN_ENABLE_%s:BOOL=OFF' % dep)

    builddir = '..'
    if stage_args.get('build_in_source', False):
        builddir = '.'
    conf_lines.append(builddir)

    for i in range(len(conf_lines) - 1):
        conf_lines[i] = conf_lines[i] + ' \\'
        conf_lines[i + 1] = '  ' + conf_lines[i + 1]
        
    return conf_lines
