# Gemma Model Learning Index Path Documentation

## Project Overview

This project involves fine-tuning the Google Gemma model on a custom dataset, specifically the Learning Path Index (LPI) Dataset, with the goal of creating a web-based application that interacts with a language model to provide learning path recommendations.

### Project Achievements
1. **Dataset Creation**: Utilizes the LPI Dataset (`neomatrix369/learning-path-index-dataset`) from Kaggle.
2. **Model Fine-Tuning**: Fine-tunes the `keras/gemma2/Keras/gemma2_2b_en/1` model on the LPI Dataset, employing techniques like LoRA or QLoRA.

### Notebooks
The following Jupyter Notebooks guide each step in the pipeline:

- **`lpi_qna_pair_generation.ipynbb`**: Processes and prepares the LPI Dataset for fine-tuning.
- **`lpi_gemma_finetuning.ipynb`**: Implements model fine-tuning with options for LoRA and QLoRA, specifically on the Gemma2 model.
