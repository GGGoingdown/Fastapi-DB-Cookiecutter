#! /bin/bash

mkdir ./env

cp .env.example ./env/.env.dev
cp .env.example ./env/.env.test
cp .env.example ./env/.env.prod


chmod -R +x ./env
