# 概要（Japanese）

![概要(Japanese)](https://github.com/yoji0806/stockpile_simulation/assets/40899163/b5c95211-4664-4824-8245-c78f53822815)




# Stockpile Demand Simulator × Evacuee Simulatior

This contains two simulators.
- stockpile demand simulator.
- evacuee simulator.

<br />


image.1 stockpile demand simulator

<img width="800" alt="stockpile demand simulator" src="https://user-images.githubusercontent.com/40899163/210713434-302f6b98-e16e-45d7-9ad7-735a4e701c0b.jpg">
<br /><br />  


image.2 evacuee simulator

<img width="800" alt="evacuee simulator" src="https://user-images.githubusercontent.com/40899163/210713205-f5b239c1-6d2d-430e-a0fc-6993ab813155.png">
<br /><br />









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

By default, it runs the stockpile demand simulator.  
To run the evacuee simulator, use `app_arc_map.py` with other port.


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
