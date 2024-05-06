def evaluate_centroids():
  from ..classifiers.centroids import CentroidsClassifier
  centroids_classifier = CentroidsClassifier()
  centroids_classifier.evaluate()

if __name__ == '__main__':
  evaluate_centroids()