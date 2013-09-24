#!/bin/sh

export PYTHONPATH=src
bin/python -c "from payday.server import serve; serve()"
