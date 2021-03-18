"""Reading and writing Ensemble Forecast Time Series in netCDF files.

See:
https://github.com/csiro-hydroinformatics/camels-aus-py
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
import os
import re

here = os.path.abspath(os.path.dirname(__file__))

verstr = 'unknown'
VERSIONFILE = "camels_aus/_version.py"
with open(VERSIONFILE, "r")as f:
    verstrline = f.read().strip()
    pattern = re.compile(r"__version__ = ['\"](.*)['\"]")
    mo = pattern.search(verstrline)
if mo:
    verstr = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))


# Get the long description from the README file
# with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
#     long_description = f.read()

with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
    long_description_content_type='text/markdown'

REQUIREMENTS = ['pandas',
                'numpy',
                'scipy', # to have netcdf read/write
                'geopandas',
                # 'cftime',
                'xarray']

TEST_REQUIREMENTS = ['pytest',
                    #  'coveralls',
                    #  'pytest-cov',
                    #  'pytest-mpl'
                     ]

CLASSIFIERS = ['Development Status :: 3 - Alpha',
                'Intended Audience :: Science/Research',
                'License :: OSI Approved :: MIT License',
                'Operating System :: OS Independent',
                'Topic :: Scientific/Engineering :: Hydrology',
                'Topic :: Database',
                'Programming Language :: Python',
                'Programming Language :: Python :: 3.8',
                'Programming Language :: Python :: 3.9'
                ]
# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

setup(
    name='camels_aus',
    version=verstr,
    description='Python package to easily access the CAMELS-AUS dataset', 
    long_description=long_description,
    long_description_content_type=long_description_content_type,
    url='https://github.com/csiro-hydroinformatics/camels-aus-py',
    author='Jean-Michel Perraud',
    author_email='per202@csiro.au',
    classifiers=CLASSIFIERS,
    keywords='earth-sciences hydrology forecast',
    packages=['camels_aus'],
    install_requires=REQUIREMENTS,
    # extras_require={
    #     # ':python_version >= "3.6"': [
    #     #     'PyQt5',
    #     # ]
    # # extras_require={  # Optional
    # #     'dev': ['check-manifest'],
    # #     'test': ['coverage'],
    # },

    # If there are data files included in your packages that need to be
    # installed, specify them here.
    #
    # If using Python 2.6 or earlier, then these have to be included in
    # MANIFEST.in as well.
    # package_data={  # Optional
    #     'sample': ['package_data.dat'],
    # },

    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files
    #
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    # data_files=[('my_data', ['data/data_file'])],  # Optional

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # `pip` to create the appropriate form of executable for the target
    # platform.
    #
    # For example, the following would provide a command called `sample` which
    # executes the function `main` from this package when invoked:
    # entry_points={  # Optional
    #     'console_scripts': [
    #         'sample=sample:main',
    #     ],
    # },

    # List additional URLs that are relevant to your project as a dict.
    #
    # This field corresponds to the "Project-URL" metadata fields:
    # https://packaging.python.org/specifications/core-metadata/#project-url-multiple-use
    #
    # Examples listed include a pattern for specifying where the package tracks
    # issues, where the source is hosted, where to say thanks to the package
    # maintainers, and where to support the project financially. The key is
    # what's used to render the link text on PyPI.
    project_urls={  # Optional
        'Bug Reports': 'https://github.com/csiro-hydroinformatics/camels-aus-py/issues',
        # 'Funding': 'https://donate.pypi.org',
        # 'Say Thanks!': 'http://saythanks.io/to/example',
        'Source': 'https://github.com/csiro-hydroinformatics/camels-aus-py',
    },
)
