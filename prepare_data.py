import json
import os
from schema_utils import get_schema

os.makedirs("data", exist_ok=True)

def make_example(row):
    schema = get_schema(row["db_id"])
    user = (
        "You are an expert SQL assistant. Given the database schema below, "
        "write a single SQL query that answers the question. "
        "Return only the SQL, no explanation. "
        "Use lowercase SQL functions and do not use column or table aliases "
        "unless necessary. Match this style: SELECT count(*) FROM table\n\n"
        f"Schema:\n{schema}\n\n"
        f"Question: {row['question']}"
    )
    return {
        "messages": [
            {"role": "user", "content": user},
            {"role": "assistant", "content": row["query"]},
        ]
    }

def write_split(in_file, out_file):
    with open(in_file) as f:
        rows = json.load(f)
    with open(out_file, "w") as f:
        for row in rows:
            f.write(json.dumps(make_example(row)) + "\n")

write_split("spider_data/train_spider.json", "data/train.jsonl")
write_split("spider_data/dev.json", "data/valid.jsonl")
print("Wrote data/train.jsonl and data/valid.jsonl")