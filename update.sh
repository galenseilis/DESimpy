rm -r dist

python -m build

python -m twine upload dist/*

pip install desimpy --upgrade
