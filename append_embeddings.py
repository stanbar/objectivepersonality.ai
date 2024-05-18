import pandas as pd
import numpy as np
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv(usecwd=False, raise_error_if_not_found=True))
from objectivepersonality_ai.embeddings.voyage2_embedding_model import VoyageEmbeddings

TRANSCRIPTS_CSV = os.getenv("TRANSCRIPTS_CSV")
if TRANSCRIPTS_CSV is None:
    raise ValueError("TRANSCRIPTS_CSV environment variable must be set")

TRANSCRIPTS_WITH_EMBEDDINGS_CSV = os.getenv("TRANSCRIPTS_WITH_EMBEDDINGS_CSV")
if TRANSCRIPTS_WITH_EMBEDDINGS_CSV is None:
    raise ValueError("TRANSCRIPTS_WITH_EMBEDDINGS_CSV environment variable must be set")

df = pd.read_csv(TRANSCRIPTS_CSV)

# Ensure the 'embeddings' column exists and is initialized if necessary
if "embeddings" not in df.columns:
    df["embeddings"] = np.nan  # Initialize as NaN

# old_promp = "Represent the person's demons, areas of fears and avoidants, and saviours, confidence and responsibility"
# prompt = "Represent the person's demons: fears, avoidances, disrespects and neglections vs saviours: confidence, responsibility, respects and diligence. The transcript contains metadata consisting of words per second [wps]. Use the metadata to understand the rate of speech and the moments when a person slows down and when he speeds up to recognise demon and savior states. People usually speed up when they are using their saviour functions, and slow down then going into demons."
# model = GritLMEmbeddings(
#     prompt
# ) 
model = VoyageEmbeddings()

def calculate_embeddings(texts: list[str]) -> np.ndarray:
    """Function to calculate embeddings for a list of texts"""
    return model.embed(texts)

def ensure_embeddings(df: pd.DataFrame, batch_size: int = 10) -> pd.DataFrame:
    """Ensure that embeddings are calculated and updated for a DataFrame"""
    # Filter rows that need embeddings
    to_embed = df[(df["transcript_tokens_length"] >= 1000) & (df["embeddings"].isna())]
    texts = to_embed["transcript_txt"].tolist()
    indices = to_embed.index.tolist()

    # Process in batches
    for start in range(0, len(texts), batch_size):
        batch_texts = texts[start:start + batch_size]
        batch_indices = indices[start:start + batch_size]
        embeddings = calculate_embeddings(batch_texts)
        for i, idx in enumerate(batch_indices):
            df.at[idx, "embeddings"] = embeddings[i].tolist()
            print(f"Processed embedding {i + 1}/{len(batch_indices)} in current batch, overall progress: {start + i + 1}/{len(texts)}")

    return df

df["embeddings"] = df["embeddings"].astype(object)

df = ensure_embeddings(df, batch_size=8)

df = df.drop(columns=["transcript_wps", "transcript_txt"])

df.to_csv(TRANSCRIPTS_WITH_EMBEDDINGS_CSV, index=False)

print(f"Updated embeddings, saved to {TRANSCRIPTS_WITH_EMBEDDINGS_CSV}")
