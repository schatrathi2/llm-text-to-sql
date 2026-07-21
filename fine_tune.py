import subprocess

subprocess.run([
    "mlx_lm.lora",
    "--model", "mlx-community/Qwen2.5-7B-Instruct-4bit",
    "--train",
    "--data", "./data",
    "--iters", "600",
    "--batch-size", "4",
    "--num-layers", "16",
    "--adapter-path", "./adapters",
], check=True)