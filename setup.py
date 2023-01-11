import setuptools
from pathlib import Path

long_description = Path("README.md").read_text()

setuptools.setup(
    name="py_heideltime",
    version="1.0.1",
    description="Python wrapper for HeidelTime temporal tagger.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Jorge Mendes, Ricardo Campos, and Hugo Sousa',
    author_email='hmosousa@gmail.com',
    url='https://github.com/hmosousa/py_heideltime.git',
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[
        "emoji==2.0.0"
    ],
    entry_points={
        'console_scripts': [
            'py_heideltime=py_heideltime.cli:cli'
        ]
    },
)
