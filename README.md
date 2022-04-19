Fastapi-Cookiecutter


### Test Locally
1. Create '.env' file.
2. Run docker command
```
# Build docker file
docker build -t fastapi-cookiecutter .

# Run test
docker run --rm --enf-file .env fastapi-cookiecutter:latest bash test.sh
```
