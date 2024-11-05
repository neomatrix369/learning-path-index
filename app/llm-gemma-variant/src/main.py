import os 
from dotenv import load_dotenv
from llama_index.core import Settings
from loguru import logger
from llama_index.llms.huggingface import HuggingFaceLLM
from llama_index.llms.huggingface_api import HuggingFaceInferenceAPI
from huggingface_hub import InferenceClient


# Load and verify API key
load_dotenv('credentials.env')
hf_token = os.getenv("hf_token")


client = InferenceClient()

for message in client.chat_completion(
	model="google/gemma-2-2b-it",
	messages=[{"role": "user", "content": "What is the capital of France?"}],
	max_tokens=500,
	stream=True,
):
    print(message.choices[0].delta.content, end="")