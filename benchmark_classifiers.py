def evaluate_centroids():
  from objectivepersonality_ai.classifiers.centroids import CentroidsClassifier
  centroids_classifier = CentroidsClassifier()
  centroids_classifier.evaluate()

def evaluate_neural_networks():
  from objectivepersonality_ai.classifiers.neural_network import NeuralNetworkClassifier
  neural_networks_classifier = NeuralNetworkClassifier()
  neural_networks_classifier.evaluate()

def evaluate_proto_networks():
  from objectivepersonality_ai.classifiers.proto_networks import ProtoNetworksClassifier
  proto_netoworks_classifier = ProtoNetworksClassifier()
  proto_netoworks_classifier.evaluate()

print("---------Neural-Networks----------")
evaluate_neural_networks()
print("---------Centroids----------")
evaluate_centroids()
print("---------Proto-Networks----------")
evaluate_proto_networks()