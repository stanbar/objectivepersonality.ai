def evaluate_centroids():
    from objectivepersonality_ai.classifiers.weighted_centroids import WeightedCentroidsClassifier

    centroids_classifier = WeightedCentroidsClassifier()
    centroids_classifier.evaluate()


if __name__ == "__main__":
    evaluate_centroids()
