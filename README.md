# Boarder drone agent system

## Local setup

```shell
cd client
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

or

```shell
cd client
conda env create -f environment.yml
conda activate boarder
python -m pip install -r requirements.txt
```

## Running

To run both `ejabberd` and `client`:

```shell
docker-compose up --build
```

To run only `ejabberd`:

```shell
docker-compose run --service-ports ejabberd
```
