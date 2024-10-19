# lpiGPT - Learning Path Index GPT

Ever thought you could ask/query a GPT about a course or smaller module of a course and have it find such bits of learning material across multiple sources of courses.

A standalone GPT app based on [Ollama](https://github.com/jmorganca/ollama) and the [Learning Path Index Dataset](https://www.kaggle.com/datasets/neomatrix369/learning-path-index-dataset).

It's simple and runs on the local machine with smaller sized and free LLMs.

> Note: credits to this program goes to the original authors of [langchain-python-rag-privategpt](https://github.com/jmorganca/ollama/tree/main/examples/langchain-python-rag-privategpt) from Ivan Martinez who contributed to an example on [jmorganca/ollama](https://github.com/jmorganca/ollama).


## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Setup](#setup)
   - [Downloading Learning Path Index datasets](#downloading-learning-path-index-datasets)
   - [Ingesting files](#ingesting-files)
     - [via native shell CLI](#via-native-shell-cli)
- [Usage](#usage)
  - [Ask questions](#ask-questions)
    - [via native shell CLI](#via-native-shell-cli-1)
    - [via Docker container](#via-docker-container)
  - [Try a different model](#try-a-different-model)
  - [Adding more files](#adding-more-files)
- [Models](#models)
  - [Embeddings models](#embeddings-models)
  - [Chat models](#chat-models)
- [Known issues](#known-issues)
- [Contributing](#contributing)
- [License](#license)

## Requirements

List out the key requirements needed to run the project, such as:

- System requirements:
  - Quadcore Intel CPU 2.3Ghz or higher, 16-32GB RAM, 100 GB Free diskspace
  - Preferrable Linux or macOS
- Python 3.9
  - [pyenv](https://github.com/pyenv/pyenv)
  - or venv
  - or [pipenv](https://pipenv.pypa.io/en/latest/)
- Docker (optional)
- Ollama ([Download & Install(https://ollama.com/download))
- Windows:
  -  Microsoft Visual C++ 14.0 or greater is required (needed when installing ```hnswlib``` )

## Installation

Install [Ollama](https://github.com/jmorganca/ollama) using the below command on the host/local machine:

```bash
curl https://ollama.ai/install.sh | sh
```

Pull the model you'd like to use:

```shell
ollama pull llama2-uncensored
```

Set up a virtual environment (or use the [Docker route](#via-docker-container)):

```shell
python3 -m venv .venv
source .venv/bin/activate
```

Please note there are other options to use as well i.e. Conda, venv, virtualenv, poetry, etc. to isolate your development environments.

For Windows, download Microsoft Visual C++ 14.0 or greater ([Link](https://visualstudio.microsoft.com/visual-cpp-build-tools/)). During installation, ensure that "Desktop development with C++" is selected.

Install the Python dependencies:

```shell
pip install -r requirements.txt
```

If you haven't installed Ollama yet, refer to the [Ollama repository](https://github.com/ollama/ollama) for installation instructions.

Pull the model you'd like to use:

```shell
ollama pull llama2-uncensored
```

and start the Ollama server

```shell
ollama serve
```


## Setup

### Downloading Learning Path Index datasets

```bash
mkdir -p source_documents

curl https://raw.githubusercontent.com/neomatrix369/learning-path-index/main/data/Courses_and_Learning_Material.csv -o "source_documents/Courses_and_Learning_Material.csv"

curl https://raw.githubusercontent.com/neomatrix369/learning-path-index/main/data/Learning_Pathway_Index.csv -o "source_documents/Learning_Pathway_Index.csv"
```

Or you can manually download them from the [Kaggle Dataset: Learning Path Index Dataset](https://www.kaggle.com/datasets/neomatrix369/learning-path-index-dataset).

### Ingesting files

#### via native shell CLI

```shell
python3 ingest.py
```

Output should look like this:

```shell
root@sai-XPS-15-9560:/home# python3 ingest.py
Downloading (…)e9125/.gitattributes: 100%|███████████████████████████████████████████████████████████████████| 1.18k/1.18k [00:00<00:00, 2.07MB/s]
Downloading (…)_Pooling/config.json: 100%|████████████████████████████████████████████████████████████████████████| 190/190 [00:00<00:00, 378kB/s]
Downloading (…)7e55de9125/README.md: 100%|███████████████████████████████████████████████████████████████████| 10.6k/10.6k [00:00<00:00, 16.2MB/s]
Downloading (…)55de9125/config.json: 100%|███████████████████████████████████████████████████████████████████████| 612/612 [00:00<00:00, 1.53MB/s]
Downloading (…)ce_transformers.json: 100%|████████████████████████████████████████████████████████████████████████| 116/116 [00:00<00:00, 252kB/s]
Downloading (…)125/data_config.json: 100%|███████████████████████████████████████████████████████████████████| 39.3k/39.3k [00:00<00:00, 29.4MB/s]
Downloading pytorch_model.bin: 100%|█████████████████████████████████████████████████████████████████████████| 90.9M/90.9M [00:09<00:00, 9.11MB/s]
Downloading (…)nce_bert_config.json: 100%|█████████████████████████████████████████████████████████████████████| 53.0/53.0 [00:00<00:00, 97.4kB/s]
Downloading (…)cial_tokens_map.json: 100%|████████████████████████████████████████████████████████████████████████| 112/112 [00:00<00:00, 698kB/s]
Downloading (…)e9125/tokenizer.json: 100%|█████████████████████████████████████████████████████████████████████| 466k/466k [00:00<00:00, 5.22MB/s]
Downloading (…)okenizer_config.json: 100%|████████████████████████████████████████████████████████████████████████| 350/350 [00:00<00:00, 627kB/s]
Downloading (…)9125/train_script.py: 100%|███████████████████████████████████████████████████████████████████| 13.2k/13.2k [00:00<00:00, 21.1MB/s]
Downloading (…)7e55de9125/vocab.txt: 100%|█████████████████████████████████████████████████████████████████████| 232k/232k [00:00<00:00, 10.7MB/s]
Downloading (…)5de9125/modules.json: 100%|████████████████████████████████████████████████████████████████████████| 349/349 [00:00<00:00, 721kB/s]
Creating new vectorstore
Loading documents from source_documents
Loading new documents: 100%|██████████████████████| 2/2 [00:00<00:00, 40.44it/s]
Loaded 1414 new documents from source_documents
Split into 2214 chunks of text (max. 500 tokens each)
Creating embeddings. May take some minutes...
Ingestion complete! You can now run lpiGPT.py to query your documents
```

```bash
usage: ingest.py [-h] [--embeddings-model-name EMBEDDINGS_MODEL_NAME] [--source-documents SOURCE_DOCUMENTS] [--persist-directory PERSIST_DIRECTORY]
                 [--target-source-chunks TARGET_SOURCE_CHUNKS] [--chunk-overlap CHUNK_OVERLAP]

ingest: ingest: process one or more documents (text) in order to create embeddings (using the Embeddings models) from them, and make them ready to be used with LLMs when a question is asked to the InstructGPT or Chat Model.

optional arguments:
  -h, --help            show this help message and exit
  --embeddings-model-name EMBEDDINGS_MODEL_NAME, -EM EMBEDDINGS_MODEL_NAME
                        Use this flag to set the Embeddings model name, see https://www.sbert.net/docs/pretrained_models.html for examples of names. Use the same model
                        when running the lpiGPT.py app.
  --source-documents SOURCE_DOCUMENTS, -S SOURCE_DOCUMENTS
                        Use this flag to specify the name of the folder where all the (source/input) documents are stored for ingestion purposes, on the local machine. The
                        documents contained in them are of the type `.csv`.
  --persist-directory PERSIST_DIRECTORY, -P PERSIST_DIRECTORY
                        Use this flag to specify the name of the vector database, this will be a folder on the local machine.
  --target-source-chunks TARGET_SOURCE_CHUNKS, -C TARGET_SOURCE_CHUNKS
                        Use this flag to specify the name chunk size to use to chunk source data.
  --chunk-overlap CHUNK_OVERLAP, -O CHUNK_OVERLAP
                        Use this flag to specify the name chunk overlap value to use to chunk source data.
```

#### Known issues

- When trying to ingest and also run the GPT app, we can get this error on system with Python 3.10 or older

```python
RuntimeError: Your system has an unsupported version of sqlite3. Chroma requires sqlite3 >= 3.35.0.
```

If this occurs then use the Docker container to run your commands, instructions are given below under each sub-section.

[back to ToC](#table-of-contents)

## Usage

### Ask questions

#### via native shell CLI

Before running ```lpiGPT.py```you need to specify the base URL for the Ollama API or the local instance of Ollama running on your machine. By default this will return a ```None``` value.

- Windows:
  - This is typically http://localhost:11434 and can be set by using the following in command line:
```shell
set OLLAMA_HOST=http://localhost:11434
```

```shell
python3 lpiGPT.py

Enter a query: Fetch me all machine learning courses of the advanced level from the Learning Path Index and show me results in a tabular form

Start time: 2023-10-07 16:14:18
> Question:
Fetch me all machine learning courses of the advanced level from the Learning Path Index and show me results in a tabular form
End time: 2023-10-07 16:17:19
Answer (took about 181.3118166923523 seconds):
| Course Name | Level | Type | Duration | Module / Sub-module | Keywords/Tags/Skills/Interests/Categories | Links |
|-------------------------------|--------|-------|----------|--------------------------------------|-----------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------|
1. Machine Learning Engineer Learning Path | Intermediate to Advanced | Free during mentorship period | AI Foundations: Quiz | Machine Learning/ Cloud/Data/Infrastructure/Bigquery/| https://www.cloudskillsboost.google/course_sessions/4968855/quizzes/387518
2. Machine Learning Engineer Learning Path | Intermediate to Advanced | Free during mentorship period | AI Development Workflow: Quiz | AI/Development/API/Vertex AI/MLOps/Workflow| https://www.cloudskillsboost.google/course_sessions/4968855/quizzes/387541
3. Machine Learning Engineer Learning Path | Intermediate to Advanced | Free during mentorship period | AI Development Options: Quiz | AI/Development/API/Vertex AI/AutoML/Workflow| https://www.cloudskillsboost.google/course_sessions/4968855/quizzes/387529
4. Machine Learning Engineer Learning Path | Intermediate to Advanced | Free during mentorship period | BigQuery Machine Learning: Develop ML Models Where Your Data Lives: Introduction | Big Query/Explanable AI/ML models/Hyperparameter. tuning/recommendation system| https://www.cloudskillsboost.google/course_sessions/4968855/quizzes/387530
Note: The results will be displayed in a table format with columns for Course Name, Level, Type, Duration, Module / Sub-module, Keywords/Tags/Skills/Interests/Categories and Links.

.
.
.
[A list of source documents it got the results from]
.
.
.
```

To exit the GPT prompt, press Ctrl-C or Ctrl-D and it will return to the Linux/Command-prompt.


```bash                                                             
> python3 lpiGPT.py --help
usage: lpiGPT.py [-h] [--chat-model CHAT_MODEL] [--embeddings-model-name EMBEDDINGS_MODEL_NAME] [--persist-directory PERSIST_DIRECTORY]
                 [--target-source-chunks TARGET_SOURCE_CHUNKS] [--hide-source] [--mute-stream]

lpiGPT: Ask questions to your documents without an internet connection, the power of LLMs (the InstructGPT or Chat model).

optional arguments:
  -h, --help            show this help message and exit
  --chat-model CHAT_MODEL, -CM CHAT_MODEL
                        Use this flag to set the InstructGPT or Chat model name, see https://huggingface.co/spaces/lmsys/chatbot-arena-leaderboard or
                        https://ollama.ai/library for more names.
  --embeddings-model-name EMBEDDINGS_MODEL_NAME, -EM EMBEDDINGS_MODEL_NAME
                        Use this flag to set the Embeddings model name, see https://www.sbert.net/docs/pretrained_models.html for examples of names. Use the same model as
                        used for ingesting the documents (ingest.py)
  --persist-directory PERSIST_DIRECTORY, -P PERSIST_DIRECTORY
                        Use this flag to specify the name of the vector database, this will be a folder on the local machine.
  --target-source-chunks TARGET_SOURCE_CHUNKS, -C TARGET_SOURCE_CHUNKS
                        Use this flag to specify the name chunk size to use to chunk source data.
  --hide-source, -S     Use this flag to disable printing of source documents used for answers.
  --mute-stream, -M     Use this flag to disable the streaming StdOut callback for LLMs.
```

#### via Docker container

You can also setup an isolated environment i.e. inside Docker container and perform the same above operations

```shell
cd docker
./build-docker-image.sh
```

when finished with building the container run the below

```shell
./run-docker-container.sh
```

you will get a prompt like this:

```shell
root@[your machine name]:/home#:
```

in there, type the same commands as in the **via native shell CLI** sections of [Ingesting files](#ingesting-files) and [Ask questions](#ask-questions) respectively.


### Try a different model

```shell
ollama pull llama2:13b
python3 lpiGPT.py --chat-model=llama2:13b
```

### Adding more files

Put any and all your files into the `source_documents` directory

The supported extensions are:

- `.csv`: CSV
and others, we have trimmed them off from here to keep this example simple and concise.

[back to ToC](#table-of-contents)

## Models

### Embeddings models

For embeddings model, the example uses a sentence-transformers model https://www.sbert.net/docs/pretrained_models.html
The `all-mpnet-base-v2` model provides the best quality, while `all-MiniLM-L6-v2` is 5 times faster and still offers good quality.

### Chat models

For chat models, have a look at [this list](https://github.com/jmorganca/ollama/#model-library) on [Ollama's github repo](https://github.com/jmorganca/ollama/). The list is basic, hence other LLM resources must be consulted i.e.

- [Kaggle models](https://www.kaggle.com/models?query=LLM)
- [HuggingFace models](https://huggingface.co/models?other=LLM)
- ...(others)..

_Please share your resources on either or both of the Embeddings and Chat models with us_

## Contributing

We are open to any or all of the below from your side in terms of contributions:

    - Reporting issues
    - Submitting pull requests
    - Coding standards or guidelines
    - Testing requirements

## License

See [LICENSE](https://github.com/neomatrix369/learning-path-index/blob/main/LICENSE) in the root folder of the project

[back to ToC](#table-of-contents)
