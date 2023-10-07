# Original code: https://lindevs.com/get-dataset-metadata-from-kaggle-using-api-and-python/

import os
import json
from pprint import pprint

from kaggle.api.kaggle_api_extended import KaggleApi

owner = 'neomatrix369'
datasetName = 'learning-path-index-dataset'

api = KaggleApi()
api.authenticate()

print(f"\nFetching the metadata of {owner}/{datasetName}")
metadata = api.metadata_get(owner, datasetName)

print(f"\nPrinting the metadata of {owner}/{datasetName}")
pprint(metadata)

metadata_filename = "../dataset-metadata.json"
metadata_file = open(metadata_filename, "w")
try:
    metadata_as_str = json.dumps(metadata, indent=2) ### Formats the JSON when saving it
    metadata_file.write(metadata_as_str)
    print(f"\nSaving the metadata to {metadata_filename}")
finally:
    metadata_file.close()
