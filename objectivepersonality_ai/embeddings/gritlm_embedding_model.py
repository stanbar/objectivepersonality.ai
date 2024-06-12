from gritlm import GritLM
from numpy import ndarray
from .embeddings_model import EmbeddingModel


class GritLMEmbeddings(EmbeddingModel):

    @staticmethod
    def gritlm_instruction(instruction):
        return (
            "<|user|>\n" + instruction + "\n<|embed|>\n"
            if instruction
            else "<|embed|>\n"
        )

    def __init__(self, instruction: str = None) -> None:
        self.model = GritLM("GritLM/GritLM-8x7B", mode="embedding", torch_dtype="auto", device_map="auto")
        # self.model = GritLM("GritLM/GritLM-7B", mode="embedding", torch_dtype="auto")
        self.instruction = self.gritlm_instruction(instruction)

    def _embed(self, sentences):
        return self.model.encode(sentences, instruction=self.instruction)
