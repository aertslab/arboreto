from setuptools import setup, find_packages

setup(
    name='arboretum',
    packages=find_packages(),
    long_description=open('README.md').read(),
    url='https://github.com/tmoerman/arboretum',
    download_url='https://github.com/tmoerman/arboretum/archive/0.1.tar.gz',
    version='0.1',
    license='LICENSE.txt',
    author='Thomas Moerman',
    author_email='thomas.moerman@gmail.com',
    install_requires=['scikit-learn', 'numpy', 'scipy', 'pandas', 'dask', 'distributed', 'lightgbm'],
    platforms=['any'],
    keywords=['gene', 'regulatory', 'network', 'inference', 'regression', 'ensemble', 'scalable']
)
