# Objective Personality AI

Objective Personality AI (OPAI) is project aimed at developing AI models to classify personality types based on video transcripts. This project utilizes datasets gathered from various sources, including YouTube, and incorporates machine learning techniques to achieve its goal.

## System Requirements

To run the scripts effectively, especially those involving computing embeddings like `GritLM/GritLM-7B`, ensure your system meets the following requirements:

- **GPU Memory**: At least 27 GB of GPU memory is required to compute embeddings with the `GritLM/GritLM-7B` model.
- **Processing Time**: It takes approximately 5 seconds to compute embeddings per dataset entry.

Note: These requirements are crucial for performance and avoiding runtime errors due to insufficient resources.

For alternative models see [MTEB leaderboard](https://huggingface.co/spaces/mteb/leaderboard)


## Dataset

The success of AI typing relies heavily on the quality and variety of data it can access. Currently, there are two methods for gathering data:

- Utilizing the dataset created by [Tom Aylott (subtlegradient)](https://huggingface.co/datasets/subtlegradient/aop-dataset-2022-11-10-interview-lines-by-youtube)
- Scraping data from YouTube videos using [this project](https://github.com/michalbaldyga/personality-type-prediction-ops/tree/dev/backend/gathering_data)

The repository assumes the dataset is provided in the following CSV format specified in the `.env` file under the `TRANSCRIPTS_CSV=<path_to_dataset.csv>`:


```csv
name,ops_type,ModalitySensory,ModalityDe,ObserverDecider,DiDe,OiOe,SN,TF,SleepPlay,BlastConsume,InfoEnergy,IntroExtro,FlexFriends,GeneralisationSpecialisation,transcript_tokens_length,transcript
```

Field descriptions:

- `name` Normalized person's name using `utils#normalise_name(name)`
- `ops_type` Full ops type (e.g. MF-Ni/Fi-SB/P(C) [2])
- `ModalitySensory: 'F' | 'M' | None` Sexual modality of the sensory function
- `ModalityDe: 'F' | 'M' | None` Sexual modality of the extroverted decider function
- `ObserverDecider: 'Observer' | 'Decider' | None`
- `DiDe: 'Di' | 'De' | None`
- `OiOe: 'Oi' | 'Oe' | None`
- ...
- `transcript_tokens_length` number of tokens computed with `tiktoken.get_encoding("cl100k_base")`
- `transcript` transcript of a person

## Installation

Clone the repository and navigate to the project directory:

```sh
git clone https://github.com/stanbar/objectivepersonality.ai.git
cd objectivepersonality.ai
```

Install dependencies:

```sh
poetry install
```
## Usage

### Compute embeddings

To compute embeddings based on the transcripts from `TRANSCRIPTS_CSV` and outputs to `TRANSCRIPTS_WITH_EMBEDDINGS_CSV`

```sh
poetry run append_embeddings.py
```

## Run benchmark for all classifiers

To run benchmarks for all classifiers:

```sh
./benchmark.sh
```

# License

This project is licensed under the PolyForm Perimeter License 1.0.1 - see the LICENSE file for details.

# Support

For support, raise an issue in the GitHub issue tracker or contact the maintainers via hello@objectivepersonality.ai

### Compute values

To compute a values of the people in the interviews 

```sh
ollama serve
```

```sh
python3 run values.py
```


### Compute saviours and demons

To compute peoples' demons and saviours

```sh
ollama serve
```

```sh
python3 run saviours_demons.py
```