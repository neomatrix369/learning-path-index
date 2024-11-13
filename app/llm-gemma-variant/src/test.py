import os 
from dotenv import load_dotenv
from llama_index.core import Settings
from loguru import logger
from llama_index.llms.ollama import Ollama
from model import Gemma
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from vector_db import VectorDB
from pathlib import Path

# Initialize the model
gemma2_2b = Ollama(model="gemma2:2b", request_timeout=60.0)
logger.debug(gemma2_2b.complete("Hello, how are you?"))
llm_model = Gemma(gemma2_2b, 2000)
Settings.llm = llm_model

print(llm_model.complete(prompt = "Hello, how are you?"))