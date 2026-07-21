import chromadb
from sentence_transformers import SentenceTransformer
from schema_utils import TABLES

embedder = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.Client()

def get_table_texts(db_id):
    """Return a list of (table_name, "table: col, col, ...") for a database."""
    t = TABLES[db_id]
    names = t["table_names_original"]
    cols = t["column_names_original"]
    out = []
    for ti, table in enumerate(names):
        col_names = [c[1] for c in cols if c[0] == ti]
        out.append((table, f"Table {table}: {', '.join(col_names)}"))
    return out

def build_index(db_id):
    """Embed each table's description and store it in a per-database collection."""
    collection = client.get_or_create_collection(name=f"db_{db_id}")
    for name, text in get_table_texts(db_id):
        vector = embedder.encode(text).tolist()
        collection.add(ids=[name], embeddings=[vector], documents=[text])
    return collection

def retrieve_schema(db_id, question, top_k=3):
    """Return the descriptions of the top_k tables most relevant to the question."""
    collection = build_index(db_id)
    q_vector = embedder.encode(question).tolist()
    results = collection.query(query_embeddings=[q_vector], n_results=top_k)
    return "\n".join(results["documents"][0])