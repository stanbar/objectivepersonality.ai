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

TRANSCRIPTS_WITH_SAVIORS_DEMONS_CSV = os.getenv("TRANSCRIPTS_WITH_SAVIORS_DEMONS_CSV")
if TRANSCRIPTS_WITH_SAVIORS_DEMONS_CSV is None:
    raise ValueError("TRANSCRIPTS_WITH_SAVIORS_DEMONS_CSV environment variable must be set")

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
        "content": f"Please give me a list of person's demons and saviours. Demons are person's fears, avoidances, disrespects and neglections. Saviours are person's areas of confidence, responsibility, respects and diligence. Here is the transcript: \n---\n {interview}"
        },
    ]
    response = ollama.chat(model='llama3', messages=messages)
    content = response['message']['content']
    return content

def ensure_saviours_and_demons(df: pd.DataFrame, batch_size: int = 1) -> pd.DataFrame:
    """Ensure that saviours and demons are calculated and updated for a DataFrame"""
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
            df.at[idx, "saviors_and_demons"] = embedding
            print(f"Processed values {i + 1}/{len(batch_indices)} in current batch, overall progress: {start + i + 1}/{len(texts)}")

    return df

# Ensure the 'embeddings' column exists and is initialized if necessary
if "saviors_and_demons" not in df.columns:
    df["saviors_and_demons"] = np.nan  # Initialize as NaN
df["saviors_and_demons"] = df["saviors_and_demons"].astype(str)

df = ensure_saviours_and_demons(df, batch_size=1)

df = df.drop(columns=["transcript_wps", "transcript_txt"])

df.to_csv(TRANSCRIPTS_WITH_SAVIORS_DEMONS_CSV, index=False)

print(f"Updated saviors_and_demons, saved to {TRANSCRIPTS_WITH_SAVIORS_DEMONS_CSV}")