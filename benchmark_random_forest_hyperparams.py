def evaluate_random_forest():
    from objectivepersonality_ai.classifiers.random_forest_hyperparams import (
        RandomForestClassifierModel,
    )

    model = RandomForestClassifierModel()
    model.evaluate()


if __name__ == "__main__":
    evaluate_random_forest()
