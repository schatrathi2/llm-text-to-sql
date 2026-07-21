# LLM-Powered Text-to-SQL

Fine-tuning an open-source LLM to translate natural-language questions into SQL, with a retrieval layer that supplies the right table schemas at query time. The model is LoRA fine-tuned on Apple Silicon and evaluated on the Spider benchmark.

## Overview

Given a database schema and a question in plain English, the system generates the SQL query that answers it. For example, "What is the total population of cities in California?" becomes `SELECT sum(population) FROM cities WHERE state = 'California'`.

The project has three parts that map to the SQL-generation task end to end. A Qwen model is LoRA fine-tuned on question-and-SQL pairs so it learns to produce correct, benchmark-style queries. A retrieval-augmented generation (RAG) layer embeds each database's table schemas in a vector store and retrieves only the relevant tables for a given question, which keeps prompts focused on databases with many tables. And an evaluation harness scores generated queries against real databases using Spider's official evaluator, reporting both exact set match and execution accuracy.

Everything runs on a single Apple Silicon machine using Apple's MLX framework. Fine-tuning uses LoRA (parameter-efficient fine-tuning), not full fine-tuning, which is what makes training feasible on a laptop.

## How it works

The base model is `mlx-community/Qwen2.5-7B-Instruct-4bit`. Fine-tuning is done with `mlx-lm`, which trains small LoRA adapters on top of the frozen base model. Retrieval uses `sentence-transformers` (the `all-MiniLM-L6-v2` embedding model) to encode table schemas, with `chromadb` as the vector store. Evaluation uses the official Spider scripts so results are directly comparable to the public Spider leaderboard.

## Repository structure

```
schema_utils.py     Builds a readable schema (with foreign keys) from tables.json
prepare_data.py     Reshapes Spider into the JSONL chat format mlx-lm expects
rag.py              Embeds table schemas and retrieves relevant ones per question
fine_tune.py        Runs LoRA fine-tuning on the base model
predict.py          Generates SQL predictions from the model
run_all.py          Runs predict.py across all four configurations
score.py            Scores a predictions file using the official Spider evaluator
all_scores.ipynb    Notebook to score every configuration
```

## Setup

### 1. Install dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install mlx-lm chromadb sentence-transformers
```

### 2. Get the Spider dataset

Download the Spider dataset from the official site, distributed under the CC BY-SA 4.0 license.

https://yale-lily.github.io/spider

Unzip it into the project root as `spider_data/`. After unzipping you should have `spider_data/train_spider.json`, `spider_data/dev.json`, `spider_data/dev_gold.sql`, `spider_data/tables.json`, and a `spider_data/database/` folder with one subfolder per database. These files are not included in this repository because of their size and license.

### 3. Get the official evaluation scripts

The scoring uses Spider's official evaluator. Download `evaluation.py` and `process_sql.py` from the Spider repository and place them in the project root next to `score.py`.

https://github.com/taoyds/spider

Use the Python 3 versions from the `master` branch. `evaluation.py` imports from `process_sql.py`, so both files are required and must sit in the same folder.

## Running the project

### 1. Prepare the training data

```bash
python prepare_data.py
```

This reads the Spider question files and writes `data/train.jsonl` and `data/valid.jsonl` in the chat format the trainer expects.

### 2. Fine-tune the model

```bash
python fine_tune.py
```

This runs LoRA fine-tuning on `mlx-community/Qwen2.5-7B-Instruct-4bit` using the prepared data, and saves the trained adapter to `./adapters`. Close memory-heavy applications while training.

### 3. Generate predictions

```bash
python run_all.py
```

This writes a predictions file for each configuration into `predictions/`, one predicted SQL per line matching the order of `dev.json`.

### 4. Score the results

Open `all_scores.ipynb` and run the cells. There is one cell per configuration, each scoring the corresponding predictions file with the official Spider evaluator.

Each cell prints a table of scores broken down by query difficulty (easy, medium, hard, extra) with a combined column (all). The two headline rows are execution accuracy, the share of predictions that return the same rows as the gold query when run against the database, and exact match, the share that match the gold query clause by clause. Below those, the table reports partial-matching scores for individual SQL components such as select, where, and group by, which are useful for seeing where the model is strong or weak. The number to report for each configuration is the value in the "all" column of the execution and exact match rows.

## Results

Evaluated on the Spider dev set (1034 questions). Numbers to be added.

| Configuration | Execution Accuracy | Exact Match |
|---|---|---|
| Base model | TBD | TBD |
| Base model + RAG | TBD | TBD |
| Fine-tuned | TBD | TBD |
| Fine-tuned + RAG | TBD | TBD |

## Notes on method

Fine-tuning uses LoRA, which trains small adapter matrices on top of the frozen base model rather than updating all of its weights. This is the standard approach for fine-tuning on consumer hardware and is not the same as full fine-tuning.

Scoring uses the standard Spider `evaluation.py`. Its execution-accuracy metric does not compare literal values by default. The separate test-suite evaluator published by the Spider authors is the stricter execution metric.

## Acknowledgements

Built on the Spider dataset (Yu et al., EMNLP 2018) and its official evaluation scripts. Model fine-tuning uses Apple's MLX framework and the Qwen model family.