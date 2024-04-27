import pandas as pd
import numpy as np
import os
from dotenv import load_dotenv, find_dotenv
from embeddings.gritlm_embedding_model import GritLMEmbeddings

load_dotenv(
    find_dotenv(usecwd=False, raise_error_if_not_found=True)
)

TRANSCRIPTS_CSV = os.getenv("TRANSCRIPTS_CSV")
if TRANSCRIPTS_CSV is None:
  raise ValueError("TRANSCRIPTS_CSV environment variable must be set")

TRANSCRIPTS_WITH_EMBEDDINGS_CSV = os.getenv("TRANSCRIPTS_WITH_EMBEDDINGS_CSV")
if TRANSCRIPTS_WITH_EMBEDDINGS_CSV is None:
  raise ValueError("TRANSCRIPTS_WITH_EMBEDDINGS_CSV environment variable must be set")

df = pd.read_csv(TRANSCRIPTS_CSV)

# Ensure the 'embeddings' column exists and is initialized if necessary
if 'embeddings' not in df.columns:
    df['embeddings'] = np.nan  # Initialize as NaN

model = GritLMEmbeddings()

def calculate_embeddings(texts, tokens_length):
    """Function to calculate embeddings for a list of texts"""
    embeddings = model.embed(texts,
    #  instruction=gritlm_instruction("Represent the transcript of a person talking about his life to classify its personality type, traits, fears, and confidence")
    )
    print(f"Computed embedding from {tokens_length} tokens")
    return embeddings[0]

def ensure_embeddings(row):
    """Ensure that embeddings are calculated and updated"""
    if pd.isna(row['embeddings']):
        row['embeddings'] = calculate_embeddings([row['transcript']], row['transcript_tokens_length']).tolist()
    return row

# Apply ensure_embeddings to each row
df = df[df['transcript_tokens_length'] >= 1000].apply(ensure_embeddings, axis=1)

# Save the updated DataFrame back to CSV
df.to_csv(TRANSCRIPTS_WITH_EMBEDDINGS_CSV, index=False)

print(f"Updated embeddings, saved to {TRANSCRIPTS_WITH_EMBEDDINGS_CSV}")
