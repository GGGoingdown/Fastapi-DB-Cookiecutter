#! /bin/bash


set -e
set -x


rm -rf ./Testing-Project

cookiecutter --no-input -f ./ project_name="Testing Project"

cd ./Testing-Project

poetry install --no-root


bash ./script/start_test.sh
