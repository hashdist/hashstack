from hashdist import build_stage
import pprint
@build_stage()
def conda_install(ctx, stage_args):
    """
    Generates conda install line

    Example::

        - name: conda-install
          pkgspec: the spec to use for conda
    """
    conda_path = ctx.parameters["conda_prefix"]
    cmd_line = '%s/bin/conda install -y -q --copy -p "${ARTIFACT}" %s' %(conda_path, stage_args['pkgspec'])
    return [cmd_line] 
