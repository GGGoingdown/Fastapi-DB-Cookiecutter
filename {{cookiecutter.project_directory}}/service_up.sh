#! /bin/bash


# Build
docker-compose -f docker-compose-test.yml --env-file ./env/.env.test build --build-arg ENVIRONMENT=test
# Start
docker-compose -f docker-compose-test.yml --env-file ./env/.env.test up -d
