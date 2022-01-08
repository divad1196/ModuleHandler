#!/bin/bash
python3 setup.py sdist bdist_wheel
pip3 install dist/*.whl --force-reinstall

cd tests
python3 tests.py
cd ..