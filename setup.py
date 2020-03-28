
from setuptools import setup, find_packages
setup(name='py_heideltime',
      version='1.0',
      description='module in python using java standalone Heideltime from https://github.com/HeidelTime/heideltime',
      author='Jorge Alexandre Rocha Mendes',
      author_email='mendesjorge49@gmail.com',
      url='https://github.com/JMendes1995/py_heideltime.git',
      packages=find_packages(),
      include_package_data=True,
      py_modules=['py_heideltime'],
      install_requires='emoji',
      entry_points={
            'console_scripts': [
                  'py_heideltime=py_heideltime.cli:dates'
            ]
      },
)

