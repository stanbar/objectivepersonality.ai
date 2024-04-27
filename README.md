# objectivepersonality.ai

## Dataset

Gathering data is one of the biggest problems in the goal of building OPS AI typing. Currently there are two known possibilities:

- Scrape data from youtube videos following [this project](https://github.com/michalbaldyga/personality-type-prediction-ops/tree/dev/backend/gathering_data)
- Use the dataset created by [Tom Aylott (subtlegradient)](https://huggingface.co/datasets/subtlegradient/aop-dataset-2022-11-10-interview-lines-by-youtube)

This repository does not specify how the dataset is gathered. However, it assumes a dataset provided in a file specified in `.env` field `TRANSCRIPTS_CSV=<path_to_dataset.csv>`, of the following format:

```csv
name,ops_type,mSe,mDe,ObserverDecider,DiDe,OiOe,SN,TF,SleepPlay,BlastConsume,InfoEnergy,IntroExtro,FlexFriends,GeneralisationSpecialisation,transcript_tokens_length,transcript
```
where:

- `name` a person name normalised with `utils/utils.py#normalise_name(name)`
- `ops_type` full ops type (e.g. MF-Ni/Fi-SB/P(C) [2])
- `mSe` sexual modality of the sensory function
- `mDe` sexual modality of the extroverted decider function
- `ObserverDecider: 'Observer' | 'Decider' | None`
- `DiDe: 'Di' | 'De' | None`
- `OiOe: 'Oi' | 'Oe' | None`
- ...
- `transcript_tokens_length` is a number of tokens computed from `tiktoken.get_encoding("cl100k_base")`
- `transcript` is a transcript of a person

## Run

```sh
poetry install
```

### Train neural_network classifier

```sh
poetry run python train/neural_network.py
```

### Train centroids

```sh
poetry run python train/centroids.py
```

### Train prototypical networks

```sh
poetry run python train/proto_networks.py
```

