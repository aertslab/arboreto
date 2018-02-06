from setuptools import setup, find_packages

setup(
    name='arboretum',
    packages=find_packages(),
    description='Scalable gene regulatory network inference using tree-based ensemble regressors',
    long_description=open('README.rst').read(),
    url='https://github.com/tmoerman/arboretum',
    version='0.1.4',
    license='BSD 3-Clause License',
    author='Thomas Moerman',
    author_email='thomas.moerman@gmail.com',
    install_requires=['scikit-learn', 'numpy', 'scipy', 'pandas', 'dask', 'distributed'],
    platforms=['any'],
    keywords=['gene', 'regulatory', 'network', 'inference', 'regression', 'ensemble', 'scalable', 'dask']
)
