rm -r dist

python -m build

twine upload dist/*

pip install desimpy --upgrade
