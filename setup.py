from setuptools import setup, find_packages

setup(
    name='arboreto',
    packages=find_packages(),
    description='Scalable gene regulatory network inference using tree-based ensemble regressors',
    long_description=open('README.rst').read(),
    url='https://github.com/tmoerman/arboreto',
    download_url='https://github.com/tmoerman/arboreto/archive/0.1.tar.gz',
    version='0.1.3',
    license='BSD 3-Clause License',
    author='Thomas Moerman',
    author_email='thomas.moerman@gmail.com',
    install_requires=['scikit-learn', 'numpy', 'scipy', 'pandas', 'dask', 'distributed'],
    platforms=['any'],
    keywords=['gene', 'regulatory', 'network', 'inference', 'regression', 'ensemble', 'scalable', 'dask']
)
