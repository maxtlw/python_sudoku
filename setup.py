from setuptools import find_packages, setup

setup(
    name='python_sudoku',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'numpy',
        'numba',
        'pytest'
    ]
)