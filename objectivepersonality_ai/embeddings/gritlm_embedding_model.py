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
        self.model_name = "GritLM/GritLM-7B"
        self.model = GritLM(self.model_name, mode="embedding", torch_dtype="auto")
        self.instruction = self.gritlm_instruction(instruction)

    def _embed(self, sentence):
        return self.model.encode(sentence, instruction=self.instruction)
