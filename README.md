# Cogreqs

_Cogreqs is an experimental drop-in replacement for [`cog init`](https://github.com/replicate/cog/blob/main/docs/getting-started-own-model.md#initialization) that intelligently populates [cog.yaml](https://github.com/replicate/cog/blob/main/docs/yaml.md)._

## Installation

`pip install cogreqs`

## Usage

Run the following command in an existing Python repository:

```
$ cogreqs --gpu .

Wrote cog.yaml
Wrote predict.py
```

cog.yaml may now contain something like

```yaml
# Configuration for Cog ⚙
# Reference: https://github.com/replicate/cog/blob/main/docs/yaml.md

build:
  # set to true if your model requires a GPU
  gpu: true

  # a list of ubuntu apt packages to install
  system_packages:
    - "ffmpeg"
    - "libsndfile-dev"

  # python version in the form '3.8' or '3.8.12'
  python_version: "3.8"

  # a list of packages in the format <package-name>==<version>
  python_packages:
    - "librosa==0.9.1"
    - "numpy==1.22.2"
    - "scipy==1.8.0"
    - "torch==1.10.2"

  # commands run after the environment is setup
  run:

# predict.py defines how predictions are run on your model
predict: "predict.py:Predictor"
```

**NOTE:** Cogreqs outputs a predict.py that's only compatible with the `future` branch of Cog. Until that branch is merged into main, install Cog from https://github.com/replicate/cog/releases/tag/v0.1.0-alpha

You can also output the generated cog.yaml contents to stdout:

```
$ cogreqs --config-path=- --predict-path=/dev/null .

# Configuration for Cog ⚙
# Reference: https://github.com/replicate/cog/blob/main/docs/yaml.md

build:
[...]
```

## CLI reference

```
usage: cogreqs [-h] [-f] [-g] [--config-path CONFIG_PATH] [--predict-path PREDICT_PATH] folder

Generate cog.yaml and predict.py from an existing repository. This is an experimental alternative to
cog init

positional arguments:
  folder                Project folder

optional arguments:
  -h, --help            show this help message and exit
  -f, --force-overwrite
                        Overwrite existing cog.yaml and predict.py
  -g, --gpu             Use GPU
  --config-path CONFIG_PATH
                        Config file path (default cog.yaml)
  --predict-path PREDICT_PATH
                        Predict file path (default predict.py)
```

## How does it work?

Cogreqs uses [pipreqs](https://github.com/bndr/pipreqs) to extract requirements from Python files in a repository. It then applies a sequence of heuristics on those requirements to populate `python_packages` and `system_packages` in [cog.yaml](https://github.com/replicate/cog/blob/main/docs/yaml.md).

For example, cogreqs knows that `librosa` requires the `ffmpeg` and `libsndfile-dev` system packages so it will add those to `system_packages` if `librosa` is one of the python requirements.

## Work in progress!

This project is very much work in progress. Please submit an issue or pull request if you have ideas for heuristics or other features!
