# schema_utils.py
import json

def load_tables(tables_path="spider_data/tables.json"):
    """Load tables.json once and index it by db_id."""
    with open(tables_path) as f:
        data = json.load(f)
    return {entry["db_id"]: entry for entry in data}

TABLES = load_tables()

def get_schema(db_id):
    """Return a readable schema string for a database, with foreign keys."""
    t = TABLES[db_id]
    table_names = t["table_names_original"]
    columns = t["column_names_original"]

    lines = []
    for ti, table in enumerate(table_names):
        cols = [c[1] for c in columns if c[0] == ti]
        lines.append(f"Table {table}: {', '.join(cols)}")

    fks = []
    for a, b in t["foreign_keys"]:
        ta, ca = table_names[columns[a][0]], columns[a][1]
        tb, cb = table_names[columns[b][0]], columns[b][1]
        fks.append(f"{ta}.{ca} = {tb}.{cb}")
    if fks:
        lines.append("Foreign keys: " + "; ".join(fks))

    return "\n".join(lines)