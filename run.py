from predict import run

run(adapter_path=None,        use_rag=False, out_file="pred_base.sql")
run(adapter_path=None,        use_rag=True,  out_file="pred_base_rag.sql")
run(adapter_path="./adapters", use_rag=False, out_file="pred_ft.sql")
run(adapter_path="./adapters", use_rag=True,  out_file="pred_ft_rag.sql")