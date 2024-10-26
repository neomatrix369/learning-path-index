# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy all application files into the container
COPY . /app

# Install system dependencies and libraries required by the application
RUN apt-get update && apt-get install -y \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies from requirements.txt
COPY requirements.txt /app/requirements.txt
RUN pip3 install -r requirements.txt

# Install specific packages to avoid any missing dependency issues
RUN pip3 install --no-cache-dir openai streamlit python-dotenv langchain faiss-cpu

# Verify that all required imports are installed
RUN python3 -c "import openai, streamlit, dotenv, langchain, faiss"

# Expose port 8501 for Streamlit
EXPOSE 8501

# Define environment variable to avoid buffering issues
ENV PYTHONUNBUFFERED=1

# Start the Streamlit app explicitly
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
