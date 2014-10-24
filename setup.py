import sys
from distutils.core import setup

import runner

requires = ['argparse'] if sys.version_info < (2, 7) else None

setup(
    name='runner',
    version=runner.__version__,
    url='https://github.com/K-Phoen/runner',
    description='Tools to deal with FIT and TCX files',
    author='Kévin Gomez',
    author_email='contact@kevingomez.fr',
    license=open('LICENSE').read(),
    packages=['runner'],
    scripts=['scripts/runner-convert'],
    install_requires=requires,
)
