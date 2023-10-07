# Get Metadata for a Kaggle Dataset

The `get-kaggle-dataset-meta-data.py` python script fetches the metadata for the [_Learning Path Index_ Kaggle Dataset](https://www.kaggle.com/datasets/neomatrix369/learning-path-index-dataset).

## Pre-requisites

Setup your `.bashrc` or `.zshrc` or Windows environment with the below environment variables:

```bash
export KAGGLE_USERNAME="[your kaggle username]"
export KAGGLE_KEY="[your kaggle API key]"
```

See [How to Obtain a Kaggle API Key](https://christianjmills.com/posts/kaggle-obtain-api-key-tutorial/).

Install dependencies by running:

```bash
pip install requirements.txt
```

## Usage

```bash
cd [into this folder]
python get-kaggle-dataset-meta-data.py
```

This creates the metadata json file in the parent folder by the name `dataset-metadata.json`.

## Docs

- [Kaggle API docs](https://www.kaggle.com/docs/api)
- [Dataset Metadata](https://github.com/Kaggle/kaggle-api/wiki/Dataset-Metadata) 
- [Kaggle Wiki](https://github.com/Kaggle/kaggle-api/wiki)
