import setuptools

setuptools.setup(
    name="py_heideltime",
    version="2.0.0",
    description="Python wrapper for HeidelTime temporal tagger.",
    author='Jorge Mendes, Ricardo Campos, and Hugo Sousa',
    author_email='mendesjorge49@gmail.com',
    url='https://github.com/JMendes1995/py_heideltime.git',
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[
        "emoji==2.0.0"
    ],
    entry_points={
        'console_scripts': [
            'py_heideltime=py_heideltime.cli:dates'
        ]
    },
)
