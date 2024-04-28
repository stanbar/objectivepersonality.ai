from sentence_transformers import SentenceTransformer
from embeddings_model import EmbeddingModel

# https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2

class MiniLMEmbeddings(EmbeddingModel):
    def __init__(self) -> None:
        self.model_name = "sentence-transformers/all-MiniLM-L6-v2"
        self.model = SentenceTransformer(self.model_name)

    def _embed(self, sentences: str):
        return self.model.encode(sentences)
