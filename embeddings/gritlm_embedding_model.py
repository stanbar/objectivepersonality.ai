from gritlm import GritLM
from numpy import ndarray
from embeddings_model import EmbeddingModel


class GritLMEmbeddings(EmbeddingModel):
    def __init__(self) -> None:
        self.model_name = "GritLM/GritLM-7B"
        self.model = GritLM(self.model_name, mode="embedding", torch_dtype="auto")

    def gritlm_instruction(instruction):
        return (
            "<|user|>\n" + instruction + "\n<|embed|>\n"
            if instruction
            else "<|embed|>\n"
        )

    def _embed(self, sentence):
        return self.model.encode(
            sentence,
            #  instruction=gritlm_instruction("Represent the transcript of a person talking about his life to classify its personality type, traits, fears, and confidence")
        )
