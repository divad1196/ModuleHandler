#!/bin/bash
python3 setup.py install --user

cd tests
python3 tests.py
cd ..