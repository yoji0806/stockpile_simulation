# Stockpile demand × Evacuee Simulatior

Prototype for KOBE078 in 2022 exhibition booth.

## Build and run

`prod` version is served by `gunicorn` instead of the `flask` dev server.

```sh
# dev
docker build -f Dockerfile.dev -t dash-prototype .
docker run -p 8050:8050 -v "$(pwd)"/app:/app --name xxx_dev dash-prototype

# prod
docker build -f Dockerfile -t docker-dash-example-prod .
docker run -p 8050:8050 -v "$(pwd)"/app:/app --name xxx_prod --rm docker-dash-prod
```

## Access the page

Go to `http://localhost:8050` in browser.

## Switch debug mode in Dockerfile

```dockerfile
ENV DASH_DEBUG_MODE True # False
```

## Development

Install the app requirements for development to get better editor support.

```sh
poetry install
```

Optional: clean initialization of `poetry`:

```sh
poetry init
cat app/requirements.txt | xargs poetry add
```

# CopyRight

Copyright (c) 2022 Yoji 

## Others
- a dash prototype environment  
Copyright (c) 2019 Jucy Technologies, Inc.
