# kagglex-final-project

A prototype written in Python to illustrate/demonstrate querying the Learning Path Index Dataset (see [Kaggle Dataset](https://www.kaggle.com/datasets/neomatrix369/learning-path-index-dataset) and [GitHub repo](https://github.com/neomatrix369/learning-path-index)), with the help of the OpenAI GPT technology (InstructHPT model and embeddings model), [Langchain](https://python.langchain.com/) and using [Facebook's FAISS library](https://faiss.ai/).


![image](https://github.com/mbhoge/kagglex-final-project/assets/988040/5396aee3-cf0f-43b6-9b44-aaf779ed803a)


The end-to-end process can be learnt by going through the code base as well as by observing the console logs when using both the Streamlit and the CLI versions.

## Pre-requisites

- Python 3.8.x or above
- OpenAI API Key (see [How to get an OpenAI API Key](https://www.howtogeek.com/885918/how-to-get-an-openai-api-key/) -- note it's may not be FREE anymore)
- Install dependencies from `requirements.txt`
- Basic Command-line experience
- Basic git and GitHub experience

## Install and run

Copy the `.env_template` to `.env` in the current folder and then add your OpenAI API Key to `.env`. 
**Please don't modify the `.env_template` file.**


```bash
pip install -r requirements.txt
```

### Interactive session via CLI app

```bash
python main.py
```

![image](https://github.com/mbhoge/kagglex-final-project/assets/1570917/9bb04765-623d-452a-bcd0-82abf74ce6a9)


### Interactive session via Streamlit app

```bash
streamlit run main.py
```

![image](https://github.com/mbhoge/kagglex-final-project/assets/1570917/714eabc6-90bf-4e48-bf45-f2c8a307bf5a)

---
