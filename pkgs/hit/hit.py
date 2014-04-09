# Package for letting package builds use tools in `hit`; really just links up
# Hashdist using the called interpreter.

import sys
import os
from textwrap import dedent
import hashdist
from hashdist import build_stage

@build_stage()
def setup_hit(ctx, stage_args):
    package = os.path.realpath(os.path.join(os.path.dirname(hashdist.__file__)))
    interpreter = os.path.realpath(sys.executable)
    return dedent('''
    mkdir "$ARTIFACT/bin"
    cat > "$ARTIFACT/bin/hit" <<END
    #!%(interpreter)s
    import sys
    import os
    sys.path.insert(0, os.path.join(os.path.realpath(os.path.dirname(__file__)), '..', 'pypkg'))
    from hashdist.hdist_logging import Logger
    from hashdist.cli.main import main, help_on_exceptions

    logger = Logger()
    sys.exit(help_on_exceptions(logger, main, sys.argv, os.environ, logger))
    END
    chmod +x "$ARTIFACT/bin/hit"
    mkdir "$ARTIFACT/pypkg"
    ln -s "%(package)s" "$ARTIFACT/pypkg/hashdist"
    ''' % dict(interpreter=interpreter, package=package)).splitlines()
