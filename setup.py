#!/usr/bin/env python
import os
import pkgutil
import subprocess
import sys
from setuptools import setup, find_packages, Extension, Command
from setuptools.command.test import test as TestCommand


# allows you to build sphinx docs from the package
# main directory with "python setup.py build_sphinx"

try:
    from sphinx.cmd.build import build_main
    from sphinx.setup_command import BuildDoc

    class BuildSphinx(BuildDoc):
        """Build Sphinx documentation after compiling C source files"""

        description = 'Build Sphinx documentation'

        def initialize_options(self):
            BuildDoc.initialize_options(self)

        def finalize_options(self):
            BuildDoc.finalize_options(self)

        def run(self):
            build_cmd = self.reinitialize_command('build_ext')
            build_cmd.inplace = 1
            self.run_command('build_ext')
            build_main(['-b', 'html', './docs', './docs/_build/html'])

except ImportError:
    class BuildSphinx(Command):
        user_options = []

        def initialize_options(self):
            pass

        def finalize_options(self):
            pass

        def run(self):
            print('!\n! Sphinx is not installed!\n!', file=sys.stderr)
            exit(1)

DOCS_REQUIRE = [
    'nbsphinx',
    'sphinx',
    'sphinx-automodapi',
    'sphinx-rtd-theme',
    'stsci-rtd-theme',
    'extension-helpers'
]
TESTS_REQUIRE = [
    'pytest',
]

setup(
    name='mirage',
    description='Create simulated JWST data',
    long_description=('A tool to create simulated NIRCam, NIRISS,'
                      'and FGS exposures'
                      'using an input dark current exposure and a'
                      'noiseless seed image, which can be produced'
                      'from source catalogs. Data can optionally be'
                      'dispersed as well, to simulate wide field'
                      'slitless data files.'),
    author='STScI (Hilbert, Volk, Chambers, Sahlmann, Filippazzo et al.)',
    author_email='hilbert@stsci.edu',
    url='https://github.com/spacetelescope/mirage',
    keywords=['astronomy'],
    classifiers=[
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering :: Astronomy',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    packages=find_packages(exclude=["examples"]),
    package_data={'mirage': ['tests/test_data/*/*.yaml',
                             'tests/test_data/*/*.list',
                             'tests/test_data/*/*.xml',
                             'tests/test_data/*/*.pointing',
                             'config/*.*']
                  },
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    install_requires=[
        'asdf>=2.11.0',
        'astropy>=5.0.4',
        'astroquery>=0.4.6',
        'bokeh>=2.2.3',
        'batman-package',
        'crds>=11.12.0',
        'grismconf',
        'gwcs>=0.18.1',
        'h5py>=3.6.0',
        'hotsoss==0.1.7',
        'ipython',
        'jinja2==3.1.2',
        'jupyter',
        'jwst',
        'jwst-backgrounds>=1.1.2',
        'lxml>=4.8.0',
        'matplotlib>=3.5.1',
        'nircam_gsim',
        'numpy',
        'photutils>=1.4.0',
        'pysiaf==0.15.0',
        'scipy>=1.8.0',
        'synphot>=1.1.1',
        'webbpsf>=1.0.0',
        'pyyaml>=6.0'
    ],
    include_package_data=True,
    extras_require={
        'docs': DOCS_REQUIRE,
        'test': TESTS_REQUIRE,
    },
    tests_require=TESTS_REQUIRE,
    cmdclass={
        'build_sphinx': BuildSphinx
    },)
