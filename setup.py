import sys
from distutils.core import setup

import runner

setup(
    name='runner',
    version=runner.__version__,
    url='https://github.com/K-Phoen/runner',
    description='Tools to deal with FIT and TCX files',
    author='Kévin Gomez',
    author_email='contact@kevingomez.fr',
    license=open('LICENSE').read(),
    packages=['runner'],
    scripts=['scripts/runner-convert', 'scripts/runner-merge'],
)
