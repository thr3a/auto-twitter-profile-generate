import torch
from transformers import T5Tokenizer, AutoModelForCausalLM
import tweepy
import random
import os

def generate_text(text):
    model_name = '/root/.cache/huggingface/hub/models--rinna--japanese-gpt-1b/snapshots/a3c6e8478d5afa92fe5174b984555e01fe378cd3'
    tokenizer = T5Tokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    if torch.cuda.is_available():
        model = model.to("cuda")
    
    token_ids = tokenizer.encode(text, add_special_tokens=False, return_tensors="pt")

    with torch.no_grad():
        output_ids = model.generate(
            token_ids.to(model.device),
            max_length=60,
            min_length=40,
            do_sample=True,
            top_k=500,
            top_p=0.95,
            pad_token_id=tokenizer.pad_token_id,
            bos_token_id=tokenizer.bos_token_id,
            eos_token_id=tokenizer.eos_token_id,
            # bad_word_ids=[[tokenizer.unk_token_id]]
        )

    output = tokenizer.decode(output_ids.tolist()[0])
    return output

def update_description(text):
    consumer_key = "kfPiWOWRcHuWKgMdndnFr0RP0"
    consumer_secret = os.environ['TWITTER_COMSUMER_SECRET']
    access_token = "1179190262-sTeCsUVdPTj8nDNVY8BXOCW4N7p4Yiq34PlEj22"
    access_token_secret = os.environ['TWITTER_TOKEN_SECRET']

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    api.update_profile(description=text)

with open('first.txt') as f:
    lines = f.read().splitlines()
    first_title = random.choice(lines)

with open('second.txt') as f:
    lines = f.read().splitlines()
    second_title = random.choice(lines)

base_text = first_title+second_title
description = generate_text(base_text).replace('</s>', '')
update_description(description)
print(description)
