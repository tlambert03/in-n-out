# Contributing

## Setup development environment

Fork the repository, then:

```sh
git clone <your-fork>
cd in-n-out
SKIP_CYTHON=1 pip install -e .[test,dev]
```

## Running tests

```sh
pytest
```
