from predict import run

run(adapter_path=None,        use_rag=False, out_file="predictions/pred_base.sql")
run(adapter_path=None,        use_rag=True,  out_file="predictions/pred_base_rag.sql")
run(adapter_path="./adapters", use_rag=False, out_file="predictions/pred_ft.sql")
run(adapter_path="./adapters", use_rag=True,  out_file="predictions/pred_ft_rag.sql")