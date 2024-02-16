---
title: KaggleX Learning Path Index Chatbot (Demo)
emoji: 💻
colorFrom: pink
colorTo: purple
sdk: streamlit
sdk_version: 1.21.0
app_file: app.py
pinned: false
---

Check out the deployed demo version at https://huggingface.co/spaces/Entz/llm_5

## Pulling the docker image from repository
docker run -it -p 7860:7860 --platform=linux/amd64 \
	-e OPENAI_API_KEY="YOUR_VALUE_HERE" \
	registry.hf.space/entz-llm-5:latest streamlit run app.py

This docker image requires some secrets to run, don't forget to set the environment values (your "OPENAI_API_KEY" in this case) in your docker command!

This repository is the prototype in A prototype written in Python to illustrate/demonstrate querying a tiny dataset extracted from the Learning Path Index Dataset (see [Kaggle Dataset](https://www.kaggle.com/datasets/neomatrix369/learning-path-index-dataset )

The dataset is stored in the folder named chroma, and can be found in the same directory. 

## Pre-requisites

- Python 3.9.x or above
- OpenAI API Key
- Install dependencies from `requirements.txt`
- Basic Command-line experience
- Basic git and GitHub experience

## Known issue

- The AI can't do simple counting well. e.g. there are 3 courses in the dataset, but AI always returns 4 when its being asked how many courses in the database.

- The AI can't interpret course fee correctly when the fee is zero. Perhaps this can be fixed in prompt engineering.

- To get better accuracy in AI's interpretation on the dataset, further cleaning has to be done on the dataset.
