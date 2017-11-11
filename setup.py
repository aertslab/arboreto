from setuptools import setup, find_packages

setup(
    name='arboretum',
    long_description=open('README.md').read(),
    version='1.0.0',
    license='LICENSE.txt',
    author='Thomas Moerman',
    author_email='thomas.moerman@esat.kuleuven.be',
    packages=find_packages(),
    install_requires=['scikit-learn', 'numpy', 'scipy', 'pandas', 'dask', 'distributed'],
    platforms=['any'],
    keywords=['gene', 'regulatory', 'network', 'inference', 'regression', 'ensemble', 'scalable']
)