def evaluate_proto_networks():
  from objectivepersonality_ai.classifiers.proto_networks import ProtoNetworksClassifier
  proto_netoworks_classifier = ProtoNetworksClassifier()
  proto_netoworks_classifier.evaluate()

if __name__ == '__main__':
  evaluate_proto_networks()