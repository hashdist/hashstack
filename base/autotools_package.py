from hashdist import build_stage

def rpath_flag(ctx, path):
   if ctx.parameters['platform'] == 'linux':
       return '-Wl,-rpath=%s' % path
   else:
       return ''

@build_stage()
def configure(ctx, stage_args):
    """
    Generates ./configure line.

    Example::

        - name: configure
          extra: ['--enable-foo', '--with-zlib=${ZLIB_DIR}']
          set_env_flags: true # default

    If set_env_flags is set, CFLAGS and LDFLAGS will be set, as appropriate for the
    platform.
    """
    conf_lines = ['./configure --prefix="${ARTIFACT}"']
    if 'extra' in stage_args:
        conf_lines.append(' '.join('"%s"' % arg for arg in stage_args['extra']))
    for i in range(len(conf_lines) - 1):
        conf_lines[i] = conf_lines[i] + ' \\'
        conf_lines[i + 1] = '  ' + conf_lines[i + 1]

    env_lines = []
    if stage_args.get('set_env_FLAGS', True):
        CFLAGS = []
        LDFLAGS = []
        for dep_var in ctx.dependency_dir_vars:
            CFLAGS.append('-I${%s_DIR}/include' % dep_var)
            LDFLAGS.append('-L${%s_DIR}/lib' % dep_var)
            LDFLAGS.append(rpath_flag(ctx, '${%s_DIR}/lib' % dep_var))
        env_lines.append('export CFLAGS="%s"' % ' '.join(CFLAGS))
        env_lines.append('export LDFLAGS="%s"' % ' '.join(LDFLAGS))

    return ['('] + env_lines + conf_lines + [')']
