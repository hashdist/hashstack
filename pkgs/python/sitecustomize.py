# This file is created by HashDist and is executed on each python startup.
# Don't print from here, or else python command line scripts may fail!
# The logic in this file is reused from:
# https://github.com/Homebrew/homebrew/blob/master/Library/Formula/python.rb
# Under a BSD-style license
# https://github.com/Homebrew/homebrew/blob/master/LICENSE.txt

import os
import sys
import site

if sys.version_info[0] != 2:
    # This can only happen if the user has set the PYTHONPATH for 3.x and run Python 2.x or vice versa.
    # Every Python looks at the PYTHONPATH variable and we can't fix it here in sitecustomize.py,
    # because the PYTHONPATH is evaluated after the sitecustomize.py. Many modules (e.g. PyQt4) are
    # built only for a specific version of Python and will fail with cryptic error messages.
    # In the end this means: Don't set the PYTHONPATH permanently if you use different Python versions.
    exit('Your PYTHONPATH points to a site-packages dir for Python 2.x but you are running Python ' +
         str(sys.version_info[0]) + '.x!\n     PYTHONPATH is currently: "' + str(os.environ['PYTHONPATH']) + '"\n' +
         '     You should `unset PYTHONPATH` to fix this.')
else:
    # Remove /System site-packages, and the Cellar site-packages
    sys.path = [ p for p in sys.path
                 if (not p.startswith('/System') and
                     not p.startswith('/usr/local/lib/python') and
                     not (p.startswith(sys.prefix) and p.endswith('site-packages'))) ]

# This is needed for Python to parse *.pth.

if 'Python.framework' not in sys.executable:
    # okay, we have a chance to be in an actual profile, as opposed to a build environment
    distutils_profile_packages = os.path.dirname(os.path.dirname(sys.executable)) + '/lib/python2.7/site-packages'
    site.addsitedir(distutils_profile_packages)
else:
    sys.stderr.write('Using Python Framework binary, which is currently not supported by hashdist...')