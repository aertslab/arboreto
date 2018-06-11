pip uninstall -y arboreto
rm -rf dist/*
python setup.py sdist
python setup.py bdist_wheel
pip install dist/*