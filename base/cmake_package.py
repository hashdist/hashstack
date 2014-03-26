from hashdist import build_stage

def rpath_flag(ctx, path):
   if ctx.parameters['platform'] == 'linux':
      return '-Wl,-rpath=%s' % path
   else:
      return ''

@build_stage()
def configure(ctx, stage_args):
    """
    Generates cmake line.

    Example::

        - name: configure
          extra: ['-D ENABLE_FOO:BOOL=ON', '-D ZLIB_DIR:PATH=${ZLIB_DIR}']
          set_env_flags: true # default
          build_in_source: false # default
          debug:  false # defaults to global parameter debug

    If set_env_flags is set, CPPFLAGS and LDFLAGS will be set, as appropriate
    for the platform.
    If build_in_source is set, build directory will be the same as source directory.
    """
    conf_lines = ['${CMAKE} -DCMAKE_INSTALL_PREFIX:PATH="${ARTIFACT}"',
                  '-DCMAKE_INSTALL_RPATH:STRING="${ARTIFACT}/lib"',
                  '-DCMAKE_INSTALL_RPATH_USE_LINK_PATH:BOOL=ON']

    #set the debug or release cmake flags
    if stage_args['debug']:
        conf_lines.append('-DCMAKE_BUILD_TYPE:STRING=Debug')
    else:
        conf_lines.append('-DCMAKE_BUILD_TYPE:STRING=Release')

    #cmake needs to be given all the dependency dirs as prefix paths
    #so that we search the hashdist directories before the system directories
    #CMake doesn't use the CPPFLAGS implicitly to find libraries
    prefix_paths = []
    CPPFLAGS = []
    LDFLAGS = []
    for dep_var in ctx.dependency_dir_vars:
        prefix_paths.append('${%s_DIR}'%dep_var)
        CPPFLAGS.append('-I${%s_DIR}/include' % dep_var)
        LDFLAGS.append('-L${%s_DIR}/lib' % dep_var)
        LDFLAGS.append(rpath_flag(ctx, '${%s_DIR}/lib' % dep_var))
    #join all the directories together as a cmake list
    conf_lines.append('-DCMAKE_PREFIX_PATH="%s"' % ';'.join(prefix_paths))

    if 'extra' in stage_args:
        conf_lines.append(' '.join('%s' % arg for arg in stage_args['extra']))

    builddir = '..'
    if stage_args.get('build_in_source', False):
        builddir = '.'
    conf_lines.append(builddir)

    for i in range(len(conf_lines) - 1):
        conf_lines[i] = conf_lines[i] + ' \\'
        conf_lines[i + 1] = '  ' + conf_lines[i + 1]

    env_lines = []
    if stage_args.get('set_env_flags', True):
        env_lines.append('export CPPFLAGS="%s"' % ' '.join(CPPFLAGS))
        env_lines.append('export LDFLAGS="%s"' % ' '.join(LDFLAGS))

    return ['('] + env_lines + conf_lines + [')']
