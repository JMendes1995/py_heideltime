from codecs import open
from os.path import join, abspath, dirname
from setuptools import setup, find_packages
import os

requirementPath = 'requirements.txt'
install_requires = []

if os.path.isfile(requirementPath):
      with open(requirementPath) as f:
            install_requires = f.read().splitlines()

here = abspath(dirname(__file__))

# Get the long description from the README file
with open(join(here, 'README.rst'), encoding='utf-8') as buff:
      long_description = buff.read()

setup(
      name="py_heideltime",
      version="2.0",
      description="python wrapper for Heideltime temporal tagger",
      author='Jorge Alexandre Rocha Mendes',
      author_email='mendesjorge49@gmail.com',
      url='https://github.com/JMendes1995/py_heideltime.git',
      packages=find_packages(),
      include_package_data=True,
      install_requires=install_requires,
      entry_points={
            'console_scripts': [
                  'py_heideltime=py_heideltime.cli:dates'
            ]
      },
)

