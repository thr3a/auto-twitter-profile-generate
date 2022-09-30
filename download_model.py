from huggingface_hub import snapshot_download
from transformers import T5Tokenizer, AutoModelForCausalLM
download_path = snapshot_download(repo_id="rinna/japanese-gpt-1b")

print(download_path)
