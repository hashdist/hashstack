from hashdist import build_stage
from os.path import join as pjoin

def rpath_flag(ctx, path):
   if ctx.parameters['platform'] == 'linux':
       return '-Wl,-rpath=%s' % path
   else:
       return ''

@build_stage()
def configure(ctx, stage_args):
    """
    Generates configure line.

    Example::

        - name: configure
          extra: ['--enable-foo', '--with-zlib=${ZLIB_DIR}']
          set_env_flags: true # default
          env_flags_append: {'LDFLAGS', '-Wl,-rpath=${ARTIFACT}/lib'} # only meaningful if set_env_flags: true
          configure_path: . # default
          global_flags: false # default

    If set_env_flags is set, CPPFLAGS and LDFLAGS will be set, as appropriate for the
    platform.
    """

    configure_path = stage_args.get('configure_path', '.')
    conf_lines = [pjoin(configure_path, 'configure') + ' --prefix="${ARTIFACT}"']

    if 'extra' in stage_args:
        conf_lines.append(' '.join('"%s"' % arg for arg in stage_args['extra']))
    for i in range(len(conf_lines) - 1):
        conf_lines[i] = conf_lines[i] + ' \\'
        conf_lines[i + 1] = '  ' + conf_lines[i + 1]

    env_lines = []
    if stage_args.get('set_env_flags', True):
        env = {'CPPFLAGS': [], 'LDFLAGS': []}
        for dep_var in ctx.dependency_dir_vars:
            env['CPPFLAGS'].append('-I${%s_DIR}/include' % dep_var)
            env['LDFLAGS'].append('-L${%s_DIR}/lib' % dep_var)
            env['LDFLAGS'].append(rpath_flag(ctx, '${%s_DIR}/lib' % dep_var))
        for var, value in stage_args.get('append', {}).items():
            env.get(var, []).append(value)
        for env_var, value in env.items():
            env_lines.append('export %s="%s"' % (env_var, ' '.join(value)))

    r = env_lines + conf_lines
    if not stage_args.get('global_flags', False):
        r = ['('] + r + [')']

    return r
