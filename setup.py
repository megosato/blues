"""
This setup.py script and other related installation scripts are adapted from
https://github.com/choderalab/yank/blob/master/setup.py
"""
from __future__ import print_function
import os
import sys
import ast
import distutils.extension
from setuptools import setup, Extension, find_packages
import numpy
import glob
import os
from os.path import relpath, join
import subprocess

#from Cython.Build import cythonize
DOCLINES = __doc__.split("\n")

########################
VERSION = "0.2.3"  # Primary base version of the build
DEVBUILD = "1"      # Dev build status, Either None or Integer as string
ISRELEASED = False  # Are we releasing this as a full cut?
__version__ = VERSION
########################

requirements = [
    'python',
    'pytest',
    'setuptools',
    'pyyaml',
    'numpy',
    'openmmtools <=0.14.0',
    'mdtraj <=1.9.1',
    'openmm <=7.1.1',
    'parmed <=3.0.1',
    'netcdf4 <=1.3.1',
]


CLASSIFIERS = """\
Development Status :: 1 - Alpha
Intended Audience :: Science/Research
Intended Audience :: Developers
License :: OSI Approved :: The MIT License (MIT)
Programming Language :: Python
Programming Language :: Python :: 3
Topic :: Scientific/Engineering :: Chemistry
Operating System :: Unix
"""

################################################################################
# Writing version control information to the module
################################################################################

def git_version():
    # Return the git revision as a string
    # copied from numpy setup.py
    def _minimal_ext_cmd(cmd):
        # construct minimal environment
        env = {}
        for k in ['SYSTEMROOT', 'PATH']:
            v = os.environ.get(k)
            if v is not None:
                env[k] = v
        # LANGUAGE is used on win32
        env['LANGUAGE'] = 'PYTHON'
        env['LANG'] = 'PYTHON'
        env['LC_ALL'] = 'PYTHON'
        out = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, env=env).communicate()[0]
        return out

    try:
        out = _minimal_ext_cmd(['git', 'rev-parse', 'HEAD'])
        GIT_REVISION = out.strip().decode('ascii')
    except OSError:
        GIT_REVISION = 'Unknown'

    return GIT_REVISION


def write_version_py(filename='blues/version.py'):
    cnt = """
# This file is automatically generated by setup.py
short_version = '{base_version:s}'
build_number = '{build_number:s}'
version = '{version:s}'
full_version = '{full_version:s}'
git_revision = '{git_revision:s}'
release = {isrelease:s}
"""
    # Adding the git rev number needs to be done inside write_version_py(),
    # otherwise the import of numpy.version messes up the build under Python 3.
    base_version = VERSION
    if DEVBUILD is not None and DEVBUILD != "None":
        local_version = base_version + ".dev" + DEVBUILD
    else:
        local_version = base_version
    full_version = local_version

    if os.path.exists('.git'):
        git_revision = git_version()
    else:
        git_revision = 'Unknown'

    if not ISRELEASED:
        full_version += '-' + git_revision[:7]

    a = open(filename, 'w')
    try:
        a.write(cnt.format(base_version=base_version,   # Base version e.g. X.Y.Z
                           build_number=DEVBUILD,       # Package build number
                           version=local_version,       # Flushed out version, usually just base, but can be X.Y.Z.devN
                           full_version=full_version,   # Full version + git short hash, unless released
                           git_revision=git_revision,   # Matched full github hash
                           isrelease=str(ISRELEASED)))  # Released flag
    finally:
        a.close()
################################################################################
# USEFUL SUBROUTINES
################################################################################
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

def find_package_data(data_root, package_root):
    files = []
    for root, dirnames, filenames in os.walk(data_root):
        for fn in filenames:
            files.append(relpath(join(root, fn), package_root))
    return files


################################################################################
# SETUP
################################################################################
write_version_py()
setup(
    name='blues',
    author = "Samuel C. Gill, Nathan M. Lim, Kalistyn Burley, David L. Mobley, and others",
    author_email='dmobley@uci.edu',
    description = ("NCMC moves in OpenMM to enhance ligand sampling"),
    long_description=read('README.md'),
    version=__version__,
    license='MIT',
    url='https://github.com/MobleyLab/blues',
    platforms = ['Linux-64', 'Mac OSX-64', 'Unix-64'],
    classifiers=CLASSIFIERS.splitlines(),
    package_dir={'blues': 'blues'},
    packages=['blues', "blues.tests", "blues.tests.data"] + ['blues.{}'.format(package) for package in find_packages('blues')],
    package_data={'blues': find_package_data('blues/tests/data', 'blues') + ['notebooks/*.ipynb'] + ['images/*']
                  },
    #install_requires=requirements,
    zip_safe=False,
    include_package_data=True)
