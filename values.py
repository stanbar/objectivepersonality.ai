import pandas as pd
import numpy as np
import os
from gritlm import GritLM
from dotenv import load_dotenv, find_dotenv
import tiktoken
import ollama
load_dotenv(find_dotenv(usecwd=False, raise_error_if_not_found=True))

TRANSCRIPTS_CSV = os.getenv("TRANSCRIPTS_CSV")
if TRANSCRIPTS_CSV is None:
    raise ValueError("TRANSCRIPTS_CSV environment variable must be set")

TRANSCRIPTS_WITH_VALUES_CSV = os.getenv("TRANSCRIPTS_WITH_VALUES_CSV")
if TRANSCRIPTS_WITH_VALUES_CSV is None:
    raise ValueError("TRANSCRIPTS_WITH_VALUES_CSV environment variable must be set")

df = pd.read_csv(TRANSCRIPTS_CSV)

def trim_to_max_tokens(text, max_tokens=16000, model='cl100k_base'):
    # Step 2: Initialize the tiktoken encoder for the given model
    encoder = tiktoken.get_encoding(model)
    
    # Step 3: Encode the text into tokens
    tokens = encoder.encode(text)
    
    # Step 4: Trim the tokens if they exceed the max_tokens limit
    if len(tokens) > max_tokens:
        tokens = tokens[:max_tokens]
    
    # Step 5: Decode the tokens back to string
    trimmed_text = encoder.decode(tokens)
    
    return trimmed_text

def calculate_embeddings(interview: str) -> np.ndarray:
    """Function to calculate embeddings for a list of texts"""
    # interview = trim_to_max_tokens(text, max_tokens=16000)
    messages = [
      {
        "role": "user",
        "content": f"Please give me a list of the 5 top most important values of the person based on his transcript where he talks about his life. The output must consist only of a Python list of strings and nothing else, so I can interpret it directly from Python environment. Here is the transcript: \n---\n {interview}"
        },
    ]
    response = ollama.chat(model='llama3', messages=messages)
    content = response['message']['content']
    return content

def ensure_values_and_interests(df: pd.DataFrame, batch_size: int = 1) -> pd.DataFrame:
    """Ensure that values and interests are calculated and updated for a DataFrame"""
    # Filter rows that need embeddings
    to_embed = df[(df["transcript_tokens_length"] >= 1000)]
    texts = to_embed["transcript_txt"].tolist()
    indices = to_embed.index.tolist()

    # Process in batches
    for start in range(0, len(texts), batch_size):
        batch_texts = texts[start:start + batch_size]
        batch_indices = indices[start:start + batch_size]
        embedding = calculate_embeddings(batch_texts[0])
        for i, idx in enumerate(batch_indices):
            print(embedding)
            df.at[idx, "values"] = embedding
            print(f"Processed values {i + 1}/{len(batch_indices)} in current batch, overall progress: {start + i + 1}/{len(texts)}")

    return df

# Ensure the 'embeddings' column exists and is initialized if necessary
if "values" not in df.columns:
    df["values"] = np.nan  # Initialize as NaN
df["values"] = df["values"].astype(str)

df = ensure_values_and_interests(df, batch_size=1)

df = df.drop(columns=["transcript_wps", "transcript_txt"])

df.to_csv(TRANSCRIPTS_WITH_VALUES_CSV, index=False)

print(f"Updated values, saved to {TRANSCRIPTS_WITH_VALUES_CSV}")