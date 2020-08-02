## Installation guide

1. Install [poetry](https://python-poetry.org/)
2. Install dependencies
```sh
poetry install
```

## Usage
- Usage sample command
```sh
poetry run python main.py -i [INPUT] -o [OUTPUT]
```

- For more detail use command
```sh
python main.py --help
```

## Docker
- Build with docker
```sh
docker-compose build
docker-compose up -d
```
- Usage
1. Copy input file `*.png`, `*.pdf`,.. into project's folder. Eg. `./tests/data/test.png`
2. Command `docker exec -it ocrdemo python3 main.py -i tests/data/test.png -o [OUTPUT]`