# Boarder drone agent system

## Local setup

```shell
cd app
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

or

```shell
cd app
conda env create -f environment.yml
conda activate boarder
python -m pip install -r requirements.txt
```

## Running

To run both `ejabberd` and `app`:

```shell
docker-compose up --build
```

To run only `ejabberd`:

```shell
docker-compose run --service-ports ejabberd
```
