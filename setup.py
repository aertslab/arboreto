from setuptools import setup, find_packages

setup(
    name='Arboretum',
    long_description=open('README.md').read(),
    version='0.1',
    license='LICENSE.txt',
    author='Thomas Moerman',
    author_email='twitter: @thomasjmoerman',
    packages=find_packages(),
    install_requires=['scikit-learn', 'numpy', 'pandas', 'xgboost', 'dask'],
    platforms=['any'],
    keywords=['gene', 'regulatory', 'network', 'inference', 'regression', 'ensemble', 'scalable']
)