from hashdist import build_stage

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
    
    conf_lines = ['./configure --prefix="${ARTIFACT}"']

    # this should be a function :)
    if 'coptflags' in stage_args and stage_args['coptflags']:
        conf_lines.append('COPTFLAGS=%s' % stage_args['coptflags'])
    if 'link' in stage_args:
        conf_lines.append('--with-shared-libraries=%d' % 
                          bool(stage_args['link'] == 'shared'))
    if 'debug' in stage_args:
        conf_lines.append('--with-debugging=%d' % stage_args['debug'])

    # Special case, no meaningful BLAS/LAPACK directories when using Accelerate

    if ctx.parameters['platform'] != 'Darwin':
        conf_lines.append('--with-blas-dir=$BLAS_DIR')
        conf_lines.append('--with-lapack-dir=$LAPACK_DIR')

    # Special case, ParMETIS also provides METIS 
    if 'PARMETIS' in ctx.dependency_dir_vars:
        conf_lines.append('--with-metis=1')
        conf_lines.append('--with-metis-dir=$PARMETIS_DIR')
        conf_lines.append('--with-parmetis=1')
        conf_lines.append('--with-parmetis-dir=$PARMETIS_DIR')
        
    for dep_var in ctx.dependency_dir_vars:
        if dep_var in ['BLAS', 'LAPACK', 'PARMETIS']:
            continue
        conf_lines.append('--with-%s=1' % dep_var.lower())
        conf_lines.append('--with-%s-dir=$%s_DIR' % 
                          (dep_var.lower(),
                           dep_var))

    for package in stage_args['download'].split(','):
        package_name = package.strip()
        conf_lines.append('--download-%s=1' % package_name)

    # Multilinify
    for i in range(len(conf_lines) - 1):
        conf_lines[i] = conf_lines[i] + ' \\'
        conf_lines[i + 1] = '  ' + conf_lines[i + 1]

    return conf_lines
