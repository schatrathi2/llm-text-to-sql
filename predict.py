import json
import re
from mlx_lm import load, generate
from schema_utils import get_schema
from rag import retrieve_schema

def build_prompt(db_id, question, use_rag=False):
    schema = retrieve_schema(db_id, question) if use_rag else get_schema(db_id)
    return (
        "You are an expert SQL assistant. Given the database schema below, "
        "write a single SQL query that answers the question. "
        "Return only the SQL, no explanation. "
        "Use lowercase SQL functions and do not use column or table aliases "
        "unless necessary. Match this style: SELECT count(*) FROM table\n\n"
        f"Schema:\n{schema}\n\n"
        f"Question: {question}"
    )

def clean_sql(text):
    """Strip markdown fences, trailing semicolons, collapse to one line."""
    text = re.sub(r"```sql|```", "", text).strip()
    text = " ".join(text.split())
    return text.rstrip(";").strip()

def run(adapter_path=None, use_rag=False, out_file="pred.sql", limit=None):
    model, tokenizer = load(
        "mlx-community/Qwen2.5-7B-Instruct-4bit",
        adapter_path=adapter_path,
    )
    with open("spider_data/dev.json") as f:
        rows = json.load(f)
    if limit is not None:
        rows = rows[:limit]

    with open(out_file, "w") as out:
        for row in rows:
            prompt = build_prompt(row["db_id"], row["question"], use_rag)
            messages = [{"role": "user", "content": prompt}]
            text = tokenizer.apply_chat_template(
                messages, add_generation_prompt=True, tokenize=False
            )
            pred = generate(model, tokenizer, prompt=text, max_tokens=256)
            out.write(clean_sql(pred) + "\n")
    print(f"Wrote {out_file}")

if __name__ == "__main__":
    # Example: base model, no RAG, limited to 5
    run(adapter_path=None, use_rag=False, out_file="predictions/pred_small.sql", limit=5)