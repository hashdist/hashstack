from hashdist import build_stage

def rpath_flag(ctx, path):
   if ctx.parameters['platform'] == 'linux':
       return '-Wl,-rpath=%s' % path
   else:
       return ''

@build_stage()
def libflags(ctx, stage_args):
    """
    Sets CPPFLAGS and LDFLAGS, as appropriate for the platform.
    """
    CPPFLAGS = []
    LDFLAGS = []
    for dep_var in ctx.dependency_dir_vars:
        CPPFLAGS.append('-I${%s_DIR}/include' % dep_var)
        LDFLAGS.append('-L${%s_DIR}/lib' % dep_var)
        LDFLAGS.append(rpath_flag(ctx, '${%s_DIR}/lib' % dep_var))

    env_lines = []
    env_lines.append('export CPPFLAGS="%s"' % ' '.join(CPPFLAGS))
    env_lines.append('export LDFLAGS="%s"' % ' '.join(LDFLAGS))

    return env_lines
