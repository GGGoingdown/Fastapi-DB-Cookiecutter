#! /bin/bash

# Link DB
python ./app/pre_start.py

# Create schema
aerich upgrade

# Initial data
python ./app/initial/initial_data.py


# Uvicorn
uvicorn app.main:app --host=0.0.0.0 --port=8000 --reload
