from evaluation import evaluate, build_foreign_key_map_from_json

DB_DIR = "spider_data/database"
TABLE = "spider_data/tables.json"
GOLD = "spider_data/dev_gold.sql"


def score(pred_file, gold_file=GOLD, etype="all",
          db_dir=DB_DIR, table=TABLE):
    """
    Run the official Spider evaluation and print the score breakdown.

    pred_file  one predicted SQL per line, same order as the gold file
    gold_file  gold SQL <tab> db_id per line (dev_gold.sql already is this)
    etype      "all", "exec", or "match"
    """
    kmaps = build_foreign_key_map_from_json(table)
    evaluate(gold_file, pred_file, db_dir, etype, kmaps)


if __name__ == "__main__":
    # Score the base model, no-RAG predictions, liimited to 5
    score("pred_small.sql")