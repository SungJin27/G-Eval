import subprocess
import sys
import os
from dotenv import load_dotenv

load_dotenv()

# 환경변수에서 키를 읽어오거나, 직접 입력해도 됩니다.
MODELS = [
    # "gpt-4-0613",
    "gpt-4.1-2025-04-14",
    # "gpt-4.1-mini-2025-04-14",
    # "gpt-4.1-nano-2025-04-14",
    # "gpt-4o-mini-2024-07-18",
    # "gpt-4o-2024-08-06",
]

PROMPT_FP   = "prompts/summeval/con_detailed.txt"
SUMMEVAL_FP = "data/summeval.json"
RESULT_DIR  = "results"
API_KEY = os.getenv("API_KEY")

os.makedirs(RESULT_DIR, exist_ok=True)

for model in MODELS:
    save_fp = os.path.join(RESULT_DIR, str(model) + ".json")
    cmd = [
        sys.executable,
        os.path.join(os.path.dirname(__file__), "gpt4_eval.py"),
        "--prompt_fp", PROMPT_FP,
        "--save_fp", save_fp,
        "--summeval_fp", SUMMEVAL_FP,
        "--key", API_KEY,
        "--model", model
    ]
    print("Running: " + model)
    subprocess.run(cmd, check=True)
