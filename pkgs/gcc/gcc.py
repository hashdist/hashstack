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
	Example::

         - name: configure
           extra: ['--enable-foo', '--with-zlib=${ZLIB_DIR}']
           set_env_flags: true # default
           configure_path: . # default
		   languages: c,c++,fortran

	* TODO: parameterise languages option so users can pick what to build.
	* TODO: test on both Linux and OSX
	"""

	format_style = '%s'
	prefix_flag = " --prefix=" + format_style % '${ARTIFACT}'

	configure_path = stage_args.get('configure_path', '.')
	conf_lines = [pjoin(configure_path, 'configure') + prefix_flag]

	if 'extra' in stage_args:
		conf_lines.append(' '.join(format_style % arg for arg in stage_args['extra']))

	# see https://gcc.gnu.org/install/configure.html
	# Some of the following could be parameterised

	# next three are needed for C++ compliance
	conf_lines.append('--enable-__cxa_atexit')
	conf_lines.append('--enable-shared')
	conf_lines.append('--enable-threads=posix')
	# just in case if locale is not complete
	conf_lines.append('--enable-clocale=gnu')
	# do only release tests
	conf_lines.append('--enable-checking=release')
	conf_lines.append('--enable-languages=fortran,c,c++')
	#conf_lines.append('--enable-bootstrap')
	conf_lines.append('--with-local-prefix="${ARTIFACT}"')
	#conf_lines.append('--with-sysroot="${ARTIFACT}"')

	env_lines = []

	if 'GMP' in ctx.dependency_dir_vars:
		conf_lines.append('--with-gmp="${GMP_DIR}"')

	if 'MPC' in ctx.dependency_dir_vars:
		conf_lines.append('--with-mpc="${MPC_DIR}"')

	if 'MPFR' in ctx.dependency_dir_vars:
		conf_lines.append('--with-mpfr="${MPFR_DIR}"')

	if 'CLOOG' in ctx.dependency_dir_vars:
		conf_lines.append('--with-cloog="${CLOOG_DIR}"')

	if 'ISL' in ctx.dependency_dir_vars:
		conf_lines.append('--with-isl="${ISL_DIR}"')

	# GCC has issues with finding the dependencies (LD_LIBRARY_PATH) in the stage2 build
	if ctx.parameters['platform'] == 'linux':
		# Build 64bit binaries only
		conf_lines.append('--disable-multilib')
		conf_lines.append('--libdir="${ARTIFACT}"/lib')
		if stage_args.get('set_env_flags', True):
			CPPFLAGS = []
			LDFLAGS = []
			for dep_var in ctx.dependency_dir_vars:
				CPPFLAGS.append('-I${%s_DIR}/include' % dep_var)
				LDFLAGS.append('-L${%s_DIR}/lib' % dep_var)
				LDFLAGS.append(rpath_flag(ctx, '${%s_DIR}/lib' % dep_var))
			env_lines.append('export CPPFLAGS="%s"' % ' '.join(CPPFLAGS))
			env_lines.append('export LDFLAGS="%s"' % ' '.join(LDFLAGS))
			# Tell configure about LDFLAGS for stage1 and stage2
			conf_lines.append('--with-stage1-ldflags="%s"' % ' '.join(LDFLAGS))
			conf_lines.append('--with-boot-ldflags="%s"' % ' '.join(LDFLAGS))

	for i in range(len(conf_lines) - 1):
		conf_lines[i] = conf_lines[i] + ' \\'
		conf_lines[i + 1] = '  ' + conf_lines[i + 1]

	return env_lines + conf_lines
