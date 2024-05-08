def evaluate_neural_networks():
    from objectivepersonality_ai.classifiers.neural_network import (
        NeuralNetworkClassifier,
    )

    neural_networks_classifier = NeuralNetworkClassifier()
    neural_networks_classifier.evaluate()


if __name__ == "__main__":
    evaluate_neural_networks()
