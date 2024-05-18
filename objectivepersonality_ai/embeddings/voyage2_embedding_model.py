import numpy as np
from .embeddings_model import EmbeddingModel
import voyageai

class VoyageEmbeddings(EmbeddingModel):

    def __init__(self, instruction: str = None) -> None:
        self.model = voyageai.Client()

    def _embed(self, sentences: list[str]) -> np.ndarray:
        instruction = "Classify the text: "
        full_sentence = [instruction + sentence for sentence in sentences]
        embeddings = self.model.embed(full_sentence, model="voyage-large-2-instruct", input_type=None).embeddings
        return np.array(embeddings)
