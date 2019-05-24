from setuptools import setup, find_packages
import os

requirementPath = 'requirements.txt'
install_requires = []
if os.path.isfile(requirementPath):
      with open(requirementPath) as f:
            install_requires = f.read().splitlines()

setup(name='heideltime',
      version='1.0',
      description='module in python using java standalone Heideltime from https://github.com/HeidelTime/heideltime',
      author='Jorge Alexandre Rocha Mendes',
      author_email='mendesjorge49@gmail.com',
      url='https://github.com/JMendes1995/py_heideltime.git',
      packages=find_packages(),
      include_package_data=True,
      install_requires=install_requires,
      entry_points={
            'console_scripts': [
                  'heideltime=heideltime.cli:dates'
            ]
      },
      )



