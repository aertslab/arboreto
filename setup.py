from setuptools import setup, find_packages

def read_requirements(fname):
    with open(fname, 'r', encoding='utf-8') as file:
        return [line.rstrip() for line in file]

setup(
    name='arboreto',
    packages=find_packages(),
    description='Scalable gene regulatory network inference using tree-based ensemble regressors',
    long_description=open('README.rst').read(),
    url='https://github.com/aertslab/arboreto',
    version='0.1.6',
    license='BSD 3-Clause License',
    author='Thomas Moerman',
    author_email='thomas.moerman@gmail.com',
    install_requires=read_requirements('requirements.txt'),
    platforms=['any'],
    keywords=['gene', 'regulatory', 'network', 'inference', 'regression', 'ensemble', 'scalable', 'dask']
)

