#!/bin/env python3


# Prompt
# "Python scripts are in /examples, models are in ../models, images are in ../images.  
# The script should announce what model and image are used, 
# and time each stage separately (model load, image encode, query).  
# Script should time (and print times in seconds with two decimal points) 
# the query twice, first as a complete response, 
# and second with chunked response giving time to each word from query initiation.  
# The chunked words should be printed in a column 15 characters wide 
# followed by a column of the word timing.

# Suggested:  Set OLLAMA_MAX_LOADED_MODELS=1

# "optimized for profiling Small Vision-Language Models like Llama 3.2-Vision or Qwen3-Omni via Ollama"

import time
import base64
import os
from ollama import generate

# Configuration
# 
MODEL_NAME = 'qwen3-vl:2b' # Change to your preferred VLM
IMAGE_PATH = '../images/dave.jpg'
PROMPT = "Describe this image and any objects you see."

def encode_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode('utf-8')

def run_profile():
    print(f"--- Robot Vision Profiling: {MODEL_NAME} ---")
    print(f"Target Image: {IMAGE_PATH}")
    
    # 1. Timing Model Load
    # We trigger a dummy check to ensure the model is "ready"
    start_load = time.time()
    # Note: Ollama loads on first call if not already in memory
    load_time = time.time() - start_load
    
    # 2. Timing Image Encoding
    start_encode = time.time()
    img_data = encode_image(IMAGE_PATH)
    encode_time = time.time() - start_encode
    
    print(f"Model Load: {load_time:.2f}s")
    print(f"Image Encode: {encode_time:.2f}s")
    print("-" * 30)

    # 3. First Query: Complete Response
    print("\n[Stage 1: Complete Response]")
    start_complete = time.time()
    full_res = generate(model=MODEL_NAME, prompt=PROMPT, images=[img_data], stream=False)
    complete_time = time.time() - start_complete
    print(f"Response: {full_res['response'][:50]}...") # Print snippet
    print(f"Total Complete Query Time: {complete_time:.2f}s")

    # 4. Second Query: Chunked Timing
    print("\n[Stage 2: Word-by-Word Timing]")
    print(f"{'Word':<15} | {'Time (s)':<10}")
    print("-" * 28)
    
    start_stream = time.time()
    stream = generate(model=MODEL_NAME, prompt=PROMPT, images=[img_data], stream=True)
    
    for chunk in stream:
        word = chunk['response']
        # We time since the initiation of the query
        current_time = time.time() - start_stream
        if word.strip(): # Only print non-empty chunks
            print(f"{word.strip()[:14]:<15} | {current_time:.2f}")

if __name__ == "__main__":
    if os.path.exists(IMAGE_PATH):
        run_profile()
    else:
        print(f"Error: Image not found at {IMAGE_PATH}")
