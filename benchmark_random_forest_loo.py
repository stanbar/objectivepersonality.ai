def evaluate_random_forest():
    from objectivepersonality_ai.classifiers.random_forest_loo import (
        RandomForestClassifierModel,
    )

    model = RandomForestClassifierModel(True)
    model.evaluate()


if __name__ == "__main__":
    evaluate_random_forest()
