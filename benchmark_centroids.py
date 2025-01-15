import os
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv(usecwd=False, raise_error_if_not_found=True))

TRANSCRIPTS_WITH_EMBEDDINGS_CSV = os.getenv("TRANSCRIPTS_WITH_EMBEDDINGS_CSV")
if TRANSCRIPTS_WITH_EMBEDDINGS_CSV is None:
    raise ValueError("TRANSCRIPTS_WITH_EMBEDDINGS_CSV environment variable is not set")

def evaluate_centroids():
    from objectivepersonality_ai.classifiers.centroids import CentroidsClassifier

    centroids_classifier = CentroidsClassifier(TRANSCRIPTS_WITH_EMBEDDINGS_CSV)
    centroids_classifier.evaluate()


if __name__ == "__main__":
    evaluate_centroids()
