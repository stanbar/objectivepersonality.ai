from abc import ABCMeta, abstractmethod
from numpy import ndarray


class EmbeddingModel(metaclass=ABCMeta):
    def embed(self, sentences: str) -> ndarray:
        embeddings = self._embed(sentences)

        if not isinstance(embeddings, ndarray):
            raise TypeError("Embeddings must be a numpy array.")

        return embeddings

    @abstractmethod
    def _embed(self, sentences: str) -> ndarray:
        pass
