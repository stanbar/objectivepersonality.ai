from sentence_transformers import SentenceTransformer
from embeddings_model import EmbeddingModel

# https://huggingface.co/Salesforce/SFR-Embedding-Mistral

class SFREmbeddings(EmbeddingModel):
    def __init__(self) -> None:
        self.model_name = "Salesforce/SFR-Embedding-Mistral"
        self.model = SentenceTransformer(self.model_name)

    def _embed(self, sentences: str):
        return self.model.encode(sentences)
