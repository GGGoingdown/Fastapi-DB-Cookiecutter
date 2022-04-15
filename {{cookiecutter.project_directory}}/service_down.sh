#! /bin/bash

# Shutdown
docker-compose -f docker-compose-test.yml --env-file ./env/.env.test down -v
