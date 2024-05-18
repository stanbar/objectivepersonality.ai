import pandas as pd
import numpy as np
import os
from dotenv import load_dotenv, find_dotenv
import chromadb
from scipy.spatial.distance import cosine

load_dotenv(find_dotenv(usecwd=False, raise_error_if_not_found=True))

TRANSCRIPTS_WITH_EMBEDDINGS_CSV = os.getenv("TRANSCRIPTS_WITH_EMBEDDINGS_CSV")
if TRANSCRIPTS_WITH_EMBEDDINGS_CSV is None:
    raise ValueError("TRANSCRIPTS_WITH_EMBEDDINGS_CSV environment variable must be set")


client = chromadb.Client()

data = pd.read_csv(TRANSCRIPTS_WITH_EMBEDDINGS_CSV)

# Convert embeddings from string to list
data['embeddings'] = data['embeddings'].apply(lambda x: np.fromstring(x.strip('[]'), sep=','))


# Group by 'name' and calculate the mean of the embeddings for each person
grouped_data = data.groupby('name')['embeddings'].apply(np.mean).reset_index()


# Create a vector collection in ChromaDB
collection_name = "transcript_embeddings"
if collection_name not in client.list_collections():
    client.create_collection(name=collection_name)
collection = client.get_collection(name=collection_name)


# Insert the vectors into the ChromaDB collection
for index, row in grouped_data.iterrows():
    person_name = row['name']
    embedding = row['embeddings']
    # Insert the document into the collection
    collection.add_document(id=person_name, vector=embedding.tolist(), metadata={"name": person_name})

print("Vector database creation completed successfully.")


# Function to find 3 closest neighbors
def find_closest_neighbors(client, collection_name, vector, top_n=3):
    # Query the collection for similar vectors
    results = client.query_collection(
        collection_name=collection_name,
        vector=vector,
        top_n=top_n + 1  # +1 because the closest one will be the vector itself
    )
    return results

# Prepare the output
output = []

# Find the 3 closest entries for each person
for index, row in grouped_data.iterrows():
    person_name = row['name']
    vector = row['embeddings'].tolist()
    results = find_closest_neighbors(client, collection_name, vector)
    
    for result in results:
        if result['id'] != person_name:  # Exclude the person itself
            output.append({
                "name": person_name,
                "closest_person": result['id'],
                "distance": result['distance']
            })

# Convert the output to DataFrame
output_df = pd.DataFrame(output)

# Write the results to an output CSV
output_csv = "closest_neighbors.csv"
output_df.to_csv(output_csv, index=False)

print(f"Output written to {output_csv}")