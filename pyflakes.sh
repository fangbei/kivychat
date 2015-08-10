#!/bin/bash

#echo
#echo "SKIPPING PYFLAKES TEST"
#echo
#exit

echo "============================================================"
echo "== pyflakes =="
pyflakes . | grep -v migration | grep -v wsgi | grep -v filebrowser | grep -v playground
