#!/bin/sh
set -e
cd $DIR 
if [ ! -f "$VENV_PATH/pyvenv.cfg" ]; then \
        python -m venv $VENV_PATH ; \
    fi

source bin/activate

if [ -f "$PROJECT_PATH/requirements.txt" ]; then \
    cd $PROJECT_PATH  && pip install -r requirements.txt; fi

sleep infinity
exec "$@"